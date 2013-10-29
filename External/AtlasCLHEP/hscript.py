# -*- python -*-

import os

import waflib.Logs as msg
import waflib.Utils
from waflib.Utils import subst_vars

PACKAGE = {
    'name': 'External/AtlasCLHEP',
    'author': ['mana collaboration'],
}

def pkg_deps(ctx):
    ctx.use_pkg('GaudiPolicy')
    return
    

def options(ctx):
    ctx.load('find_clhep')
    return

def configure(ctx):
    msg.debug ('[configure] package name: '+PACKAGE['name'])

    if not ctx.env.CXX:
        msg.fatal('load a c++ compiler first')
        pass

    if not ctx.env.HWAF_FOUND_CLHEP:
        ctx.load('find_clhep')
        ctx.find_clhep()
        pass
    
    if not ctx.env.HWAF_FOUND_CLHEP:
        msg.fatal('load a CLHEP environment first')
        pass
    
    return

def build(ctx):
    return
