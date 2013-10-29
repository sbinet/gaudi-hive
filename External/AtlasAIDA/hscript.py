# -*- python -*-
# @purpose: configuration of aida

import waflib.Logs as msg

PACKAGE = {
    'name': 'External/AtlasAIDA',
    'author': ['mana collaboration'],
}

def pkg_deps(ctx):
    # no dep
    return

def options(opt):
    return

def configure(ctx):
    msg.debug ('[configure] package name: '+PACKAGE['name'])
    ctx.env['INCLUDES_AIDA'] = ctx.path.find_dir('inc').abspath()
    
    return

def build(ctx):
    ctx.install_headers(incdir='inc', relative_trick=False)
    return

def install(ctx):
    return
