// Include files
// From Gaudi
#include "GaudiKernel/AlgFactory.h"
#include "GaudiKernel/IAlgManager.h"
#include "GaudiKernel/IJobOptionsSvc.h"
#include "GaudiAlg/ISequencerTimerTool.h"

#include "GaudiParallelizer.h"

// ----------------------------------------------------------------------------
// Implementation file for class: GaudiParallelizer
//
// 09/12/2011: Illya Shapoval
// ----------------------------------------------------------------------------
DECLARE_ALGORITHM_FACTORY(GaudiParallelizer)

// ============================================================================
// Standard constructor, initializes variables
// ============================================================================
GaudiParallelizer::GaudiParallelizer(const std::string& name, ISvcLocator* pSvcLocator)
  : GaudiAlgorithm(name, pSvcLocator)
  , m_timerTool( 0 )
{
  declareProperty( "Members"        , m_names                  );
  declareProperty( "ModeOR"         , m_modeOR         = false );
  declareProperty( "MeasureTime"    , m_measureTime    = false );
  declareProperty( "ReturnOK"       , m_returnOK       = false );
  declareProperty( "NumberOfThreads", m_nthreads       = 0 );

  m_names.declareUpdateHandler (&GaudiParallelizer::membershipHandler, this );
}

// ============================================================================
// Destructor
// ============================================================================
GaudiParallelizer::~GaudiParallelizer() {}

// ============================================================================
// Initialization
// ============================================================================
StatusCode GaudiParallelizer::initialize() {
  if ( msgLevel(MSG::DEBUG) ) debug() << "==> Initialize" << endmsg;
  StatusCode sc = GaudiAlgorithm::initialize(); // must be executed first
  if ( sc.isFailure() ) return sc; // error printed already by GaudiAlgorithm

  StatusCode status = decodeNames();
  if ( !status.isSuccess() ) return status;

  m_timerTool = tool<ISequencerTimerTool>( "SequencerTimerTool" );
  if ( m_timerTool->globalTiming() ) m_measureTime = true;

  if ( m_measureTime ) {
    m_timer = m_timerTool->addTimer( name() );
    m_timerTool->increaseIndent();
  } else {
    release( m_timerTool );
    m_timerTool = 0;
  }

  //== Initialize the algorithms
  std::vector<AlgorithmEntry>::iterator itE;
  for ( itE = m_entries.begin(); m_entries.end() != itE; itE++ ) {
    Algorithm* myAlg = itE->algorithm();
    if ( m_measureTime ) {
      itE->setTimer( m_timerTool->addTimer( myAlg->name() ) );
    }

    status = myAlg->sysInitialize();
    if ( !status.isSuccess() ) {
      return Error( "Can not initialize " + myAlg->name(),
                    status );
    }
  }

  if ( m_measureTime ) m_timerTool->decreaseIndent();

  if ( m_nthreads != 0 ) {
    // Construct the TBB task scheduler with m_nthreads threads
    tbb::task_scheduler_init init( m_nthreads );
  }
  else {
    m_nthreads = tbb::task_scheduler_init::default_num_threads();
  }

  if ( msgLevel(MSG::DEBUG) ) debug() << "Number of threads set to be used in the TBB thread pool is "
                                      << m_nthreads << endmsg;
  return StatusCode::SUCCESS;
}

// ============================================================================
// Main execution
// ============================================================================
StatusCode GaudiParallelizer::execute() {
  if ( m_measureTime ) m_timerTool->start( m_timer );

  if ( msgLevel(MSG::DEBUG) ) debug() << "==> Execute algorithms in parallel" << endmsg;

  for (std::vector<AlgorithmEntry>::iterator itE = m_entries.begin(); m_entries.end() != itE; ++itE ) {
    Algorithm* myAlg = itE->algorithm();
    if ( ! myAlg->isEnabled() ) continue;
      if ( ! myAlg->isExecuted() ) {

        m_task_group.run(boost::bind(&AlgorithmEntry::run,
                                     boost::ref(*itE),
                                     boost::ref(*this)));
      }
  }

  m_task_group.wait();
  if ( msgLevel(MSG::DEBUG) ) debug() << "==> Joining parallel algorithm tasks" << endmsg;

  for( std::vector<AlgorithmEntry>::const_iterator it = m_entries.begin(); it != m_entries.end(); ++it ){
    if ( msgLevel(MSG::DEBUG) ) debug() << "Algorithm wrapper " << &*it
                                        << " around the algorithm " << it->algorithm()->name()
                                        << " received return status code " << it->m_returncode
                                        << endmsg;
  }

  for( std::vector<AlgorithmEntry>::const_iterator it = m_entries.begin(); it != m_entries.end(); ++it )
    if ( !(it->m_returncode.isSuccess()) ) return it->m_returncode;

  setExecuted( true );
  if ( m_measureTime ) m_timerTool->stop( m_timer );
  return StatusCode::SUCCESS;
}

// ============================================================================
// Finalize
// ============================================================================
StatusCode GaudiParallelizer::finalize() {
  if ( msgLevel(MSG::DEBUG) ) debug() << "==> Finalize" << endmsg;

  return GaudiAlgorithm::finalize(); // must be called after all other actions
}

// ============================================================================

StatusCode GaudiParallelizer::decodeNames(){

  StatusCode final = StatusCode::SUCCESS;
  m_entries.clear();

  //== Get the "Context" option if in the file...
  IJobOptionsSvc* jos = svc<IJobOptionsSvc>( "JobOptionsSvc" );
  bool addedContext = false;  //= Have we added the context ?
  bool addedRootInTES = false;  //= Have we added the rootInTES ?
  bool addedGlobalTimeOffset = false;  //= Have we added the globalTimeOffset ?


  //= Get the Application manager, to see if algorithm exist
  IAlgManager* appMgr = svc<IAlgManager>("ApplicationMgr");
  const std::vector<std::string>& nameVector = m_names.value();
  std::vector<std::string>::const_iterator it;
  for ( it = nameVector.begin(); nameVector.end() != it; it++ ) {
    const Gaudi::Utils::TypeNameString typeName(*it);
    const std::string &theName = typeName.name();
    const std::string &theType = typeName.type();

    //== Check whether the specified algorithm already exists. If not, create it
    StatusCode result = StatusCode::SUCCESS;
    SmartIF<IAlgorithm> myIAlg = appMgr->algorithm(typeName, false); // do not create it now
    if ( !myIAlg.isValid() ) {
      //== Set the Context if not in the jobOptions list
      if ( ""  != context() ||
           ""  != rootInTES() ||
           0.0 != globalTimeOffset() ) {
        bool foundContext = false;
        bool foundRootInTES = false;
        bool foundGlobalTimeOffset = false;
        const std::vector<const Property*>* properties = jos->getProperties( theName );
        if ( 0 != properties ) {
          // Iterate over the list to set the options
          for ( std::vector<const Property*>::const_iterator itProp = properties->begin();
               itProp != properties->end();
               itProp++ )   {
            const StringProperty* sp = dynamic_cast<const StringProperty*>(*itProp);
            if ( 0 != sp )    {
              if ( "Context" == (*itProp)->name() ) {
                foundContext = true;
              }
              if ( "RootInTES" == (*itProp)->name() ) {
                foundRootInTES = true;
              }
              if ( "GlobalTimeOffset" == (*itProp)->name() ) {
                foundGlobalTimeOffset = true;
              }
            }
          }
        }
        if ( !foundContext && "" != context() ) {
          StringProperty contextProperty( "Context", context() );
          jos->addPropertyToCatalogue( theName, contextProperty ).ignore();
          addedContext = true;
        }
        if ( !foundRootInTES && "" != rootInTES() ) {
          StringProperty rootInTESProperty( "RootInTES", rootInTES() );
          jos->addPropertyToCatalogue( theName, rootInTESProperty ).ignore();
          addedRootInTES = true;
        }
        if ( !foundGlobalTimeOffset && 0.0 != globalTimeOffset() ) {
          DoubleProperty globalTimeOffsetProperty( "GlobalTimeOffset", globalTimeOffset() );
          jos->addPropertyToCatalogue( theName, globalTimeOffsetProperty ).ignore();
          addedGlobalTimeOffset = true;
        }
      }

      Algorithm *myAlg = 0;
      result = createSubAlgorithm( theType, theName, myAlg );
      // (MCl) this should prevent bug #35199... even if I didn't manage to
      // reproduce it with a simple test.
      if (result.isSuccess()) myIAlg = myAlg;
    } else {
      Algorithm *myAlg = dynamic_cast<Algorithm*>(myIAlg.get());
      if (myAlg) {
        subAlgorithms()->push_back(myAlg);
        // when the algorithm is not created, the ref count is short by one, so we have to fix it.
        myAlg->addRef();
      }
    }

    //== Remove the property, in case this is not a GaudiAlgorithm...
    if ( addedContext ) {
      jos->removePropertyFromCatalogue( theName, "Context" ).ignore();
      addedContext = false;
    }
    if ( addedRootInTES ) {
      jos->removePropertyFromCatalogue( theName, "RootInTES" ).ignore();
      addedRootInTES = false;
    }
    if ( addedGlobalTimeOffset ) {
      jos->removePropertyFromCatalogue( theName, "GlobalTimeOffset" ).ignore();
      addedGlobalTimeOffset = false;
    }

    // propagate the sub-algorithm into own state.
    if ( result.isSuccess () &&
         Gaudi::StateMachine::INITIALIZED <= FSMState() &&
         myIAlg.isValid   () &&
         Gaudi::StateMachine::INITIALIZED  > myIAlg->FSMState() )
    {
      StatusCode sc = myIAlg->sysInitialize() ;
      if  ( sc.isFailure() ) { result = sc ; }
    }

    // propagate the sub-algorithm into own state.
    if ( result.isSuccess () &&
         Gaudi::StateMachine::RUNNING <= FSMState() &&
         myIAlg.isValid   () &&
         Gaudi::StateMachine::RUNNING  > myIAlg->FSMState() )
    {
      StatusCode sc = myIAlg->sysStart () ;
      if  ( sc.isFailure() ) { result = sc ; }
    }

    //== Is it an Algorithm ?  Strange test...
    if ( result.isSuccess() ) {
      // TODO: (MCl) it is possible to avoid the dynamic_cast in most of the
      //             cases by keeping the result of createSubAlgorithm.
      Algorithm*  myAlg = dynamic_cast<Algorithm*>(myIAlg.get());
      if (myAlg!=0) {
        // Note: The reference counting is kept by the system of sub-algorithms
        m_entries.push_back( AlgorithmEntry( myAlg ) );
        if (msgLevel(MSG::DEBUG)) debug () << "Added algorithm " << theName << endmsg;
      } else {
        warning() << theName << " is not an Algorithm - failed dynamic_cast"
                  << endmsg;
        final = StatusCode::FAILURE;
      }
    } else {
      warning() << "Unable to find or create " << theName << endmsg;
      final = result;
    }

  }

  release(appMgr).ignore();
  release(jos).ignore();

  //== Print the list of algorithms
  MsgStream& msg = info();
  if ( m_modeOR ) msg << "OR ";
  msg << "Member list: ";
  std::vector<AlgorithmEntry>::iterator itE;
  for ( itE = m_entries.begin(); m_entries.end() != itE; itE++ ) {
    Algorithm* myAlg = (*itE).algorithm();
    std::string myAlgType = System::typeinfoName( typeid( *myAlg) ) ;
    if ( myAlg->name() == myAlgType ) {
      msg << myAlg->name();
    } else {
      msg << myAlgType << "/" << myAlg->name();
    }
    if ( itE+1 != m_entries.end() ) msg << ", ";
  }
  if ( "" != context() ) msg << ", with context '" << context() << "'";
  if ( "" != rootInTES() ) msg << ", with rootInTES '" << rootInTES() << "'";
  if ( 0.0 != globalTimeOffset() ) msg << ", with globalTimeOffset " << globalTimeOffset();
  msg << endmsg;

  return final;

}

//=========================================================================
//  Interface for the Property manager
//=========================================================================
void GaudiParallelizer::membershipHandler ( Property& /* p */ )
{
  // no action for not-yet initialized sequencer
  if ( Gaudi::StateMachine::INITIALIZED > FSMState() ) { return ; } // RETURN

  decodeNames().ignore();

  if  ( !m_measureTime ) { return ; }                                // RETURN

  // add the entries into timer table:

  if ( 0 == m_timerTool )
  { m_timerTool = tool<ISequencerTimerTool>( "SequencerTimerTool" ) ; }

  if ( m_timerTool->globalTiming() ) m_measureTime = true;

  m_timer = m_timerTool->addTimer( name() );
  m_timerTool->increaseIndent();

  for ( std::vector<AlgorithmEntry>::iterator itE = m_entries.begin() ;
        m_entries.end() != itE; ++itE )
  {
    itE->setTimer( m_timerTool->addTimer( itE->algorithm()->name() ) );
  }

  m_timerTool->decreaseIndent();

}
//=============================================================================
