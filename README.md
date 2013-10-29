gaudi-hive
==========

A testbed for a multicore-enabled gaudi-based framework.

## Installation with CMake

```sh
$ export CMTCONFIG=x86_64-slc6-gcc46-opt
$ cd gaudi-hive
$ . ./atlas-setup.sh
$ ./configure
$ (cd build-dir && make -j 8 && make install)

# useful alias
$ cd gaudi-hive
$ alias gaudirun="python2.6 $PWD/cmake/env.py -x $PWD/InstallArea/$CMTCONFIG/GaudiEnvironment.xml  gaudirun.py"

# hello world examples
$ cd GaudiExamples/options
$ gaudirun GaudiCommonTests.opts

# hive examples
$ cd GaudiHive/options
$ gaudirun Hive.opts
```

## Installation with hwaf

```sh
# create a workarea
$ hwaf init work
$ cd work

# bootstrap workarea
$ hwaf setup -variant=x86_64-slc6-gcc46-opt

# checkout gaudi-hive, use wip/cmt-ng branch
$ hwaf pkg co -b=wip/cmt-ng git://github.com/sbinet/gaudi-hive hive

# finish bootstrap of gaudi-hive/hwaf
$ cat src/hive/hwaf-cfg/lcg-64d.conf >> local.conf

# configure, make, make-install
$ hwaf configure
$ hwaf

# run
$ hwaf shell 
[hwaf] $ cd install-area/jobOptions/GaudiExamples
[hwaf] $ gaudirun.py GaudiCommonTests.opts
```

