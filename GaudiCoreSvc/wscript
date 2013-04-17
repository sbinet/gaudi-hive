# -*- python -*-

import waflib.Logs as msg

PACKAGE = {
    'name': 'GaudiCoreSvc',
    'author': ['Gaudi collaboration'],
}

def pkg_deps(ctx):
    ctx.use_pkg('GaudiPolicy')
    ctx.use_pkg('GaudiKernel')
    ctx.use_pkg('External/AtlasBoost')
    return

def configure(ctx):
    msg.debug ('[configure] package name: '+PACKAGE['name'])
    return

def build(ctx):

    ctx.build_complib(
        name = 'GaudiCoreSvc',
        source = [
            'src/ApplicationMgr/*.cpp',
            'src/EventSelector/*.cpp',
            'src/IncidentSvc/*.cpp',
            'src/JobOptionsSvc/*.cpp',
            'src/MessageSvc/*.cpp',
            ],
        use = [
            'GaudiKernel',
            'python',
            'boost', 'boost-python',
            ],
        )

    return


