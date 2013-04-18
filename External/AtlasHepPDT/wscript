# -*- python -*-

import os

import waflib.Logs as msg
import waflib.Utils
from waflib.Utils import subst_vars

PACKAGE = {
    'name': 'External/AtlasHepPDT',
    'author': ['gaudi collaboration'],
}

def pkg_deps(ctx):
    ctx.use_pkg('GaudiPolicy')
    return
    

def options(ctx):
    ctx.load('find_heppdt')
    return

def configure(ctx):
    msg.debug ('[configure] package name: '+PACKAGE['name'])

    if not ctx.env.CXX:
        msg.fatal('load a c++ compiler first')
        pass

    if not ctx.env.HWAF_FOUND_HEPPDT:
        ctx.load('find_heppdt')
        ctx.find_heppdt()
        pass
    
    if not ctx.env.HWAF_FOUND_HEPPDT:
        msg.fatal('load a HepPDT environment first')
        pass
    
    return

def build(ctx):
    return
