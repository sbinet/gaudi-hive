# -*- python -*-

import waflib.Logs as msg

PACKAGE = {
    'name': 'GaudiAlg',
    'author': ['Gaudi collaboration'],
}

def pkg_deps(ctx):
    ctx.use_pkg('GaudiPolicy')

    ctx.use_pkg('GaudiKernel')
    ctx.use_pkg('GaudiUtils')

    ctx.use_pkg('External/AtlasAIDA')
    ctx.use_pkg('External/AtlasBoost')
    return

def configure(ctx):
    msg.debug ('[configure] package name: '+PACKAGE['name'])
    return

def build(ctx):

    ctx.build_linklib(
        name = 'GaudiAlgLib',
        source = 'lib/*.cpp',
        use = ['GaudiKernel',
               'GaudiUtilsLib',
               'AIDA',
               'boost',
               ]
        )

    ctx.build_complib(
        name = 'GaudiAlg',
        source = 'components/*.cpp',
        use  = ['GaudiKernel',
                'GaudiAlgLib',
                'AIDA',
                'boost',
                ]
        )

    return


