# -*- python -*-

import waflib.Logs as msg

PACKAGE = {
    'name': 'GaudiKernel',
    'author': ['Gaudi collaboration'],
}

def pkg_deps(ctx):
    ctx.use_pkg('GaudiPolicy')
    ctx.use_pkg('External/AtlasROOT')
    ctx.use_pkg('External/AtlasBoost')
    ctx.use_pkg('External/AtlasPOSIX')
    ctx.use_pkg('External/AtlasPython')
    ctx.use_pkg('External/AtlasTBB')
    return

def configure(ctx):
    msg.debug ('[configure] package name: '+PACKAGE['name'])

    return

def build(ctx):

    ctx.build_linklib(
        name = 'GaudiKernel',
        source = 'Lib/*.cpp',
        use = ['Reflex',
               'ROOT',
               'boost-thread', 'boost-date_time', 'boost-chrono',
               'boost-system', 'boost-filesystem',
               'tbb',],
        )

    o = ctx.build_app(
        name     = 'genconf',
        source   = 'Util/genconf.cpp',
        use      = ['GaudiKernel', 'Reflex',
                    'boost-thread', 'boost-date_time',
                    'boost-system', 'boost-filesystem', 'boost-program_options',
                    'boost',
                    'tbb',
                    ],
        do_test  = False,
        )
    ctx.env['GENCONF'] = 'genconf.exe'
    #ctx.add_group()
    

    ctx.build_pymodule(source=['python/GaudiKernel/*.py',],
                       # override default b/c python files
                       # already under 'PACKAGE_NAME' == 'GaudiKernel'
                       install_path_root='${INSTALL_AREA}/python')

    ctx.build_reflex_dict(
        name = 'GaudiKernel',
        source = 'dict/dictionary.h',
        selection_file = 'dict/dictionary.xml',
        use  = [
            'GaudiKernel',
            'Reflex',
            'boost',
            'pthread', 'rt',
            ],
        )

