# -*- python -*-
# @purpose: configuration of various posix libraries

PACKAGE = {
    'name': 'External/AtlasPOSIX',
    'author': ['mana collaboration'],
}

def pkg_deps(ctx):
    ctx.use_pkg('GaudiPolicy')
    return

def options(opt):
    
    return

def configure(ctx):
    if not ctx.env.CXX:
        ctx.fatal('Load a C++ compiler first')
        pass

    if not ctx.env.HWAF_FOUND_POSIXLIBS:
        ctx.load('find_posixlibs')
        ctx.find_posixlibs()
        pass
    if not ctx.env.HWAF_FOUND_POSIXLIBS:
        ctx.fatal('Load a posix environment first')
        pass
    return

def build(ctx):
    return

def install(ctx):
    return
