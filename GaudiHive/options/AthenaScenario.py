import json
from Gaudi.Configuration import *
# ============================================================================
from Configurables import GaudiExamplesCommonConf, CPUCruncher,HiveEventLoopMgr
#GaudiExamplesCommonConf()
# ============================================================================     

#-------------------------------------------------------------------------------
# Metaconfig

NUMBEROFEVENTS = 10
NUMBEROFEVENTSINFLIGHT = 1
NUMBEROFALGOSINFLIGHT = 1000
NUMBEROFTHREADS = 4
CLONEALGOS = False
DUMPQUEUES = False
VERBOSITY = 5


NumberOfEvents = NUMBEROFEVENTS
NumberOfEventsInFlight = NUMBEROFEVENTSINFLIGHT
NumberOfAlgosInFlight = NUMBEROFALGOSINFLIGHT
NumberOfThreads = NUMBEROFTHREADS
CloneAlgos = CLONEALGOS
DumpQueues = DUMPQUEUES
Verbosity = VERBOSITY


def load_athena_scenario(filename):
  data = open(filename).read()
  workflow = eval(data)
  cpu_cruncher_algos = []
  all_outputs = set()
  all_inputs  = set()
  for algo in workflow["algorithms"]:
    new_algo = CPUCruncher(algo["name"],
                           avgRuntime=float(algo["runtimes_wall"][1]/1000000.),
                           Inputs = algo["inputs"],
                           Outputs = algo["outputs"]
                           )
    cpu_cruncher_algos.append(new_algo)
    all_outputs.update(algo["outputs"])
    all_inputs.update(algo["inputs"])
  
  #look for the objects that haven't been provided within the job. Assume this needs to come via input
  new_algo = CPUCruncher("input",
                         avgRuntime=1,
                         Inputs=[],
                         Outputs=[item for item in all_inputs.difference(all_outputs)]
                         )
  cpu_cruncher_algos.append(new_algo)

  print [item for item in all_inputs.difference(all_outputs)]
  return cpu_cruncher_algos
        
# Set output level threshold 2=DEBUG, 3=INFO, 4=WARNING, 5=ERROR, 6=FATAL )
ms = MessageSvc() 
ms.OutputLevel     =  Verbosity

crunchers = load_athena_scenario("Athena.json")

# Setup the Event Loop Manager
evtloop = HiveEventLoopMgr()
evtloop.MaxAlgosParallel = NumberOfAlgosInFlight
evtloop.MaxEventsParallel = NumberOfEventsInFlight
evtloop.NumThreads = NumberOfThreads 
evtloop.CloneAlgorithms = CloneAlgos
evtloop.DumpQueues = DumpQueues

# And the Application Manager
app = ApplicationMgr()
app.TopAlg = crunchers
app.EvtSel = "NONE" # do not use any event input
app.EvtMax = NumberOfEvents
app.EventLoop = evtloop
#app.MessageSvcType = "TBBMessageSvc"


