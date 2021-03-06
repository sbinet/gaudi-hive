#ifndef GAUDIHIVE_ALGOEXECUTIONTASK_H
#define GAUDIHIVE_ALGOEXECUTIONTASK_H

// Framework include files
#include "GaudiKernel/IAlgorithm.h"
#include "GaudiKernel/SmartIF.h"
#include "GaudiKernel/ISvcLocator.h"

#include "ForwardSchedulerSvc.h"

// External libs
#include "tbb/task.h"

class AlgoExecutionTask: public tbb::task {
public:
  AlgoExecutionTask(IAlgorithm* algorithm, 
                    unsigned int algoIndex, 
                    ISvcLocator* svcLocator,
                    ForwardSchedulerSvc* schedSvc):
    m_algorithm(algorithm),
    m_algoIndex(algoIndex),
    m_schedSvc(schedSvc),
    m_serviceLocator(svcLocator){};
  virtual tbb::task* execute();
private:  
  SmartIF<IAlgorithm> m_algorithm;
  const unsigned int m_algoIndex;
  // For the callbacks on task finishing
  SmartIF<ForwardSchedulerSvc> m_schedSvc;
  SmartIF<ISvcLocator> m_serviceLocator;
};

#endif
