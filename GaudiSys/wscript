# -*- python -*-

import waflib.Logs as msg

PACKAGE = {
    'name': 'GaudiSys',
    'author': ['Gaudi collaboration'],
}

def pkg_deps(ctx):
    ctx.use_pkg('GaudiPolicy')

    ctx.use_pkg('GaudiKernel')
    ctx.use_pkg('GaudiCoreSvc')
    ctx.use_pkg('GaudiCommonSvc')
    ctx.use_pkg('GaudiAud')
    ctx.use_pkg('GaudiAlg')
    ctx.use_pkg('GaudiPython')  # Needed by gaudirun.py
    return

def configure(ctx):
    msg.debug ('[configure] package name: '+PACKAGE['name'])
    return

def build(ctx):
    return


