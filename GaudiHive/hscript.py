# -*- python -*-

import waflib.Logs as msg

PACKAGE = {
    'name': 'GaudiHive',
    'author': ['Gaudi collaboration'],
}

def pkg_deps(ctx):
    ctx.use_pkg('GaudiPolicy')

    ctx.use_pkg('GaudiKernel')
    ctx.use_pkg('GaudiAlg')

    ctx.use_pkg('External/AtlasAIDA')
    ctx.use_pkg('External/AtlasBoost')
    ctx.use_pkg('External/AtlasROOT')
    ctx.use_pkg('External/AtlasTBB')
    return

def configure(ctx):
    msg.debug ('[configure] package name: '+PACKAGE['name'])
    return

def build(ctx):

    ctx.build_complib(
        name = 'GaudiHive',
        source = 'src/*.cpp',
        use = ['GaudiKernel',
               'GaudiAlgLib',
               'AIDA',
               'boost',
               'ROOT',
               'tbb',
               ]
        )

    ctx.install_joboptions(
        source=[
            'options/*',
            ],
        cwd='options',
        )

    ctx.build_app(
        name = 'concurrentRun',
        source = 'src/bin/concurrentRun.cpp',
        use = [
            'GaudiKernel',
            'boost',
            ],
        )

    return


