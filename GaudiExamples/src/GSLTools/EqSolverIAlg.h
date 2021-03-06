// $Id: EqSolverIAlg.h,v 1.1 2003/11/27 11:05:27 mato Exp $
#ifndef ALGTOOLS_EQSOLVERIALG_H 
#define ALGTOOLS_EQSOLVERIALG_H 1


// Include files

// from Gaudi
#include "GaudiKernel/Algorithm.h"
#include "GaudiKernel/Property.h"
#include "GaudiKernel/MsgStream.h"

/// Forward references
class IEqSolver;

//-----------------------------------------------------------------------------
/**  @class EqSolverIAlg EqSolver.h
 *   @file Algorithm file for the class IEqSolver
 *   @see GaudiGSL/IEqSolver.h
 *   @author Kirill Miklyaev kirillm@iris1.itep.ru
 *   @date   2003-07-07
 */
//-----------------------------------------------------------------------------

class EqSolverIAlg : public Algorithm {

public:
  /// Standard constructor
  EqSolverIAlg( const std::string& name, ISvcLocator* pSvcLocator );

  virtual ~EqSolverIAlg( ); ///< Destructor

  virtual StatusCode initialize();    ///< Algorithm initialization
  virtual StatusCode execute   ();    ///< Algorithm execution
  virtual StatusCode finalize  ();    ///< Algorithm finalization

protected:

private:

  IEqSolver*   m_privateTool;
  IEqSolver*   m_publicTool;

};
#endif // ALGTOOLS_EQSOLVERIALG_H
