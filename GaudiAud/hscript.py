# -*- python -*-

import waflib.Logs as msg

PACKAGE = {
    'name': 'GaudiAud',
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
        name = 'GaudiAud',
        source = '*.cpp',
        use = ['GaudiKernel',
               #'ROOT',
               #'boost-thread', 'boost-date_time',
               #'boost-system', 'boost-filesystem',
               ],
        )

