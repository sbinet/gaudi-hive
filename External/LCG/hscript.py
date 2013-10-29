# -*- python -*-
# @purpose: configuration of LCG libraries

PACKAGE = {
    'name': 'External/LCG',
    'author': ['gaudi collaboration'],
}

def pkg_deps(ctx):
    ctx.use_pkg('GaudiPolicy')
    return

def options(ctx):
    ctx.load('find_lcg')
    return

def configure(ctx):
    if not ctx.env.CXX:
        ctx.fatal('Load a C++ compiler first')
        pass

    if not ctx.env.HWAF_FOUND_LCG:
        ctx.load('find_lcg')
        ctx.find_lcg()
        pass
    if not ctx.env.HWAF_FOUND_LCG:
        ctx.fatal('Load a LCG environment first')
        pass
    return

def build(ctx):
    return

def install(ctx):
    return
