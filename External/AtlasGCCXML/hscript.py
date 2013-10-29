# -*- python -*-

import os

import waflib.Utils
import waflib.Logs as msg

PACKAGE = {
    'name': 'External/AtlasGCCXML',
    'author': ['mana collaboration'],
}

def pkg_deps(ctx):
    # FIXME
    #ctx.use_pkg('External/AtlasCMake', private=True)    
    return

def options(ctx):
    ctx.load('find_gccxml')
    return

def configure(ctx):

    if not ctx.env.HWAF_FOUND_CXX_COMPILER:
        ctx.fatal('load a C++ compiler first')
        pass
    
    if not ctx.env.HWAF_FOUND_GCCXML:
        ctx.load('find_gccxml')
        ctx.find_gccxml()
        pass
    
    if not ctx.env.HWAF_FOUND_GCCXML:
        ctx.fatal('no hepwaf configuration for gccxml')
        pass

    return


def build(ctx):
    return