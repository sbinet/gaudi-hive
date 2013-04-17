# -*- python -*-

import waflib.Logs as msg

PACKAGE = {
    'name': 'GaudiUtils',
    'author': ['Gaudi collaboration'],
}

def pkg_deps(ctx):
    ctx.use_pkg('GaudiPolicy')
    ctx.use_pkg('GaudiKernel')

    ctx.use_pkg('External/AtlasAIDA')
    ctx.use_pkg('External/AtlasBoost')
    return

def configure(ctx):
    msg.debug ('[configure] package name: '+PACKAGE['name'])
    return

def build(ctx):

    ctx.build_linklib(
        name = 'GaudiUtilsLib',
        source = '''\
        Lib/*.cpp
        ''',
        use = ['GaudiKernel',
               'AIDA',
               'boost',
               ]
        )

    ctx.build_complib(
        name = 'GaudiUtils',
        source = '''
        component/IODataManager.cpp
        component/SignalMonitorSvc.cpp
        component/StalledEventMonitor.cpp
        ''',
        # FIXME: need xercesc...
        #component/XMLCatalogTest.cpp
        #component/XMLFileCatalog.cpp
        #component/MultiFileCatalog.cpp
        use  = ['GaudiKernel',
                'GaudiUtilsLib',
                'AIDA',
                'boost',
                ]
        )

    return


