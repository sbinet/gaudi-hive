# -*- python -*-

import waflib.Logs as msg

PACKAGE = {
    'name': 'Gaudi',
    'author': ['Gaudi collaboration'],
}

def pkg_deps(ctx):
    ctx.use_pkg('GaudiPolicy')

    ctx.use_pkg('GaudiSys')

    ctx.use_pkg('External/AtlasBoost')
    ctx.use_pkg('External/AtlasPython')
    return

def configure(ctx):
    msg.debug ('[configure] package name: '+PACKAGE['name'])
    return

def build(ctx):

    ctx.build_app(
        name = 'Gaudi',
        source = 'src/main.cpp',
        use = [
            'GaudiKernel',
            'boost',
            ],
        )

    ctx.build_pymodule(source=['python/Gaudi/*.py',],
                       # override default b/c python files
                       # already under 'PACKAGE_NAME' == 'Gaudi'
                       install_path_root='${INSTALL_AREA}/python')

    ctx.install_scripts(source=[
        'scripts/*',
        ])

    ctx.hwaf_declare_runtime_alias("Gaudi", "Gaudi.exe")
    ctx.hwaf_declare_runtime_alias("GaudiRun", "gaudirun.py")
    ctx.hwaf_declare_runtime_alias("gaudirun", "gaudirun.py")
    ctx.hwaf_declare_runtime_alias("gaudipython", "python")
    return


