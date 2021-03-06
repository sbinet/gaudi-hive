// Framework includes
#include "GaudiKernel/SvcFactory.h"
#include "GaudiKernel/IAlgorithm.h"
#include "GaudiKernel/Algorithm.h" // will be IAlgorithm if context getter promoted to interface
#include "tbb/task.h"

// C++
#include <unordered_set>
#include <algorithm>
#include <map>
#include <sstream>

// Local 
#include "ForwardSchedulerSvc.h"
#include "AlgoExecutionTask.h"
#include "AlgResourcePool.h"

// External libs
// DP waiting for the TBB service
#include "tbb/task_scheduler_init.h"

// Instantiation of a static factory class used by clients to create instances of this service
DECLARE_SERVICE_FACTORY(ForwardSchedulerSvc)

//===========================================================================
// Infrastructure methods

ForwardSchedulerSvc::ForwardSchedulerSvc( const std::string& name, ISvcLocator* svcLoc ):
 base_class(name,svcLoc),
 m_isActive(false),
 m_algosInFlight(0),
 m_threadPoolSize(1) 
{
  declareProperty("MaxEventsInFlight", m_maxEventsInFlight = 1 );
  declareProperty("MaxAlgosInFlight", m_maxAlgosInFlight = 1 );
  declareProperty("ThreadPoolSize", m_threadPoolSize = 1 );
  declareProperty("WhiteboardSvc", m_whiteboardSvcName = "EventDataSvc" );
  // Will disappear when dependencies are properly propagated into the C++ code of the algos
  declareProperty("AlgosDependencies", m_algosDependencies);    
}

//---------------------------------------------------------------------------
ForwardSchedulerSvc::~ForwardSchedulerSvc(){}
//---------------------------------------------------------------------------

StatusCode ForwardSchedulerSvc::initialize(){

  // Initialise mother class (read properties, ...)  
  StatusCode sc(Service::initialize());
  if (!sc.isSuccess())
    warning () << "Base class could not be initialized" << endmsg;  

  // Get the algo resource pool
  m_algResourcePool = serviceLocator()->service("AlgResourcePool");
  if (!m_algResourcePool.isValid())
    error() << "Error retrieving AlgoResourcePool" << endmsg;  
  
  // Get Whiteboard
  m_whiteboard = serviceLocator()->service(m_whiteboardSvcName);
  if (!m_whiteboard.isValid())
    fatal() << "Error retrieving EventDataSvc interface IHiveWhiteBoard." << endmsg;  
  
  // Set the number of slots
  m_freeSlots=m_maxEventsInFlight; 
  
  // Get the list of algorithms
  const std::list<IAlgorithm*>& algos = m_algResourcePool->getFlatAlgList();  
  const unsigned int algsNumber = algos.size(); 
  info() << "Found " <<  algsNumber << " algorithms" << endmsg;

  // Prepare empty event slots
  info() << "Setting the whiteboard slots to " << m_maxEventsInFlight << endmsg;
  sc = m_whiteboard->setNumberOfStores(m_maxEventsInFlight);
  if (!sc.isSuccess())
    warning() << "Number of stores in the WhiteBoard could not be properly set!" << endmsg;

  const unsigned int algosDependenciesSize=m_algosDependencies.size();
  info() << "Algodependecies size is " << algosDependenciesSize << endmsg;

  /* Dependencies
   0) Read deps from config file
   1) Look for handles in algo, if none
   2) Assume none are required
  */
  if (algosDependenciesSize == 0){    
    for (IAlgorithm* ialgoPtr : algos){
      Algorithm* algoPtr = dynamic_cast<Algorithm*> (ialgoPtr);
      const std::vector<MinimalDataObjectHandle*>& algoHandles(algoPtr->handles());
      std::vector<std::string> algoDependencies;
      if (!algoHandles.empty()){
        info() << "Algorithm " << algoPtr->name() << " data dependencies:" << endmsg;
        for (MinimalDataObjectHandle* handlePtr : algoHandles ){
          if (handlePtr->accessType() == IDataObjectHandle::AccessType::READ){
            const std::string& productName = handlePtr->dataProductName();
            info() << "  o READ Handle found for product " << productName << endmsg;
            algoDependencies.emplace_back(productName);
          }
        }          
      } else {
        info() << "Algorithm " << algoPtr->name() << " has no data dependencies." << endmsg;
      }
      
      m_algosDependencies.emplace_back(algoDependencies);      
    }
  }

  // Fill the containers to convert algo names to index 
  m_algname_vect.reserve(algsNumber);
  unsigned int index=0;
  for (IAlgorithm* algo : algos){
    const std::string& name = algo->name();
    m_algname_index_map[name]=index;
    m_algname_vect.emplace_back(name);
    index++;
  }

  // prepare the control flow part
  const AlgResourcePool* algPool = dynamic_cast<const AlgResourcePool*>(m_algResourcePool.get());
  m_cfManager.initialize(algPool->getControlFlow(), m_algname_index_map);
  unsigned int controlFlowNodeNumber = algPool->getControlFlowNodeCounter();
  // Shortcut for the message service
  SmartIF<IMessageSvc> messageSvc (serviceLocator());
  if (!messageSvc.isValid())
    error() << "Error retrieving MessageSvc interface IMessageSvc." << endmsg;
    
  m_eventSlots.assign(m_maxEventsInFlight,EventSlot(m_algosDependencies,algsNumber,controlFlowNodeNumber,messageSvc));
  std::for_each(m_eventSlots.begin(),m_eventSlots.end(),[](EventSlot& slot){slot.complete=true;});

  // Clearly inform about the level of concurrency
  info() << "Concurrency level information:" << endmsg;
  info() << " o Number of events in flight: " << m_maxEventsInFlight << endmsg;
  info() << " o Number of algorithms in flight: " << m_maxAlgosInFlight << endmsg;
  info() << " o TBB thread pool size: " << m_threadPoolSize << endmsg;
          
   
  // Activate the scheduler 
  info() << "Activating scheduler in a separate thread" << endmsg;
  m_thread = std::thread (std::bind(&ForwardSchedulerSvc::m_activate,
                                    this));  
  return StatusCode::SUCCESS;
  
}
//---------------------------------------------------------------------------  

StatusCode ForwardSchedulerSvc::finalize(){

  StatusCode sc(Service::finalize());
  if (!sc.isSuccess())
    warning () << "Base class could not be finalized" << endmsg;   
  
  sc = m_deactivate();
  if (!sc.isSuccess())
    warning () << "Scheduler could not be deactivated" << endmsg;
    
  info() << "Joining Scheduler thread" << endmsg;
  m_thread.join();  
  
  return sc;

  }
//---------------------------------------------------------------------------  
/**
 * Activate the scheduler. From this moment on the queue of actions is 
 * checked. The checking will stop when the m_isActive flag is false and the 
 * queue is not empty. This will guarantee that all actions are executed and 
 * a stall is not created.
 */
void ForwardSchedulerSvc::m_activate(){  
  
  // Now it's running
  m_isActive=true;

  /** The pool must be initialised in the thread from where the tasks are 
   * launched (http://threadingbuildingblocks.org/docs/doxygen/a00342.html)
   * The scheduler is initialised here since this method runs in a separate
   * thread and spawns the tasks (through the execution of the lambdas)
  **/

  debug() << "Initialising a TBB thread pool of size " << m_threadPoolSize << endmsg;
  tbb::task_scheduler_init TBBSchedInit(m_threadPoolSize);
  
  // Wait for actions pushed into the queue by finishing tasks.
  action thisAction;  
  StatusCode sc(StatusCode::SUCCESS);
  
  // Continue to wait if the scheduler is running or there is something to do
  info() << "Start checking the actionsQueue" << endmsg;
  while(m_isActive or m_actionsQueue.size()!=0){
    m_actionsQueue.pop(thisAction);
    sc = thisAction();
    if (sc!=StatusCode::SUCCESS)
      verbose() << "Action did not succed (which is not bad per se)." << endmsg;
    else
      verbose() << "Action succed." << endmsg;
  }
}

//---------------------------------------------------------------------------

/**
 * Deactivates the scheduler. Two actions are pushed into the queue:
 *  1) Drain the scheduler untill all events are finished.
 *  2) Flip the status flag m_isActive to false
 * This second action is the last one to be executed by the scheduler.
 */
StatusCode ForwardSchedulerSvc::m_deactivate(){
  
  if (m_isActive){
    // Drain the scheduler
    m_actionsQueue.push(std::bind(&ForwardSchedulerSvc::m_drain,
                                  this));    
    // This would be the last action
    m_actionsQueue.push([this]() -> StatusCode {m_isActive=false;return StatusCode::SUCCESS;});
  }
  
  return StatusCode::SUCCESS;
}

//===========================================================================

//===========================================================================
// Utils and shortcuts 

inline const std::string& ForwardSchedulerSvc::m_index2algname (unsigned int index) {
  return m_algname_vect[index];
}

//---------------------------------------------------------------------------

inline unsigned int ForwardSchedulerSvc::m_algname2index(const std::string& algoname) {
  unsigned int index = m_algname_index_map[algoname];
  return index;
}  

//===========================================================================
// EventSlot management
/**
 * Add event to the scheduler. There are two cases possible:
 *  1) No slot is free. A StatusCode::FAILURE is returned.
 *  2) At least one slot is free. An action which resets the slot and kicks 
 * off its update is queued.
 */
StatusCode ForwardSchedulerSvc::pushNewEvent(EventContext* eventContext){
  
  if (!eventContext){
    fatal() << "Event context is nullptr" << endmsg;
    return StatusCode::FAILURE;
    }  
  
  if (m_freeSlots == 0){
    info() << "A free processing slot could not be found." << endmsg;
    return StatusCode::FAILURE;   
    }

  m_freeSlots--;

  auto action = [this,eventContext] () -> StatusCode {
    // Event processing slot forced to be the same as the wb slot
    const unsigned int thisSlotNum = eventContext->m_evt_slot;
    EventSlot& thisSlot = m_eventSlots[thisSlotNum];
    if (!thisSlot.complete)
      fatal() << "The slot " << thisSlotNum << " is supposed to be a finished event but it's not" << endmsg;
    info() << "A free processing slot was found." << endmsg;
    thisSlot.reset(eventContext);
    return this->m_updateStates(thisSlotNum);
  }; // end of lambda

  
// // HACK
//   static decltype(action)* prevAction;
//   if (eventContext->m_evt_num == 0){
//     m_actionsQueue.push(action);
//     return StatusCode::SUCCESS;
//   }
//   else if(eventContext->m_evt_num == 1){
//     always() << "Holding update states since evt number is 1" << endmsg;
//     prevAction=new decltype(action) (action);
//     return StatusCode::SUCCESS;
//   }
//   else if(eventContext->m_evt_num == 2){
//     always() << "Pushing update states for 1 and 2 since evt number is 2" << endmsg;
//     m_actionsQueue.push(action);
//     m_actionsQueue.push(*prevAction);
//     return StatusCode::SUCCESS;
//   }
//   else{
//     m_actionsQueue.push(action);
//     return StatusCode::SUCCESS;
//   }
  

  // Kick off the scheduling!
  m_actionsQueue.push(action);

  return StatusCode::SUCCESS;;
}
//---------------------------------------------------------------------------

unsigned int ForwardSchedulerSvc::freeSlots(){
  return m_freeSlots;
  }

//---------------------------------------------------------------------------

StatusCode ForwardSchedulerSvc::m_drain(){
  
  unsigned int slotNum=0;
  for (auto& thisSlot : m_eventSlots){
    if (not thisSlot.algsStates.allAlgsExecuted() and not thisSlot.complete){
      m_updateStates(slotNum);
    }
    slotNum++;
  }
  return StatusCode::SUCCESS;
}

//---------------------------------------------------------------------------
/**
* Get a finished event or block until one becomes available.
*/
StatusCode ForwardSchedulerSvc::popFinishedEvent(EventContext*& eventContext){
  if (static_cast<int>(m_freeSlots) == m_maxEventsInFlight){
      return StatusCode::FAILURE;     
  }
  else{
    m_finishedEvents.pop(eventContext);
    m_freeSlots++;
    debug() << "Popped slot " << eventContext->m_evt_slot << "(event "
            << eventContext->m_evt_num << ")" << endmsg;
    return StatusCode::SUCCESS;
  }
}

//---------------------------------------------------------------------------
/**
* Try to get a finished event, if not available just fail
*/
StatusCode ForwardSchedulerSvc::tryPopFinishedEvent(EventContext*& eventContext){
  if (m_finishedEvents.try_pop(eventContext)){
    debug() << "Try Pop successful slot " << eventContext->m_evt_slot 
            << "(event " << eventContext->m_evt_num << ")" << endmsg;
    m_freeSlots++;
    return StatusCode::SUCCESS;
  }
  return StatusCode::FAILURE;
}

//---------------------------------------------------------------------------
/// Stops scheduling and returns the failure
StatusCode ForwardSchedulerSvc::m_eventFailed(EventContext* eventContext){
  
  fatal() << "Event " << eventContext->m_evt_num << " on slot " 
          << eventContext->m_evt_slot << " failed" << endmsg;

  m_dumpSchedulerState(-1);
          
  // Set the number of slots available to 0
  m_freeSlots=0;          
          
  // Empty queue and deactivate the service
  action thisAction;
  while(m_actionsQueue.try_pop(thisAction)){};
  m_deactivate();
  
  // Push into the finished events queue the failed context
  EventContext* thisEvtContext;
  while(m_finishedEvents.try_pop(thisEvtContext)){};
  m_finishedEvents.push(eventContext);
  
  return StatusCode::FAILURE;
  
}

//===========================================================================

//===========================================================================
// States Management

StatusCode ForwardSchedulerSvc::m_updateStates(EventSlotIndex si){

  // Fill a map of initial state / action using closures.
  // done to update the states w/o several if/elses
  // Posterchild for constexpr with gcc4.7 onwards!
  const std::map<AlgsExecutionStates::State, std::function<StatusCode(AlgoSlotIndex iAlgo, EventSlotIndex si)>> 
   statesTransitions = {
  {AlgsExecutionStates::CONTROLREADY, std::bind(&ForwardSchedulerSvc::m_promoteToDataReady,
                                      this,
                                      std::placeholders::_1,  
                                      std::placeholders::_2)},
  {AlgsExecutionStates::DATAREADY, std::bind(&ForwardSchedulerSvc::m_promoteToScheduled,
                                   this,
                                   std::placeholders::_1,
                                   std::placeholders::_2)}
  };

  StatusCode global_sc(StatusCode::FAILURE);
  StatusCode partial_sc;

   // Sort from the oldest to the newest event
   // Prepare a vector of pointers to the slots to avoid copies
   std::vector<EventSlot*> eventSlotsPtrs;

   // Consider all slots if si <0 or just one otherwhise
   if (si<0){
   const int eventsSlotsSize(m_eventSlots.size());
   eventSlotsPtrs.reserve(eventsSlotsSize);
    for (auto slotIt=m_eventSlots.begin();slotIt!=m_eventSlots.end();slotIt++){
      if (!slotIt->complete)
        eventSlotsPtrs.push_back(&(*slotIt));
      }
    std::sort(eventSlotsPtrs.begin(),
              eventSlotsPtrs.end(), 
              [](EventSlot* a, EventSlot* b){return a->eventContext->m_evt_num < b->eventContext->m_evt_num;});
    } else{
      eventSlotsPtrs.push_back(&m_eventSlots[si]);
    }

  for (EventSlot* thisSlotPtr : eventSlotsPtrs){
    EventSlotIndex iSlot = thisSlotPtr->eventContext->m_evt_slot;

    // Cache the states of the algos to improve readability and performance
    auto& thisSlot = m_eventSlots[iSlot];
    AlgsExecutionStates& thisAlgsStates = thisSlot.algsStates;

    // Take care of the control ready update
    m_cfManager.updateEventState(thisAlgsStates.m_states,thisSlot.controlFlowState);

    for (unsigned int iAlgo=0;iAlgo<m_algname_vect.size();++iAlgo){
      const AlgsExecutionStates::State& algState = thisAlgsStates.algorithmState(iAlgo);
      if (algState==AlgsExecutionStates::ERROR)
        error() << " Algo " << m_index2algname(iAlgo) << " is in ERROR state." << endmsg;
      // Loop on state transitions from the one suited to algo state up to the one for SCHEDULED.
      partial_sc=StatusCode::SUCCESS;
      for (auto state_transition = statesTransitions.find(algState);
           state_transition!=statesTransitions.end() && partial_sc.isSuccess();
           state_transition++){
        partial_sc = state_transition->second(iAlgo,iSlot);
        if (partial_sc.isFailure()){
          debug() << "Could not apply transition from " 
              << thisAlgsStates.algorithmState(iAlgo) << " for algorithm " << m_index2algname(iAlgo)
              << " on processing slot " << iSlot << endmsg;
          }
        else{global_sc=partial_sc;}
        } // end loop on transitions
    } // end loop on algos

    // Not complete because this would mean that the slot is already free!
    if (!thisSlot.complete &&
      !thisSlot.algsStates.algsPresent(AlgsExecutionStates::CONTROLREADY) &&
      !thisSlot.algsStates.algsPresent(AlgsExecutionStates::DATAREADY) &&
      !thisSlot.algsStates.algsPresent(AlgsExecutionStates::SCHEDULED)){
      thisSlot.complete=true;
      m_finishedEvents.push(thisSlot.eventContext);
      debug() << "Event " << thisSlot.eventContext->m_evt_num 
             << " finished (slot "<< thisSlot.eventContext->m_evt_slot 
             << ")." << endmsg;
      // now let's return the fully evaluated result of the control flow
      std::stringstream ss;
      m_cfManager.printEventState(ss,thisSlot.controlFlowState,0);
      debug() << ss.str() << endmsg;
      thisSlot.eventContext= nullptr;
    } else{
      m_isStalled(iSlot).ignore();
    }

  } // end loop on slots    

  verbose() << "States Updated." << endmsg;

  return global_sc;
}

//---------------------------------------------------------------------------

StatusCode ForwardSchedulerSvc::m_isStalled(EventSlotIndex iSlot){
  // Get the slot
  EventSlot& thisSlot = m_eventSlots[iSlot];

  if (m_actionsQueue.empty() &&
      m_algosInFlight == 0 &&
      (!thisSlot.algsStates.algsPresent(AlgsExecutionStates::DATAREADY))){

    info() << "About to declare a stall"<< endmsg;
    fatal() << "Stall detected!" << endmsg;
    m_dumpSchedulerState(iSlot);
    throw GaudiException ("Stall detected",
                          name(),
                          StatusCode::FAILURE);
    return StatusCode::FAILURE;
  }
  return StatusCode::SUCCESS;
}

//---------------------------------------------------------------------------

void ForwardSchedulerSvc::m_dumpSchedulerState(EventSlotIndex iSlot){

  EventSlotIndex slotCount = -1;
  for (auto thisSlot : m_eventSlots){
    slotCount++;

    if ( thisSlot.complete )
      continue;
    
    if ( 0 > iSlot or iSlot == slotCount){      
      fatal() << "Algorithms states for event " << thisSlot.eventContext->m_evt_num << endmsg;
      unsigned int algoIndex=0;
      for (const AlgsExecutionStates::State& thisState : thisSlot.algsStates ){
        fatal() << " o " << m_index2algname(algoIndex)
                << " was in state " << AlgsExecutionStates::stateNames[thisState]
                << ". Its data dependencies are ";
        auto deps (thisSlot.dataFlowMgr.dataDependencies(algoIndex));
        char separator=',';
        std::stringstream depsStringStream;
        const int depsSize=deps.size();
        if (depsSize==0){
          depsStringStream << " none.";
        }

        for (int i=0;i<depsSize;++i){
          if (i==depsSize-1)
            separator = ' ';
          depsStringStream << deps[i] << separator;
          }
         algoIndex++;
         fatal() << depsStringStream.str() << endmsg;
      }
      
      
      // Snapshot of the WhiteBoard
      fatal() << "The content of the whiteboard for this event was:" << endmsg;
      const auto& wbSlotContent ( thisSlot.dataFlowMgr.content() );
      for (auto& product : wbSlotContent ){
        fatal() << " o " << product << endmsg;
      }

      // Snapshot of the ControlFlow
      fatal() << "The status of the control flow for this event was:" << endmsg;
      std::stringstream cFlowStateStringStream;
      m_cfManager.printEventState(cFlowStateStringStream,thisSlot.controlFlowState,0);

      fatal() << cFlowStateStringStream.str() << endmsg;

      }

  }

}

//---------------------------------------------------------------------------

StatusCode ForwardSchedulerSvc::m_promoteToControlReady(AlgoSlotIndex iAlgo, EventSlotIndex si){

  // Do the control flow
  StatusCode sc = m_eventSlots[si].algsStates.updateState(iAlgo,AlgsExecutionStates::CONTROLREADY);
  if (sc.isSuccess())
    debug() << "Promoting " << m_index2algname(iAlgo) << " to CONTROLREADY" << endmsg;

  return sc;

}

//---------------------------------------------------------------------------

StatusCode ForwardSchedulerSvc::m_promoteToDataReady(AlgoSlotIndex iAlgo, EventSlotIndex si){

  StatusCode sc (m_eventSlots[si].dataFlowMgr.canAlgorithmRun(iAlgo));
  StatusCode updateSc(StatusCode::FAILURE);
  if (sc == StatusCode::SUCCESS)
    updateSc = m_eventSlots[si].algsStates.updateState(iAlgo,AlgsExecutionStates::DATAREADY);

  if (updateSc.isSuccess())
    debug() << "Promoting " << m_index2algname(iAlgo) << " to DATAREADY" << endmsg;

  return updateSc;

}

//---------------------------------------------------------------------------

StatusCode ForwardSchedulerSvc::m_promoteToScheduled(AlgoSlotIndex iAlgo, EventSlotIndex si){
  
  if (m_algosInFlight == m_maxAlgosInFlight)
    return StatusCode::FAILURE;

  const std::string& algName(m_index2algname(iAlgo));
  
  IAlgorithm* ialgoPtr=nullptr;
  StatusCode sc ( m_algResourcePool->acquireAlgorithm(algName,ialgoPtr) );
  
  if (sc.isSuccess()){
    Algorithm* algoPtr = dynamic_cast<Algorithm*> (ialgoPtr); // DP: expose the setter of the context?   
    EventContext* eventContext ( m_eventSlots[si].eventContext );
    if (!eventContext)
      fatal() << "Event context for algorithm " << algName 
              << " is a nullptr (slot " << si<< ")" << endmsg;

    algoPtr->setContext(m_eventSlots[si].eventContext);
    tbb::task* t = new( tbb::task::allocate_root() ) AlgoExecutionTask(ialgoPtr, iAlgo, serviceLocator(), this);
    tbb::task::enqueue( *t);
    ++m_algosInFlight;
    info() << "Algorithm " << algName << " was submitted on event "
           << eventContext->m_evt_num <<  ". Algorithms scheduled are "
           << m_algosInFlight << endmsg;

    StatusCode updateSc ( m_eventSlots[si].algsStates.updateState(iAlgo,AlgsExecutionStates::SCHEDULED) );
    if (updateSc.isSuccess())
      debug() << "Promoting " << m_index2algname(iAlgo) << " to SCHEDULED" << endmsg;
    return updateSc;
  }
  else{
    info() << "Could not acquire instance for algorithm " 
        << m_index2algname(iAlgo) << " on slot " << si << endmsg;
    return sc;
  }

}

//---------------------------------------------------------------------------
/// The call to this method is triggered only from within the AlgoExecutionTask.
StatusCode ForwardSchedulerSvc::m_promoteToExecuted(AlgoSlotIndex iAlgo, EventSlotIndex si, IAlgorithm* algo){  

  // Put back the instance
  Algorithm* castedAlgo = dynamic_cast<Algorithm*>(algo); // DP: expose context getter in IAlgo?
  if (!castedAlgo)
    fatal() << "The casting did not succed!" << endmsg;
  EventContext* eventContext = castedAlgo->getContext();

  // Checkif the execution failed
  if (eventContext->m_evt_failed)
    m_eventFailed(eventContext);
  
  StatusCode sc = m_algResourcePool->releaseAlgorithm(algo->name(),algo);

  if (!sc.isSuccess()){
    error() << "[Event " << eventContext->m_evt_num 
            << ", Slot " << eventContext->m_evt_slot  << "] "
            << "Instance of algorithm " << algo->name()
            << " could not be properly put back." << endmsg;
    return StatusCode::FAILURE;
    }

  m_algosInFlight--;  

  // Update the catalog: some new products may be there
  m_whiteboard->selectStore(eventContext->m_evt_slot).ignore();

  // update prods in the dataflow
  // DP: Handles could be used. Just update what the algo wrote
  std::vector<std::string> new_products;
  m_whiteboard->getNewDataObjects(new_products).ignore();
  for (const auto& new_product : new_products)
    debug() << "Found in WB: " << new_product << endmsg;
  m_eventSlots[si].dataFlowMgr.updateDataObjectsCatalog(new_products);

  // update controlflow
  // .......

  debug() << "Algorithm " << algo->name() << " executed. Algorithms scheduled are "
      << m_algosInFlight << endmsg;

  // Schedule an update of the status of the algorithms
  auto updateAction = std::bind(&ForwardSchedulerSvc::m_updateStates,
                                this,
                                -1);
  m_actionsQueue.push(updateAction);

  debug() << "Trying to handle execution result of " << m_index2algname(iAlgo) << "." << endmsg;
  State state;
  if (algo->filterPassed()){
    state = State::EVTACCEPTED;
  } else {
    state = State::EVTREJECTED;
  }

  sc = m_eventSlots[si].algsStates.updateState(iAlgo,state);
  if (sc.isSuccess())
    debug() << "Promoting " << m_index2algname(iAlgo) << " on slot " << si << " to " << AlgsExecutionStates::stateNames[state] << endmsg;
  return sc;
}

//===========================================================================



