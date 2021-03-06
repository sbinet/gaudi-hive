#ifndef GAUDIKERNEL_EVENTCONTEXT_H
#define GAUDIKERNEL_EVENTCONTEXT_H

#include <memory>

/** @class EventContext EventContext.h GaudiKernel/EventContext.h
 *
 * This class represents an entry point to all the event specific data.
 * It is needed to make the algorithm "aware" of the event it is operating on.
 * This was not needed in the serial version of Gaudi where the assumption
 * of 1-event-at-the-time processing was implicit.
 *
 * This class has nothing to do with the AlgContextSvc!
 *
 * @author Danilo Piparo
 * @date 2012
 **/

class _opaque_pthread_t;

// Thread id type
#ifdef __APPLE__
  #define THREADID_TYPE _opaque_pthread_t*
#else
  #define THREADID_TYPE unsigned long int
#endif


// fast implementation, to be better organised.
class EventContext{
public:
  EventContext():
    m_evt_num(0),
    m_evt_slot(0),
    m_thread_id(0){};
  bool m_evt_failed;
  long int m_evt_num;
  size_t   m_evt_slot;
  THREADID_TYPE m_thread_id;
};

#endif //GAUDIKERNEL_EVENTCONTEXT_H
