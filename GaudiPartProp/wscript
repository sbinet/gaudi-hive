# -*- python -*-

import waflib.Logs as msg

PACKAGE = {
    'name': 'GaudiPartProp',
    'author': ['Gaudi collaboration'],
}

def pkg_deps(ctx):
    ctx.use_pkg('GaudiPolicy')

    ctx.use_pkg('GaudiKernel')
    return

def configure(ctx):
    msg.debug ('[configure] package name: '+PACKAGE['name'])

    return

def build(ctx):

    ctx.build_complib(
        name = 'GaudiPartProp',
        source = 'src/*.cpp',
        use = ['GaudiKernel',
               ],
        )
    return


