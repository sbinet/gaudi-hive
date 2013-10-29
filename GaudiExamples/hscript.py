# -*- python -*-

import waflib.Logs as msg

PACKAGE = {
    'name': 'GaudiExamples',
    'author': ['Gaudi collaboration'],
}

def pkg_deps(ctx):
    ctx.use_pkg('GaudiPolicy')

    ctx.use_pkg('Gaudi')
    ctx.use_pkg('RootCnv')
    ctx.use_pkg('RootHistCnv')
    
    ctx.use_pkg('External/AtlasAIDA')
    ctx.use_pkg('External/AtlasBoost')
    ctx.use_pkg('External/AtlasCLHEP')
    ctx.use_pkg('External/AtlasGSL')
    ctx.use_pkg('External/AtlasHepPDT')
    ctx.use_pkg('External/AtlasPython')
    ctx.use_pkg('External/AtlasROOT')
    return

def configure(ctx):
    msg.debug ('[configure] package name: '+PACKAGE['name'])
    return

def build(ctx):

    ctx.build_linklib(
        name = 'GaudiExamplesLib',
        source = 'src/Lib/*.cpp',
        includes = 'src/Lib',
        use = ['GaudiKernel',
               'CLHEP',
               ]
        )
    
    ctx.build_complib(
        name = 'GaudiExamples',
        source = [
            'src/AbortEvent/*.cpp',
            'src/AlgSequencer/*.cpp',
            'src/AlgTools/*.cpp',
            'src/DataOnDemand/*.cpp',
            'src/AlgErrAud/*.cpp',
            'src/GSLTools/*.cpp',
            'src/RandomNumber/*.cpp',
            'src/Histograms/*.cpp',
            'src/NTuples/*.cpp',
            'src/TupleEx/*.cpp',
            'src/CounterEx/*.cpp',
            'src/PartProp/*.cpp',
            'src/Properties/*.cpp',
            'src/ExtendedProperties/*.cpp',
            #'src/POOLIO/*.cpp', ################### fixme: needs POOL
            'src/ColorMsg/ColorMsgAlg.cpp',
            'src/History/History.cpp',
            'src/THist/*.cpp',
            'src/ErrorLog/ErrorLogTest.cpp',
            'src/EvtColsEx/EvtColAlg.cpp',
            'src/Maps/*.cpp',
            'src/MultipleLogStreams/*.cpp',
            'src/GaudiCommonTests/*.cpp',
            'src/IncidentSvc/*.cpp',
            'src/bug_34121/*.cpp',
            'src/Auditors/*.cpp',
            'src/Timing/*.cpp',
            'src/Selections/*.cpp',
            'src/SvcInitLoop/*.cpp',
            'src/StringKeys/*.cpp',
            'src/StatusCodeSvc/*.cpp',
            'src/testing/*.cpp',
            'src/IntelProfiler/*.cpp',
            #'src/Dll/GaudiExamples*.cpp',
        ],
        includes = 'src/Lib',
        use = [
            'GaudiKernel',
            'GaudiExamplesLib',
            'GaudiAlgLib',
            'GaudiGSLLib',
            'GaudiUtils',
            'boost',
            'python',
            'HepPDT',
            'ROOT',
            ],
        )

    ## FIXME: needs POOL
    # ctx.build_reflex_dict(
    #     name = 'GaudiExamples',
    #     source = 'src/POOLIO/dict.h',
    #     selection_file = 'src/POOLIO/dict.xml',
    #     use  = [
    #         'GaudiKernel',
    #         'Reflex',
    #         'POOL',
    #         ],
    #     )
    

    ctx.build_pymodule(source=['python/GaudiExamples/*.py',],
                       # override default b/c python files
                       # already under 'PACKAGE_NAME' == 'GaudiExamples'
                       install_path_root='${INSTALL_AREA}/python')

    ctx.install_joboptions(
        source=[
            'options/*',
            ],
        cwd='options',
        )


    ctx.build_app(
        name = 'Allocator',
        source = 'src/Allocator/*.cpp',
        use = 'GaudiExamplesLib',
        includes = 'src/Lib',
        )
    return

