# -*- python -*-

import waflib.Logs as msg

PACKAGE = {
    'name': 'GaudiSvc',
    'author': ['Gaudi collaboration'],
}

def pkg_deps(ctx):
    ctx.use_pkg('GaudiPolicy')
    ctx.use_pkg('GaudiKernel')

    ctx.use_pkg('External/AtlasAIDA')
    ctx.use_pkg('External/AtlasROOT') # reflex
    ctx.use_pkg('External/AtlasCLHEP')
    ctx.use_pkg('External/AtlasBoost')
    return

def configure(ctx):
    msg.debug ('[configure] package name: '+PACKAGE['name'])
    return

def build(ctx):
    ctx.build_complib(
        name = 'GaudiSvc',
        source = '''\
           AlgContextSvc/*.cpp
           ApplicationMgr/*.cpp
           AuditorSvc/*.cpp
           ChronoStatSvc/*.cpp
           EventSelector/*.cpp
           ExceptionSvc/*.cpp
           DataSvc/*.cpp
           DetectorDataSvc/*.cpp
           HistogramSvc/*.cpp
           HistorySvc/*.cpp
           IncidentSvc/*.cpp
           IssueLogger/*.cpp
           JobOptionsSvc/*.cpp
           MessageSvc/*.cpp
           NTupleSvc/*.cpp
           ParticlePropertySvc/*.cpp
           PersistencySvc/*.cpp
           RndmGenSvc/*.cpp
           StatusCodeSvc/*.cpp
           ToolSvc/*.cpp
           THistSvc/*.cpp
           FastContainersSvc/*.cpp
           VFSSvc/*.cpp
           Dll/GaudiSvc*.cpp
           ''',
        use = ['GaudiKernel', 'Reflex', 'ROOT', 'AIDA', 'CLHEP',
               'boost-system', 'boost-filesystem',
               'boost-regex', 'boost-thread',
               ],
        )
    return


