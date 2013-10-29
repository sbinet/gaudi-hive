# -*- python -*-

import waflib.Logs as msg

PACKAGE = {
    'name': 'GaudiCommonSvc',
    'author': ['Gaudi collaboration'],
}

def pkg_deps(ctx):
    ctx.use_pkg('GaudiPolicy')
    ctx.use_pkg('GaudiKernel')

    ctx.use_pkg('External/AtlasAIDA')
    ctx.use_pkg('External/AtlasROOT') # reflex
    ctx.use_pkg('External/AtlasBoost')
    return

def configure(ctx):
    msg.debug ('[configure] package name: '+PACKAGE['name'])
    return

def build(ctx):
    ctx.build_complib(
        name = 'GaudiCommonSvc',
        source = '''\
        src/DataSvc/*.cpp
        src/HistogramSvc/*.cpp
        src/PersistencySvc/*.cpp
        src/*.cpp
        ''',
        use = ['GaudiKernel', 'Reflex', 'ROOT', 'AIDA',
               'boost-system', 'boost-filesystem',
               'boost-regex', 'boost-thread',
               ],
        )
    return


