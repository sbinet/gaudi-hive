# -*- python -*-

import waflib.Logs as msg

PACKAGE = {
    'name': 'GaudiMTTools',
    'author': ['Gaudi collaboration'],
}

def pkg_deps(ctx):
    ctx.use_pkg('GaudiPolicy')

    ctx.use_pkg('GaudiKernel')
    ctx.use_pkg('GaudiAlg')
    ctx.use_pkg('External/AtlasBoost')
    return

def configure(ctx):
    msg.debug ('[configure] package name: '+PACKAGE['name'])

    return

def build(ctx):

    ctx.build_complib(
        name = 'GaudiMTTools',
        source = 'src/*.cpp',
        use = ['GaudiKernel',
               'GaudiAlgLib',
               'boost',
               ],
        
        )
    return


