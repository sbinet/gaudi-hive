# -*- python -*-
# @purpose: configuration of uuid

import os

import waflib.Logs as msg
import waflib.Utils
from waflib.Utils import subst_vars

PACKAGE = {
    'name': 'External/AtlasUUID',
    'author': ['mana collaboration'],
}

def pkg_deps(ctx):
    return

def options(ctx):
    return

def configure(ctx):
    if not ctx.env.CXX:
        ctx.fatal('Load a C++ compiler first')
        pass

    if not ctx.env.HWAF_FOUND_UUID:
        ctx.load('find_uuid')
        ctx.find_uuid()
        
    if not ctx.env.HWAF_FOUND_UUID:
        ctx.fatal('Load a UUID environment first')
        pass
    return

def build(ctx):
    return

def install(ctx):
    return
