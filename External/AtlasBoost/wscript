# -*- python -*-
# @purpose: configuration of boost

import os

import waflib.Options
import waflib.Logs as msg
from waflib.Utils import subst_vars

PACKAGE = {
    'name': 'External/AtlasBoost',
    'author': ['mana collaboration'],
}

def pkg_deps(ctx):
    ctx.use_pkg('External/AtlasPython', public=True)
    

def options(ctx):
    ctx.load('find_boost')
    return

def configure(ctx):
    msg.debug ('[configure] package name: '+PACKAGE['name'])

    if not ctx.env.CXX:
        ctx.fatal('Load a C++ compiler first')

    if not ctx.env.HWAF_FOUND_PYTHON:
        ctx.fatal('Load a python environment first')
        pass

    if not ctx.env.HWAF_FOUND_BOOST:
        ctx.load('find_boost')
        ctx.find_boost()
        pass

    if not ctx.env.HWAF_FOUND_BOOST:
        ctx.fatal('Load a boost environment first')
        pass
    return

def build(ctx):
    return

def install(ctx):
    return
