# -*- python -*-

import waflib.Logs as msg

PACKAGE = {
    'name': 'GaudiGSL',
    'author': ['Gaudi collaboration'],
}

def pkg_deps(ctx):
    ctx.use_pkg('GaudiPolicy')

    ctx.use_pkg('GaudiKernel')
    ctx.use_pkg('GaudiAlg')

    ctx.use_pkg('External/AtlasAIDA')
    ctx.use_pkg('External/AtlasCLHEP')
    ctx.use_pkg('External/AtlasGSL')
    return

def configure(ctx):
    msg.debug ('[configure] package name: '+PACKAGE['name'])

    return

def build(ctx):

    ctx.build_linklib(
        name = 'GaudiGSLLib',
        source = 'src/Lib/*.cpp',
        use = ['GaudiKernel',
               'GaudiAlgLib',
               'AIDA', 'CLHEP-GenericFunctions',
               'gsl',
               ],
        
        )
    ctx.install_headers('GaudiMath')
    
    ctx.build_complib(
        name = 'GaudiGSL',
        source = 'src/Components/*.cpp',
        use = ['GaudiKernel',
               'GaudiGSLLib',
               'AIDA', 'CLHEP-GenericFunctions',
               'gsl',
               ],
        )

    ctx.build_reflex_dict(
        name = 'GaudiGSLMath',
        source = 'dict/GaudiGSLMath.h',
        selection_file = 'dict/GaudiGSLMath.xml',
        use  = [
            'GaudiGSLLib',
            'Reflex',
            'pthread', 'rt',
            ],
        )
    return


