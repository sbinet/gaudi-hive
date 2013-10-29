# -*- python -*-
# @purpose: configuration of python

import waflib.Logs as msg

PACKAGE = {
    'name': 'External/AtlasPython',
    'author': ['mana collaboration'],
}

def pkg_deps(ctx):
    return

def options(ctx):
    ctx.load('find_python')

def configure(ctx):
    msg.debug ('[configure] package name: '+PACKAGE['name'])

    if not ctx.env.CXX:
        ctx.fatal('Load a C++ compiler first')
        pass

    if not ctx.env.HWAF_FOUND_PYTHON:
        ctx.load('find_python')
        ctx.find_python()
        pass
    
    # disable the creation of .pyo files
    ctx.env['PYO'] = 0

    return

def build(ctx):
    ctx.symlink_as('${INSTALL_AREA}/bin/python', ctx.env['PYTHON'][0])
    return

def install(ctx):
    return
