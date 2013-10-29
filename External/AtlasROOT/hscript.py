# -*- python -*-
# @purpose: configuration of ROOT

import os

import waflib.Logs as msg
import waflib.Options
from waflib.Utils import subst_vars

PACKAGE = {
    'name': 'External/AtlasROOT',
    'author': ['mana collaboration'],
}

def pkg_deps(ctx):
    ctx.use_pkg('External/AtlasPython')
    ctx.use_pkg('External/AtlasGCCXML')
    #FIXME
    #ctx.use_pkg('External/AtlasXRootD')
    return

def options(ctx):
    ctx.load('find_root')
    return

def configure(ctx):
    msg.debug ('[configure] package name: '+PACKAGE['name'])

    if not ctx.env.CXX:
        ctx.fatal('load a C++ compiler first')
        pass

    if not ctx.env.HWAF_FOUND_ROOT:
        ctx.load('find_root')
        ctx.find_root()
        pass
    
    if not ctx.env.HWAF_FOUND_ROOT:
        ctx.fatal('no hepwaf configuration for ROOT')
        pass
    
    return

def build(ctx):
    return

#def install(ctx):
#    return
