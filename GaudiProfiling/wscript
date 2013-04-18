# -*- python -*-

import waflib.Logs as msg

PACKAGE = {
    'name': 'GaudiProfiling',
    'author': ['Gaudi collaboration'],
}

def pkg_deps(ctx):
    ctx.use_pkg('GaudiPolicy')

    ctx.use_pkg('GaudiKernel')
    ctx.use_pkg('GaudiAlg')
    ctx.use_pkg('External/AtlasBoost')
    ctx.use_pkg('External/AtlasROOT')
    return

def configure(ctx):
    msg.debug ('[configure] package name: '+PACKAGE['name'])

    return

def build(ctx):

    # ctx.build_complib(
    #     name = 'GaudiProfiling',
    #     source = 'src/component/*.cpp',
    #     use = ['GaudiKernel',
    #            ],
    #     )

    # ctx.build_complib(
    #     name = 'GaudiGoogleProfiling',
    #     source = 'src/component/google/*.cpp',
    #     use = ['GaudiKernel',
    #            'GaudiAlg',
    #            'tcmalloc',
    #            ],
    #     )

    # ctx.build_complib(
    #     name = 'IntelProfiler',
    #     source = 'src/component/intel/*.cpp',
    #     use = ['GaudiKernel',
    #            ],
    #     )

    ctx.build_pymodule(source=['python/GaudiProfiling/*.py',],
                       # override default b/c python files
                       # already under 'PACKAGE_NAME' == 'GaudiProfiling'
                       install_path_root='${INSTALL_AREA}/python')
    
    ctx.install_scripts(source=[
        'scripts/*',
        ])
    
    ctx.build_app(
        name     = 'GaudiGenProfilingHtml',
        source   = 'src/app/pfm_gen_analysis.cpp',
        use      = ['GaudiKernel',
                    'z',
                    ],
        )

    return


