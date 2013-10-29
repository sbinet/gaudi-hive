# -*- python -*-

import os

import waflib.Logs as msg
import waflib.Utils
from waflib.Utils import subst_vars

PACKAGE = {
    'name': 'External/AtlasTBB',
    'author': ['mana collaboration'],
}

def pkg_deps(ctx):
    return
    

def options(ctx):
    ctx.load('find_tbb')
    return

def configure(ctx):
    msg.debug ('[configure] package name: '+PACKAGE['name'])

    if not ctx.env.CXX:
        msg.fatal('load a c++ compiler first')
        pass

    if not ctx.env.HWAF_FOUND_TBB:
        ctx.load('find_tbb')
        ctx.find_tbb()
        pass
    
    if not ctx.env.HWAF_FOUND_TBB:
        msg.fatal('load a TBB environment first')
        pass
    
    return

def build(ctx):
    return
