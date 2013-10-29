# -*- python -*-

## stdlib imports
import os
import os.path as osp
import sys

## waf imports
import waflib.Logs as msg
import waflib.Utils
import waflib.Configure
import waflib.Build
import waflib.Task
import waflib.Tools.ccroot
from waflib.Configure import conf
from waflib.TaskGen import feature, before_method, after_method, extension, after

PACKAGE = {
    'name': 'GaudiPolicy',
    'author': ['gaudi collaboration'],
}

def pkg_deps(ctx):
    return

def options(ctx):
    ctx.load('find_compiler')
    return

def configure(ctx):
    msg.debug ('[configure] package name: '+PACKAGE['name'])
    # register this module for export
    ctx.hwaf_export_module("wscript")

    ctx.load('find_compiler')
    ctx.find_cxx_compiler()
    
    if not ctx.env.HWAF_FOUND_PYTHON:
        ctx.load('find_python')
        ctx.find_python()
        pass
    ctx.load('python')

    ctx.env.GENCONF = 'genconf.exe'
    ctx.env.GENCONF_CONFIGURABLE_MODULE = 'GaudiKernel'
    
    if ctx.is_darwin():
        # we really want .so and not .dylib...
        for shlib in ['cshlib', 'cxxshlib']:
            linkflags = ctx.env['LINKFLAGS_%s'%shlib][:]
            ctx.env['LINKFLAGS_%s'%shlib] = [l.replace('-dynamiclib','-shared')
                                             for l in linkflags]
            ctx.env['%s_PATTERN'%shlib]      = 'lib%s.so'

        # and no stinking current_version either
        for flag in ['CXXFLAGS_cxxshlib','CFLAGS_cshlib']:
            _flags = ctx.env[flag][:]
            if '-compatibility_version' in _flags:
                _idx = _flags.index('-compatibility_version')
                # +2 b/c it is of the form: ['-compatibility_version','1',...]
                ctx.env[flag] = _flags[:_idx]+_flags[_idx+2:]
            _flags = ctx.env[flag][:]
            if '-current_version' in _flags:
                _idx = _flags.index('-current_version')
                # +2 b/c it is of the form: ['-current_version','1',...]
                ctx.env[flag] = _flags[:_idx]+_flags[_idx+2:]
        
    # preprocessor ---
    ctx.env.append_unique(
        'DEFINES',
        ['DISABLE_ALLOC',
         'HAVE_NEW_IOSTREAMS',
         '_GNU_SOURCE',
         'GAUDI_V20_COMPAT',
         # FIXME: only meaningful for slc6-gcc4x...
         '__USE_XOPEN2K8'
         ]
        )
    if ctx.is_opt():
        ctx.env.append_unique(
            'DEFINES',
            ['NDEBUG=1',
             ]
            )
    import sys
    if ctx.is_linux():
        ctx.env.append_unique('DEFINES', ['linux'])

    def subst(v):
        return waflib.Utils.subst_vars(v, ctx.env)
    
    # C compiler flags -----------------------------------------------
    if ctx.is_windows():
        # dummy
        pass
    else:
        ctx.env.append_value(
            'COMMONFLAGS',
            ['-O2', '-fPIC',
             '-pipe', '-ansi', '-Wall', '-W', '-pthread'])

        if ctx.is_dbg():
            ctx.env.append_value('COMMONFLAGS', ['-g'])

        if ctx.is_32b():
            ctx.env.append_value('COMMONFLAGS', ['-m32'])
        else:
            ctx.env.append_value('COMMONFLAGS', ['-m64'])

        ctx.env.append_unique('CCFLAGS', subst('${COMMONFLAGS}').split())
        ctx.env.append_unique('CFLAGS', subst('${COMMONFLAGS}').split())

        # C++ compiler flags ---------------------------------------------
        ctx.env.append_unique('CXXFLAGS', subst('${COMMONFLAGS}').split())
        ctx.env.append_unique(
            'CXXFLAGS',
            ['-std=c++0x',
             '-Wno-deprecated',
             ]
            )

        if ctx.is_darwin():
            ctx.env.append_unique(
                'CXXFLAGS',
                ['-Wno-non-virtual-dtor',
                 '-Wno-long-long',
                 '-Wwrite-strings',
                 '-Wpointer-arith',
                 '-Woverloaded-virtual',
                 '-ftemplate-depth-512',
                 '-fmessage-length=0',
                 ]
                )
        # Fortran compiler flags -----------------------------------------
        ctx.env.append_unique('FCFLAGS', subst('${COMMONFLAGS}').split())

        # link flags
        if ctx.is_dbg():
            ctx.env.append_unique('LINKFLAGS', ['-g',])
        if ctx.is_32b():
            ctx.env.append_unique('LINKFLAGS', ['-m32',])
        else:
            ctx.env.append_unique('LINKFLAGS', ['-m64',])

    # shared library link flags
    if ctx.is_dbg() and not ctx.is_windows():
        ctx.env.append_unique('SHLINKFLAGS', ['-g'])

    if ctx.is_linux():
        ctx.env.append_unique(
            'SHLINKFLAGS',
            ['-Wl,--hash-style=both',
             '-Wl,--as-needed',
             #'-Wl,--no-undefined',
             '-ldl'
             ]
            )
    elif ctx.is_darwin():
        ctx.env.append_unique(
            'SHLINKFLAGS',
            ['-Wl,-dead_strip_dylibs',
             #'-Wl,--as-needed',
             #'-Wl,--no-undefined',
             # darwin linker doesn't know about --hash-style=both
             #'-Wl,--hash-style=both', 
             '-ldl'
             ]
            )
    elif ctx.is_windows():
        #FIXME: what should the defaults be ?
        ctx.env.append_unique('SHLINKFLAGS', [])
        msg.warn('**FIXME**: dummy SHLINKFLAGS value for windows')

    else:
        raise RuntimeError('unhandled platform [%s]' % sys.platform)
    
    if ctx.is_64b() and ctx.is_linux():
        ctx.env.append_unique(
            'SHLINKFLAGS',            
            [
                # align at 4096b boundaries instead of 1Mb
                '-Wl,-z,max-page-size=0x1000',
                ]
            )
        
    # LDFLAGS: options for the linker
    # LIBS: -l options (library names) to pass to the linker
    
    # library path
    import os
    if ctx.is_linux():
        if ctx.is_64b():
            ctx.env.append_unique(
                'LIBPATH',
                [
                    # no need: implicitly taken from ldconfig...
                    #'/usr/lib64',
                 ]
                )
        else:
            ctx.env.append_unique(
                'LIBPATH',
                ['/usr/lib',
                 ]
                )
            pass
        pass
    elif ctx.is_darwin():
        ctx.env.append_unique(
            'LIBPATH',
            ['/usr/lib',
             ]
            )
        pass
    
    if 'LD_LIBRARY_PATH' in os.environ:
        ll = []
        for l in os.getenv('LD_LIBRARY_PATH','.').split(os.pathsep):
            if l: ll.append(l)
            else: ll.append('.')
        ctx.env.append_unique(
            'LD_LIBRARY_PATH', 
            ll
            )
        del ll
        
    if ctx.is_darwin():
        ll = []
        for l in os.getenv('LD_LIBRARY_PATH','.').split(os.pathsep):
            # this can confuse macports...
            if not l.startswith(('/usr','/opt/local')):
                if l: ll.append(l)
                else: ll.append('.')
        ctx.env.append_unique('DYLD_LIBRARY_PATH',
                              ll)
        del ll
        pass

    ctx.hwaf_declare_runtime_env('JOBOPTSEARCHPATH')
    ctx.hwaf_declare_runtime_env('DATAPATH')
    ctx.hwaf_declare_runtime_env('XMLPATH')

def build(ctx):
    return

### -----------------------------------------------------------------------------
import sys
import waflib.Build
class InstallContext(waflib.Build.InstallContext):
    def __init__(self, **kw):
        super(InstallContext, self).__init__(**kw)
        return

    def execute_build(self):
        self.logger = msg
        lvl = msg.log.level
        if lvl < msg.logging.ERROR:
            msg.log.setLevel(msg.logging.ERROR)
            pass
        try:
            ret = super(InstallContext, self).execute_build()
        finally:
            msg.log.setLevel(lvl)
        return ret
    pass # class InstallContext

### -----------------------------------------------------------------------------
import sys
import waflib.Build
class UninstallContext(waflib.Build.UninstallContext):
    def __init__(self, **kw):
        super(UninstallContext, self).__init__(**kw)
        return

    def execute_build(self):
        self.logger = msg
        lvl = msg.log.level
        if lvl < msg.logging.ERROR:
            msg.log.setLevel(msg.logging.ERROR)
        try:
            ret = super(UninstallContext, self).execute_build()
        finally:
            msg.log.setLevel(lvl)
        return ret
    pass # class UninstallContext

### ---------------------------------------------------------------------------
@feature('*')
@after_method('process_source') #@before_method('process_rule')
def massage_c_and_cxx_linkflags(self):
    for n in ('cshlib', 'cstlib', 'cprogram',):
        c = waflib.Task.classes[n]
        c.run_str='${LINK_CC} ${CCLNK_SRC_F}${SRC} ${CCLNK_TGT_F}${TGT[0].abspath()} ${LINKFLAGS} ${RPATH_ST:RPATH} ${FRAMEWORKPATH_ST:FRAMEWORKPATH} ${FRAMEWORK_ST:FRAMEWORK} ${ARCH_ST:ARCH} ${STLIB_MARKER} ${STLIBPATH_ST:STLIBPATH} ${STLIB_ST:STLIB} ${SHLIB_MARKER} ${LIBPATH_ST:LIBPATH} ${LIB_ST:LIB}'
    for n in ('cxxshlib', 'cxxstlib', 'cxxprogram',):
        cxx = waflib.Task.classes[n]
        cxx.run_str='${LINK_CXX} ${CXXLNK_SRC_F}${SRC} ${CXXLNK_TGT_F}${TGT[0].abspath()} ${LINKFLAGS} ${RPATH_ST:RPATH} ${FRAMEWORKPATH_ST:FRAMEWORKPATH} ${FRAMEWORK_ST:FRAMEWORK} ${ARCH_ST:ARCH} ${STLIB_MARKER} ${STLIBPATH_ST:STLIBPATH} ${STLIB_ST:STLIB} ${SHLIB_MARKER} ${LIBPATH_ST:LIBPATH} ${LIB_ST:LIB}'
    return

### ---------------------------------------------------------------------------
@feature('cxx', 'c')
@after_method('apply_incpaths')
def insert_blddir(self):
    self.env.prepend_value('INCPATHS', self.env.BUILD_INSTALL_AREA_INCDIR)
    self.env.prepend_value('INCPATHS', self.env.INSTALL_AREA_INCDIR)
    self.env.prepend_value('INCPATHS', '.')

    self.env.prepend_value('LIBPATH', self.env.BUILD_INSTALL_AREA_LIBDIR)
    return

### ---------------------------------------------------------------------------
@feature('hwaf_runtime_tsk', '*')
@before_method('process_rule')
def insert_project_level_pythonpath(self):
    '''
    insert_project_level_pythonpath adds ${INSTALL_AREA}/python into the
    ${PYTHONPATH} environment variable.
    '''
    _get = getattr(self, 'hwaf_get_install_path', None)
    if not _get: _get = getattr(self.bld, 'hwaf_get_install_path')
    pydir = _get('${INSTALL_AREA}/python')
    self.env.prepend_value('PYTHONPATH', pydir)
    return

### ---------------------------------------------------------------------------
@feature('hwaf_runtime_tsk', '*')
@before_method('process_rule')
def insert_project_level_joboptpath(self):
    '''
    insert_project_level_joboptpath adds ${INSTALL_AREA}/jobOptions into the
    ${JOBOPTSEARCHPATH} environment variable.
    '''
    _get = getattr(self, 'hwaf_get_install_path', None)
    if not _get: _get = getattr(self.bld, 'hwaf_get_install_path')
    d = _get('${INSTALL_AREA}/jobOptions')
    self.env.prepend_value('JOBOPTSEARCHPATH', d)
    return

### ---------------------------------------------------------------------------
@feature('hwaf_runtime_tsk', '*')
@before_method('process_rule')
def insert_project_level_datapath(self):
    '''
    insert_project_level_datapath adds ${INSTALL_AREA}/share into the
    ${DATAPATH} environment variable.
    '''
    _get = getattr(self, 'hwaf_get_install_path', None)
    if not _get: _get = getattr(self.bld, 'hwaf_get_install_path')
    d = _get('${INSTALL_AREA}/share')
    self.env.prepend_value('DATAPATH', d)
    return

### ---------------------------------------------------------------------------
@feature('hwaf_runtime_tsk', '*')
@before_method('process_rule')
def insert_project_level_xmlpath(self):
    '''
    insert_project_level_xmlpath adds ${INSTALL_AREA}/XML into the
    ${XMLPATH} environment variable.
    '''
    _get = getattr(self, 'hwaf_get_install_path', None)
    if not _get: _get = getattr(self.bld, 'hwaf_get_install_path')
    d = _get('${INSTALL_AREA}/XML')
    self.env.prepend_value('XMLPATH', d)
    return

### ---------------------------------------------------------------------------
class symlink_tsk(waflib.Task.Task):
    """
    A task to install symlinks of binaries and libraries under the *build*
    install-area (to not require shaggy RPATH)
    this is needed for genconf and gencliddb.
    """
    color   = 'PINK'
    reentrant = True
    
    def run(self):
        import os
        try:
            os.remove(self.outputs[0].abspath())
        except OSError:
            pass
        return os.symlink(self.inputs[0].abspath(),
                          self.outputs[0].abspath())


@feature('symlink_tsk')
@after_method('apply_link')
def add_install_copy(self):
    link_cls_name = self.link_task.__class__.__name__
    # FIXME: is there an API for this ?
    if link_cls_name.endswith('lib'):
        outdir = self.bld.path.make_node('.install_area').make_node('lib')
    else:
        outdir = self.bld.path.make_node('.install_area').make_node('bin')
    link_outputs = waflib.Utils.to_list(self.link_task.outputs)
    for out in link_outputs:
        if isinstance(out, str):
            n = out
        else:
            n = out.name
        out_sym = outdir.find_or_declare(n)
        #print("===> ", self.target, link_cls_name, out_sym.abspath())
        tsk = self.create_task('symlink_tsk',
                               out,
                               out_sym)
        self.source += tsk.outputs

# def symlink_tgt(cls):
#     old = cls.run
#     def wrap(self):
#         return old(self)
#     setattr(cls, 'run', wrap)
# symlink_tgt(some_cls)

def _get_pkg_name(self):
    # FIXME: should this be more explicit ?
    pkg_name = self.path.name
    return pkg_name

def _get_pkg_version_defines(self):
    pkg_name = _get_pkg_name(self)
    pkg_vers = "%s-XX-XX-XX" % pkg_name
    pkg_defines = ['PACKAGE_VERSION="%s"' % pkg_vers,
                   'PACKAGE_VERSION_UQ=%s'% pkg_vers]
    cmt_dir_node = self.path.get_src().find_dir('cmt')
    if not cmt_dir_node:
        return pkg_defines
    version_cmt = cmt_dir_node.find_resource('version.cmt')
    if not version_cmt:
        return pkg_defines
    pkg_vers = version_cmt.read().strip()
    pkg_defines = ['PACKAGE_VERSION="%s"' % pkg_vers,
                   'PACKAGE_VERSION_UQ=%s'% pkg_vers]
    #msg.debug("*** %s %r" % (pkg_name, pkg_vers))
    return pkg_defines

def _get_srcs_lst(self, source):
    '''hack to support implicit src/*cxx in CMT req-files'''
    if isinstance(source, (list, tuple)):
        src = []
        for s in source:
            src.extend(_get_srcs_lst(self, s))
        return src
    elif not isinstance(source, type('')):
        ## a waflib.Node ?
        return [source]
    else:
        src_node = self.path.find_dir('src')
        srcs = self.path.ant_glob(source)
        if srcs:
            # OK. finders, keepers.
            pass
        elif src_node:
            # hack to mimick CMT's default (to take sources from src)
            srcs = src_node.ant_glob(source)
            pass
        if not srcs:
            # ok, try again from bldnode
            src_node = self.path.find_dir('src')
            try:    srcs = self.path.get_bld().ant_glob(source)
            except: pass
            if srcs:
                # OK. finders, keepers.
                pass
            elif src_node:
                # hack to mimick CMT's default (to take sources from src)
                try:    srcs = src_node.get_bld().ant_glob(source)
                except: pass
                pass
            if not srcs:
                # ok, maybe the output of a not-yet executed task
                srcs = source
                pass
            pass
        return waflib.Utils.to_list(srcs)
    self.fatal("unreachable")
    return []

### ---------------------------------------------------------------------------
def build_app(self, name, source, **kw):
    kw = dict(kw)

    # FIXME: hack !!! cppunit doesn't propagate correctly...
    do_test = kw.get('do_test', False)
    if do_test:
        return

    kw['features'] = waflib.Utils.to_list(
        kw.get('features', 'cxx cxxprogram')) + [
        'symlink_tsk',
        ]
    
    kw['use'] = waflib.Utils.to_list(kw.get('use', []))

    pkg_node = self.path.get_src()
    src_node = self.path.find_dir('src')

    srcs = _get_srcs_lst(self, source)
    linkflags = waflib.Utils.to_list(kw.get('linkflags', []))
    linkflags = self.env.SHLINKFLAGS + linkflags
    kw['linkflags'] = linkflags

    defines = waflib.Utils.to_list(kw.get('defines', []))
    kw['defines'] = defines + _get_pkg_version_defines(self)
    
    includes = waflib.Utils.to_list(kw.get('includes', []))
    includes.insert(0, self.path.abspath())
    #includes.insert(1, self.path.abspath()+'/'+PACKAGE_NAME)
    kw['includes'] = includes + [src_node]

    # extract package name
    PACKAGE_NAME = _get_pkg_name(self)

    exe = self(
        name=name,
        source=srcs,
        target=name+'.exe',
        install_path='${INSTALL_AREA}/bin',
        libpath = self.env.LD_LIBRARY_PATH + [self.path.get_bld().abspath()],
        #libpath = self.env.LD_LIBRARY_PATH,
        **kw)
        
    return exe

### ---------------------------------------------------------------------------
def build_complib(self, name, source, **kw):

    kw = dict(kw)
    do_genmap = kw.get('do_genmap', True)
    do_genconf= kw.get('do_genconf', True)
    do_cliddb = kw.get('do_cliddb', False)
    
    #msg.info('=========== %s ============' % name)
    #msg.info("::: %s" % self.path.abspath())
    src_node = self.path.find_dir('src')
    bld_node = src_node.get_bld()

    srcs = _get_srcs_lst(self, source)
    includes = waflib.Utils.to_list(kw.get('includes', []))
    includes.insert(0, self.path.abspath())
    #includes.insert(1, self.path.abspath()+'/'+PACKAGE_NAME)
    kw['includes'] = includes + [src_node]

    linkflags = waflib.Utils.to_list(kw.get('linkflags', []))
    linkflags = self.env.SHLINKFLAGS + linkflags
    kw['linkflags'] = linkflags

    defines = waflib.Utils.to_list(kw.get('defines', []))
    kw['defines'] = defines + _get_pkg_version_defines(self)

    kw['depends_on'] = waflib.Utils.to_list(kw.get('use', [])) + \
                       waflib.Utils.to_list(kw.get('depends_on', []))
    #print("---> depends: %s" % kw['depends_on'])
    
    # extract package name
    PACKAGE_NAME = _get_pkg_name(self)

    # schedule the requested features
    features = ['cxx', 'cxxshlib',]
    features.append('symlink_tsk')
    if do_genmap:
        features.append('gen_map')
    if do_genconf:
        features.append('gen_conf')
        #features.append('py')
    if do_cliddb:
        features.append('gen_cliddb')
        
    lib = self(
        #features='cxx cxxshlib symlink_tsk',
        features=features,
        name='complib-%s' % name,
        source=srcs,
        target=name,
        install_path='${INSTALL_AREA}/lib',
        libpath = self.env.LD_LIBRARY_PATH + [self.path.get_bld().abspath()],
        reentrant=True,
        **kw)
    lib_name = "lib%s.so" % (lib.target,) # FIXME !!
    lib.env['GENCONF_LIBNAME'] = lib.target
    lib.env['PACKAGE_NAME'] = PACKAGE_NAME
    lib.env['GENCLIDDB_LIB_NAME'] = lib.target
    lib.env['GENCLIDDB'] = self.env['GENCLIDDB']
    
    return lib

### ---------------------------------------------------------------------------
def build_linklib(self, name, source, **kw):

    #msg.info('=========== %s ============' % name)
    # extract package name
    PACKAGE_NAME = _get_pkg_name(self)

    kw = dict(kw)
    linkflags = kw.get('linkflags', [])
    linkflags = self.env.SHLINKFLAGS + linkflags
    kw['linkflags'] = linkflags
    
    src_node = self.path.find_dir('src')

    srcs = _get_srcs_lst(self, source)
    includes = waflib.Utils.to_list(kw.get('includes', []))
    includes.insert(0, self.path.abspath())
    #includes.insert(1, self.path.abspath()+'/'+PACKAGE_NAME)
    kw['includes'] = includes + [src_node]

    export_incs = None
    kw['export_includes'] = waflib.Utils.to_list(
        kw.get('export_includes', [])
        )[:]
    if not kw['export_includes']:
        inc_node = self.path.find_dir(PACKAGE_NAME)
        if inc_node:
            export_incs = '.'
            kw['export_includes'].append(export_incs)
        inc_node = self.path.find_dir('inc/%s' % PACKAGE_NAME)
        if inc_node:
            export_incs = 'inc'
            kw['export_includes'].append(export_incs)
            #self.fatal('%s: export_includes - inc' % name)
        else:
            #self.fatal('%s: could not find [inc/%s] !!' % (name,PACKAGE_NAME))
            pass
    else:
        export_incs = kw['export_includes']
        #msg.info('%s: exports: %r' % (name, kw['export_includes']))
        pass

    kw['includes'].extend(kw['export_includes'])
    
    kw['use'] = waflib.Utils.to_list(kw.get('use', [])) + ['dl']
    
    defines = waflib.Utils.to_list(kw.get('defines', []))
    kw['defines'] = defines + _get_pkg_version_defines(self)

    #msg.info ("==> build_linklib(%s, '%s', %r)..." % (name, source, kw))
    o = self(
        features        = 'cxx cxxshlib symlink_tsk',
        name            = name,
        source          = srcs,
        target          = name,
        install_path    = '${INSTALL_AREA}/lib',
        #export_includes = ['.', './'+PACKAGE_NAME],
        #export_includes = export_,
        libpath = self.env.LD_LIBRARY_PATH + [self.path.get_bld().abspath()],
        #libpath         = self.env.LD_LIBRARY_PATH,
        **kw
        )
    # for use-exports
    self.env['LIB_%s' % name] = [name]
    for lib in waflib.Utils.to_list(kw['use']):
        env = self.env
        if lib == name:
            continue
        env.append_unique('INCLUDES_%s'%name, env['INCLUDES_%s'%lib])
        env.append_unique('LIB_%s'%name,      env['LIB_%s'%lib])
        env.append_unique('LIBPATH_%s'%name,  env['LIBPATH_%s'%lib])
        pass
    self.env.append_unique('LIBPATH_%s'%name, self.path.get_bld().abspath())
    #msg.info('--> libpath[%s]: %s' % (name, self.env['LIBPATH_%s'%name]))
    #msg.info('--> incpath[%s]: %s' % (name, export_incs))

    if export_incs:
        export_incs = waflib.Utils.to_list(export_incs)[0]
        if export_incs == '.':
            self.install_headers()
        elif export_incs == 'inc':
            incdir = self.path.find_dir('inc')
            hdrdir = 'inc/%s' % PACKAGE_NAME
            self.install_headers(hdrdir, cwd=incdir)
        else:
            pass

    #o.post()
    return o

### ---------------------------------------------------------------------------
def build_dual_use_lib(self, name, source, **kw):

    # extract package name
    PACKAGE_NAME = _get_pkg_name(self)

    srcs = _get_srcs_lst(self, source)
    link_libname = name
    link_kw = dict(kw)
    link_kw['name'] = link_libname
    link_kw['source'] = srcs
    link_o = self.build_linklib(**link_kw)

    comp_kw = dict(kw)
    comp_libname = name + "Comps"
    comp_kw['name'] = comp_libname
    comp_uses = waflib.Utils.to_list(comp_kw.get('use', []))
    comp_kw['use'] = [link_libname] + comp_uses
    src_dir = self.path.find_dir('src')
    if not src_dir:
        self.fatal("no 'src' directory in package [%s]!" % PACKAGE_NAME)
        pass
    comp_dir = src_dir.find_dir('components')
    if not comp_dir:
        self.fatal("no 'src/components' directory in package [%s]!" %
                   PACKAGE_NAME)
        pass
    comp_srcs = comp_dir.ant_glob("*.cxx")
    comp_kw['source'] = srcs + comp_srcs
    comp_o = self.build_complib(**comp_kw)

    pydir = self.path.find_dir('python')
    if not pydir:
        pydir = self.path.find_or_declare('python')
        pydir.make_node('__init__.py')
        pass
    pyredirect = pydir.make_node(name+'Conf.py')
    pyredirect.write(
'''## redirect %s.%sConf to %s.%sConf
from %s.%sConf import *
## EOF ##
''' % (PACKAGE_NAME, comp_libname,
       PACKAGE_NAME, link_libname,
       PACKAGE_NAME, comp_libname)
        )

    return

### ---------------------------------------------------------------------------
def build_pymodule(self, source, **kw):
    
    # extract package name
    PACKAGE_NAME = _get_pkg_name(self)

    # add ${INSTALL_AREA}/python to PYTHONPATH if not there already
    #pypath = self.hwaf_get_install_path('${INSTALL_AREA}/python')
    pypath = waflib.Utils.subst_vars('${INSTALL_AREA}/python', self.env)
    if not (pypath in self.env.get_flat('PYTHONPATH')):
        self.env.prepend_value('PYTHONPATH', pypath)
        pass
    
    install_path_root = kw.get('install_path_root',
                               '${INSTALL_AREA}/python/%s' % PACKAGE_NAME)
    
    #source = waflib.Utils.to_list(source)
    pydir = self.path.find_dir('python')
    if not pydir:
        msg.info(
            'no such directory: [%s]' %
            os.path.join(self.path.abspath(), 'python')
            )
        msg.info('cannot execute [build_pymodule]')
        return
    pyfiles = pydir.ant_glob(
        '**/*',
        dir=False,
        relative_trick=True,
        )
    if 1:
        _fixup_pymodule_install(
            self,
            name = 'py-%s' % PACKAGE_NAME,
            source = pyfiles,
            install_path_root = install_path_root
            )
    else:
        self(
            features     = 'py',
            name         = 'py-%s' % PACKAGE_NAME,
            source       = pyfiles,
            install_path = '${INSTALL_AREA}/python/%s' % PACKAGE_NAME,
            )
    return

def _fixup_pymodule_install(self, name, source, install_path_root):
    # temporary hack for issue 901
    # http://code.google.com/p/waf/issues/detail?id=901
    source = waflib.Utils.to_list(source)
    pydir = self.path.get_src().find_dir('python')
    if not pydir:
        return
    dirs = {}
    for f in source:
        fname = f.path_from(pydir)
        dname = os.path.dirname(fname)
        try:
            dirs[dname].append(f)
        except KeyError:
            dirs[dname] = [f]
    for d in dirs:
        if (not d) or d == '.':
            n = name
            i = install_path_root
        else:
            n = '%s-%s' % (name, d)
            i = os.path.join(install_path_root, d)
            
        self(
            features     = 'py',
            name         = n,
            source       = dirs[d],
            install_path = i,
            )
    return

### -----------------------------------------------------------------------------
def install_joboptions(self, source='share/*.py', cwd='share', **kw):
    
    # extract package name
    PACKAGE_NAME = _get_pkg_name(self)

    source = waflib.Utils.to_list(source)
    _srcs = []
    for f in source:
        _srcs.extend(self.path.ant_glob(f, dir=False))
    source = _srcs[:]
    del _srcs
    
    if isinstance(cwd, str):
        cwd = self.path.find_dir(cwd)

    self.install_files(
        '${INSTALL_AREA}/jobOptions/%s' % PACKAGE_NAME,
        source,
        cwd=cwd,
        relative_trick=True
        )
    return

### -----------------------------------------------------------------------------
def install_headers(self, incdir=None, relative_trick=True, cwd=None):
    
    # extract package name
    PACKAGE_NAME = _get_pkg_name(self)
    inc_node = None
    if not incdir:
        inc_node = self.path.find_dir(PACKAGE_NAME)
        if not inc_node:
            return
    else:
        if isinstance(incdir, str):
            inc_node = self.path.find_dir(incdir)
        else:
            inc_node = incdir
            pass
        pass
    
    if isinstance(cwd, str):
        cwd = self.path.find_dir(cwd)
        
    if not inc_node:
        self.fatal('no such directory [%s] (pkg=%s)' % (incdir, PACKAGE_NAME))
        pass
    
    includes = inc_node.ant_glob('**/*', dir=False)
    self.install_files(
        '${INSTALL_AREA}/include', includes, 
        relative_trick=relative_trick,
        cwd=cwd,
        postpone=False,
        )

    incpath = waflib.Utils.subst_vars('${INSTALL_AREA}/include',self.env)
    #msg.info("--> [%s] %s" %(PACKAGE_NAME,incpath))
    self.env.append_unique('INCLUDES_%s' % PACKAGE_NAME,
                           [incpath,inc_node.parent.abspath()])
    #inc_node.parent.abspath())
    return
    
### -----------------------------------------------------------------------------
def install_scripts(self, source, **kw):
    
    # extract package name
    PACKAGE_NAME = _get_pkg_name(self)

    source = waflib.Utils.to_list(source)
    _srcs = []
    for f in source:
        _srcs.extend(self.path.ant_glob(f, dir=False))
    source = _srcs[:]
    del _srcs
    
    self.install_files(
        '${INSTALL_AREA}/bin',
        source, 
        #relative_trick=True,
        chmod=waflib.Utils.O755,
        )
    return

### ---------------------------------------------------------------------------
def install_xmls(self, source, relative_trick=True, cwd=None):
    
    # extract package name
    PACKAGE_NAME = _get_pkg_name(self)

    source = waflib.Utils.to_list(source)
    _srcs = []
    for f in source:
        _srcs.extend(self.path.ant_glob(f, dir=False))
    source = _srcs[:]
    del _srcs

    self.install_files(
        '${INSTALL_AREA}/XML/%s' % PACKAGE_NAME,
        source, 
        relative_trick=relative_trick,
        cwd=cwd,
        postpone=False,
        )
    return

### ---------------------------------------------------------------------------
def install_data(self, source, relative_trick=False, cwd=None):
    
    # extract package name
    PACKAGE_NAME = _get_pkg_name(self)

    source = waflib.Utils.to_list(source)
    _srcs = []
    for f in source:
        _srcs.extend(self.path.ant_glob(f, dir=False))
    source = _srcs[:]
    del _srcs

    self.install_files(
        '${INSTALL_AREA}/share',
        source, 
        relative_trick=relative_trick,
        cwd=cwd,
        postpone=False,
        )
    return


### ----------------------------------------------------------------------------
@feature('gen_conf')
@after('symlink_tsk')
def schedule_gen_conf(self):
    lnk_task = getattr(self, 'link_task', None)
    if not lnk_task:
        return
    for n in lnk_task.outputs:
        gen_conf_hook(self, n)
    pass

@after('symlink_tsk')
def gen_conf_hook(self, node):
    "Bind the .dsomap file extension to the creation of a genconf task"
    dso = self.env['GENCONF_LIBNAME']
    bld_node = node.get_bld().parent
    pkg_name = bld_node.name # FIXME!!
    genconf_dir_node = bld_node.make_node('genConf').make_node(pkg_name)
    self.env['GENCONF_OUTPUTDIR'] = genconf_dir_node.abspath()
    genconf_node = genconf_dir_node.make_node('%sConf.py' % dso)
    initpy_node = genconf_dir_node.make_node('__init__.py')
    confdb_node = genconf_dir_node.make_node('%s_confDb.py' % dso)
    tsk = self.create_task('gen_conf',
                           node,
                           [genconf_node,genconf_dir_node,initpy_node,confdb_node])
    # schedule the merge of confdb.py files
    merge_confdb_hook(self, confdb_node).set_run_after(tsk)

    # schedule the installation of py-files
    src_node = self.path.get_src()
    py_dir = src_node.find_dir('python')
    py_files = [genconf_node, confdb_node]
    if not py_dir:
        py_files.append(initpy_node)
    PACKAGE_NAME = self.env['PACKAGE_NAME']
    self.bld(
        features='py',
        name    ='py-genconf-%s' % PACKAGE_NAME,
        source  = py_files,
        install_path = '${INSTALL_AREA}/python/%s' % PACKAGE_NAME,
        )

    # add ${INSTALL_AREA}/python to PYTHONPATH if not there already
    pypath = waflib.Utils.subst_vars('${INSTALL_AREA}/python', self.env)
    if not pypath in self.env.get_flat('PYTHONPATH'):
        self.env.prepend_value('PYTHONPATH', pypath)
        pass
    
    return

class gen_conf(waflib.Task.Task):
    vars = ['DEFINES', 'INCLUDES',
            'GENCONF', 
            'GENCONF_CONFIGURABLE_MODULE']
    color= 'BLUE'
    ext_in  = ['.bin', '.so']
    ext_out = ['.py']
    shell = False
    reentrant = True
    after = ['cxxshlib', 'cxxprogram', 'symlink_tsk', 'gen_map']
    depends_on = ['genconf', 'complib-GaudiCoreSvc']
    
    def run(self):
        import os
        cmd = '${GENCONF} -p ${PACKAGE_NAME} -i %s -o ${GENCONF_OUTPUTDIR} --configurable-module=${GENCONF_CONFIGURABLE_MODULE}' % (
            self.inputs[0].name,
            )
        cmd = waflib.Utils.subst_vars(cmd, self.env)

        bld_node = self.inputs[0].parent.get_bld()
    
        o = self.outputs[0].change_ext('.genconf.log')
        fout_node = bld_node.find_or_declare(o.name)
        fout = open(fout_node.abspath(), 'w')
        env = self.generator.bld._get_env_for_subproc()
        rc = self.generator.bld.exec_command(
            cmd,
            stdout=fout,
            stderr=fout,
            env=env
            )
        if rc != 0:
            msg.error("** error running [%s]" % cmd)
            msg.error(fout_node.read())
        return rc
    
### ---------------------------------------------------------------------------
g_confdb_merger = None
@feature('merge_confdb')
def schedule_merge_confdb(self):
    pass

@extension('_confDb.py')
def merge_confdb_hook(self, node):
    global g_confdb_merger
    if g_confdb_merger is None:
        import os
        bld_area = os.path.basename(self.env['BUILD_INSTALL_AREA'])
        bld_node = self.bld.bldnode.find_dir(bld_area)
        py_node = bld_node.make_node('python')
        py_node.mkdir()
        out_node = py_node.make_node(
            'project_%s_merged_confDb.py' %
            self.bld.hwaf_project_name().replace('-', '_')
            )
        g_confdb_merger = self.create_task('merge_confdb', node, out_node)
        self.bld.install_files(
            '${INSTALL_AREA}/python',
            out_node,
            relative_trick=False
            )
    else:
        g_confdb_merger.inputs.append(node)
    return g_confdb_merger

class merge_confdb(waflib.Task.Task):
    color='PINK'
    ext_in = ['_confDb.py']
    #ext_out= ['.py']
    after = ['merge_dsomap',]
    run_str = 'cat ${SRC} > ${TGT}'
    reentrant = False
    
    def runnable_status(self):
        status = waflib.Task.Task.runnable_status(self)
        if status == waflib.Task.ASK_LATER:
            return status
        
        import os
        for in_node in self.inputs:
            try:
                os.stat(in_node.abspath())
            except:
                msg.debug("::missing input [%s]" % in_node.abspath())
                return waflib.Task.ASK_LATER
        return waflib.Task.RUN_ME
    
### ---------------------------------------------------------------------------
import waflib.Build
waflib.Build.BuildContext.build_complib = build_complib
waflib.Build.BuildContext.build_linklib = build_linklib
waflib.Build.BuildContext.build_dual_use_lib = build_dual_use_lib
waflib.Build.BuildContext.build_app = build_app

waflib.Build.BuildContext.build_pymodule = build_pymodule
waflib.Build.BuildContext.install_joboptions = install_joboptions
waflib.Build.BuildContext.install_headers = install_headers
waflib.Build.BuildContext.install_scripts = install_scripts
waflib.Build.BuildContext.install_data = install_data
waflib.Build.BuildContext.install_xmls = install_xmls

## EOF ##
        