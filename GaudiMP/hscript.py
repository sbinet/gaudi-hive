# -*- python -*-

import waflib.Logs as msg

PACKAGE = {
    'name': 'GaudiMP',
    'author': ['gaudi collaboration'],
}

def pkg_deps(ctx):
    ctx.use_pkg('GaudiPolicy')
    ctx.use_pkg('GaudiKernel')
    ctx.use_pkg('GaudiPython')

    ctx.use_pkg('External/AtlasPython')
    ctx.use_pkg('External/AtlasROOT')
    return

def configure(ctx):
    msg.debug ('[configure] package name: '+PACKAGE['name'])
    return

def build(ctx):

    ctx.build_complib(
        name = 'GaudiMP',
        source = 'Lib/*.cpp',
        use = ['GaudiKernel', 'GaudiPython',
               'Reflex', 'ROOT',
               'python',
               ],
        includes = ['.'],
        )

    ctx.build_reflex_dict(
        name = 'GaudiMP',
        source = 'dict/gaudimp_dict.h',
        selection_file = 'dict/selection.xml',
        use = ['complib-GaudiMP',
               'GaudiKernel', 'GaudiPython',
               'Reflex', 'ROOT',
               'python',
               ]
        )
    

    ctx.install_headers()
    ctx.build_pymodule(
        source=['python/GaudiMP/*.py',],
        # override default b/c python files
        # already under 'PACKAGE_NAME' == 'GaudiMP'
        install_path_root='${INSTALL_AREA}/python')

    # ctx.build_pymodule(
    #     source = [#'python/*.py',
    #               'python/GaudiMP/*.py',]
    #     )

    return

### EOF ###
