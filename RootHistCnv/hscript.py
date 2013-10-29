# -*- python -*-

import waflib.Logs as msg

PACKAGE = {
    'name': 'RootHistCnv',
    'author': ['Gaudi collaboration'],
}

def pkg_deps(ctx):
    ctx.use_pkg('GaudiPolicy')
    ctx.use_pkg('GaudiKernel')

    ctx.use_pkg('External/AtlasAIDA')
    ctx.use_pkg('External/AtlasROOT')
    return

def configure(ctx):
    msg.debug ('[configure] package name: '+PACKAGE['name'])
    return

def build(ctx):

    ctx.build_complib(
        name = 'RootHistCnv',
        source = 'src/*.cpp',
        use = [
            'GaudiKernel',
            'AIDA',
            'ROOT',
            ],
        )

    return

