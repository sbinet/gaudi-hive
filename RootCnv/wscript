# -*- python -*-

import waflib.Logs as msg

PACKAGE = {
    'name': 'RootCnv',
    'author': ['Gaudi collaboration'],
}

def pkg_deps(ctx):
    ctx.use_pkg('GaudiPolicy')
    ctx.use_pkg('GaudiKernel')
    ctx.use_pkg('GaudiUtils')

    ctx.use_pkg('External/AtlasROOT')
    return

def configure(ctx):
    msg.debug ('[configure] package name: '+PACKAGE['name'])
    return

def build(ctx):

    ## FIXME: we need POOL...
    if 1:
        return
    
    root_linkopts = ['ROOT', 'Cintex', 'TreePlayer', 'MathMore']

    ctx.build_linklib(
        name = 'RootCnvLib',
        source = '''\
           src/*.cpp
           ''',
        use = [
            'GaudiKernel',
            'GaudiUtils',
            ] + root_linkopts,
        defines = ['__POOL_COMPATIBILITY'],
        )

    ctx.build_complib(
        name = 'RootCnv',
        source = '''components/*.cpp''',
        use = [
            'GaudiKernel',
            'GaudiUtils',
            'RootCnvLib',
            ] + root_linkopts,
        defines = ['__POOL_COMPATIBILITY'],
        )

    ctx.build_app(
        name = 'gaudi_merge',
        source = 'merge/merge.cpp',
        use = ['RootCnvLib', ] + root_linkopts,
        )
    
    ctx.build_reflex_dict(
        name = 'RootCnv',
        source = 'dict/RootCnv_dict.h',
        selection_file = 'dict/RootCnv_dict.xml',
        use  = [
            'GaudiKernel',
            'Reflex',
            ],
        )

    return


