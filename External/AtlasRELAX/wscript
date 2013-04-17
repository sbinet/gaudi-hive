# -*- python -*-
# @purpose: configuration of relax

import waflib.Logs as msg

PACKAGE = {
    'name': 'relax',
    'author': ['mana collaboration'],
}

def pkg_deps(ctx):
    #FIXME
    ctx.use_pkg('External/AtlasROOT')
    #ctx.use_pkg('External/AtlasReflex')
    return

def options(opt):
    return

def configure(ctx):
    msg.debug ('[configure] package name: '+PACKAGE['name'])
    return

def build(ctx):

    ctx.build_reflex_dict(
        name = 'ReflexRflx',
        target = 'ReflexRflx',
        source = 'dict/ReflexDict.h',
        selection_file = 'dict/ReflexDict.xml',
        use = ['Reflex','ROOT']
        )

    ctx.build_reflex_dict(
        name = 'STLRflx',
        target = 'STLRflx',
        source = 'dict/STLDict.h',
        selection_file = 'dict/STLDict.xml',
        use = ['Reflex','ROOT']
        )

    ctx.build_reflex_dict(
        name = 'STLAddRflx',
        target = 'STLAddRflx',
        source = 'dict/STLAddDict.h',
        selection_file = 'dict/STLAddDict.xml',
        use = ['Reflex','ROOT']
        )

    return

#def install(ctx):
#    return
