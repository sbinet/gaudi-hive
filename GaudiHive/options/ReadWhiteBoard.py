####################################################################
# Write a DST and a miniDST, including File Summary Records
####################################################################

from Gaudi.Configuration import *
from Configurables import Gaudi__RootCnvSvc as RootCnvSvc, GaudiPersistency
from Configurables import WriteHandleAlg, ReadHandleAlg, HiveWhiteBoard, HiveSlimEventLoopMgr, HiveReadAlgorithm,ForwardSchedulerSvc, AlgResourcePool

# Output Levels
MessageSvc(OutputLevel=WARNING)
IncidentSvc(OutputLevel=DEBUG)
RootCnvSvc(OutputLevel=INFO)
SequencerTimerTool(OutputLevel=WARNING)

GaudiPersistency()

EventSelector(OutputLevel=DEBUG, PrintFreq=50, FirstEvent=1,
              Input = ["DATAFILE='PFN:HandleWB_ROOTIO.dst'  SVC='Gaudi::RootEvtSelector' OPT='READ'"])
FileCatalog(Catalogs = [ "xmlcatalog_file:HandleWB_ROOTIO.xml" ])

product_name="MyCollision"

loader = HiveReadAlgorithm("Loader",
                           OutputLevel=INFO,
                           NeededResources = ['ROOTIO','SOMETHINGELSE'],
                           Cardinality = 2 #framework should be able to fix this config problem
                           )

writer = WriteHandleAlg ("Writer",
                         Output="/Event/"+product_name,
                         UseHandle=True,
                         IsClonable=True)
                         
reader = ReadHandleAlg ("Reader",
                         Input=product_name,
                         IsClonable=True,
                         OutputLevel=INFO)

evtslots = 5
algoparallel = 10

whiteboard   = HiveWhiteBoard("EventDataSvc",
                              EventSlots = evtslots)

eventloopmgr = HiveSlimEventLoopMgr(OutputLevel=INFO)

scheduler = ForwardSchedulerSvc(MaxEventsInFlight = evtslots,
                                MaxAlgosInFlight = algoparallel,
                                OutputLevel=WARNING,
                                AlgosDependencies = [[],[product_name]])
                                
# Application setup
ApplicationMgr( TopAlg = [loader, reader],
                EvtMax   = -1,
                HistogramPersistency = "NONE",
                ExtSvc = [whiteboard],
                EventLoop = eventloopmgr)
