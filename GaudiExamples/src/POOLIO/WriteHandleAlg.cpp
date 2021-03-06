// Framework include files
#include "GaudiKernel/AlgFactory.h"
#include "GaudiKernel/MsgStream.h"

#include "GaudiKernel/IDataProviderSvc.h"
#include "GaudiKernel/IDataManagerSvc.h"

#include "WriteHandleAlg.h"

DECLARE_ALGORITHM_FACTORY(WriteHandleAlg)

//---------------------------------------------------------------------------  

WriteHandleAlg::WriteHandleAlg ( const std::string& name , // the algorithm instance name 
              ISvcLocator*pSvc ):
              GaudiAlgorithm ( name , pSvc ){

      declareProperty("UseHandle", m_useHandle = true, "Specify the usage of the handle to write");

      // For Concurrent run
      declareProperty("Output", m_output_name, "The output name");
    }
//---------------------------------------------------------------------------

StatusCode WriteHandleAlg::initialize(){
  MsgStream log(msgSvc(), name());

  StatusCode outputSC = declareDataObj(m_output_name, m_output_handle, IDataObjectHandle::WRITE);  
  return outputSC.isSuccess();
}

//---------------------------------------------------------------------------

StatusCode WriteHandleAlg::execute  ()  // the execution of the algorithm 
{

  MsgStream log(msgSvc(), name());
  
  log << MSG::INFO << "Hello, I am executing" << endmsg;

  // Set collision to the current event number from the context; 
  // if the context doesn't exist, set it to some dummy value 
  // this fallback allows to stay compatible with non-hive infrastructure 
  Collision* c = new Collision(getContext() ? getContext()->m_evt_num : 42);

  if (m_useHandle) m_output_handle->put(c);
  else eventSvc()->registerObject("/Event","MyCollision",c);
  
  return StatusCode::SUCCESS ;
}

//---------------------------------------------------------------------------

StatusCode WriteHandleAlg::finalize () // the finalization of the algorithm 
{ 
   return GaudiAlgorithm::finalize () ;
}

//---------------------------------------------------------------------------
