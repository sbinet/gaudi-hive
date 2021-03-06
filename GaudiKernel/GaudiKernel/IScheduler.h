#ifndef GAUDIKERNEL_ISCHEDULER_H
#define GAUDIKERNEL_ISCHEDULER_H

// Framework include files
#include "GaudiKernel/EventContext.h"
#include "GaudiKernel/IInterface.h"

// C++ include files
#include <functional>

/**@class IScheduler IScheduler.h GaudiKernel/IScheduler.h
 *
 *  General interface for algorithm scheduler.
 * 
 *  @author  Danilo Piparo
 *  @version 1.0
 */
class GAUDI_API IScheduler: virtual public IInterface {
public:
  /// InterfaceID
  DeclareInterfaceID(IScheduler,1,0);
  
  /// Make an event available to the scheduler
  virtual StatusCode pushNewEvent(EventContext* eventContext) = 0;
    
  /// Retrieve a finished event from the scheduler
  virtual StatusCode popFinishedEvent(EventContext*& eventContext) = 0;

  /// Try to retrieve a finished event from the scheduler
  virtual StatusCode tryPopFinishedEvent(EventContext*& eventContext) = 0;
  
  /// Get the free event processing slots
  virtual unsigned int freeSlots() = 0;
  
};
#endif
