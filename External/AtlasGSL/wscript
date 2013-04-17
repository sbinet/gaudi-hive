# -*- python -*-

import os

import waflib.Logs as msg
import waflib.Utils
from waflib.Utils import subst_vars

PACKAGE = {
    'name': 'External/AtlasGSL',
    'author': ['gaudi collaboration'],
}

def pkg_deps(ctx):
    ctx.use_pkg('GaudiPolicy')
    return
    

def options(ctx):
    return

def configure(ctx):
    msg.debug ('[configure] package name: '+PACKAGE['name'])

    if not ctx.env.CXX:
        msg.fatal('load a c++ compiler first')
        pass

    if not ctx.env.HWAF_FOUND_GSL:
        ctx.load('find_gsl')
        ctx.find_gsl()
        pass
    
    if not ctx.env.HWAF_FOUND_GSL:
        msg.fatal('load a GSL environment first')
        pass
    
    return

def build(ctx):
    return
