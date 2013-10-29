# -*- python -*-

import waflib.Logs as msg

PACKAGE = {
    'name': 'PartPropSvc',
    'author': ['Gaudi collaboration'],
}

def pkg_deps(ctx):
    ctx.use_pkg('GaudiPolicy')
    ctx.use_pkg('GaudiKernel')

    ctx.use_pkg('External/AtlasHepPDT')
    return

def configure(ctx):
    msg.debug ('[configure] package name: '+PACKAGE['name'])
    return

def build(ctx):
    ctx.build_complib(
        name = 'PartPropSvc',
        source = '''\
           src/*.cpp
           ''',
        use = [
            'GaudiKernel',
            'HepPDT',
            ],
        )
    ctx.install_joboptions(source=['share/*.py', 'share/*.txt'])
    ctx.install_data(source=['share/PDGTABLE', 'share/PDGTABLE.MeV'])
    return


