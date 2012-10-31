gaudi-hive
==========

A testbed for a multicore-enabled gaudi-based framework.

Installation
------------

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

