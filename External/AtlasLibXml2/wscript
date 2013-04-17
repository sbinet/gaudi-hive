# -*- python -*-
# @purpose: configuration of libXML2

import os

import waflib.Logs as msg
import waflib.Options
from waflib.Utils import subst_vars

PACKAGE = {
    'name': 'External/AtlasLibXml2',
    'author': ['mana collaboration'],
}

def pkg_deps(ctx):
    #ctx.use_pkg('External/AtlasGCCXML')
    return

def options(ctx):
    return

def configure(ctx):
    msg.debug ('[configure] package name: '+PACKAGE['name'])

    if not ctx.env.CXX:
        msg.fatal('load a C++ compiler first')
        pass
    
    if not ctx.env.HWAF_FOUND_LIBXML2:
        ctx.load('find_libxml2')
        ctx.find_libxml2()
    return

def build(ctx):
    return

#def install(ctx):
#    return
