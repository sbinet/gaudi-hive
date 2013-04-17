# -*- python -*-
# @purpose: configuration for binutils

PACKAGE = {
    'name': 'binutils',
    'author': ['mana collaboration'],
}

def pkg_deps(ctx):
    ctx.use_pkg('GaudiPolicy')
    ctx.use_pkg('External/AtlasPOSIX')
    return

def options(opt):
    
    return

def configure(ctx):
    if not ctx.env.CXX:
        ctx.fatal('Load a C++ compiler first')
        pass

    if not ctx.env.HWAF_FOUND_POSIXLIBS:
        ctx.fatal('Load a posix environment first')
        pass

    return

def build(ctx):
    return

def install(ctx):
    return
