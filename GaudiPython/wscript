# -*- python -*-

import waflib.Logs as msg

PACKAGE = {
    'name': 'GaudiPython',
    'author': ['Gaudi collaboration'],
}

def pkg_deps(ctx):
    ctx.use_pkg('GaudiPolicy')
    ctx.use_pkg('GaudiKernel')
    ctx.use_pkg('GaudiAlg')
    ctx.use_pkg('GaudiUtils')

    ctx.use_pkg('External/AtlasCLHEP')
    ctx.use_pkg('External/AtlasAIDA')
    ctx.use_pkg('External/AtlasROOT') # reflex
    ctx.use_pkg('External/AtlasPython')
    return

def configure(ctx):
    msg.debug ('[configure] package name: '+PACKAGE['name'])
    return

def build(ctx):

    ctx.build_linklib(
        name = 'GaudiPythonLib',
        source = 'Lib/*.cpp',
        use = ['GaudiKernel',
               'GaudiAlgLib',
               'GaudiUtilsLib',
               'CLHEP',
               'AIDA',
               'ROOT',
               'python',
               ]
        )

    ctx.build_complib(
        name = 'GaudiPython',
        source = 'Services/*.cpp',
        use  = ['GaudiKernel',
                'GaudiAlgLib',
                'GaudiUtilsLib',
                'GaudiPythonLib',
                'CLHEP',
                'Reflex',
                'AIDA',
                'python',
                ]
        )

    ctx.build_reflex_dict(
        name = 'GaudiPython',
        source = 'dict/kernel.h',
        selection_file = 'dict/selection_kernel.xml',
        use  = [
            'GaudiAlgLib',
            'GaudiUtilsLib',
            'GaudiPythonLib',
            'CLHEP',
            'Reflex',
            'AIDA',
            'python',
            ],
        #lib = ['GaudiAlgLib', 'GaudiUtilsLib', 'GaudiPythonLib',]
        )

    ctx.build_pymodule(
        source=['python/GaudiPython/*.py',],
        # override default b/c python files
        # already under 'PACKAGE_NAME' == 'GaudiPython'
        install_path_root='${INSTALL_AREA}/python')

    # ctx.build_pymodule(
    #     source = [#'python/*.py',
    #               'python/GaudiPython/*.py',]
    #     )
    return


