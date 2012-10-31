gaudi-hive
==========

A testbed for a multicore-enabled gaudi-based framework.

Installation
------------

```sh
$ asetup slc5,64,rel_2,devval,gcc46
$ . ./atlas-setup.sh
$ ./configure
$ cd build-dir
$ make -j 8
$ make install

# useful alias
$ alias gaudirun="python2.6 $PWD/cmake/env.py -x $PWD/InstallArea/$CMTCONFIG/GaudiEnvironment.xml  gaudirun.py"

# hello world examples
$ cd GaudiExamples/options
$ gaudirun GaudiCommonTests.opts

# hive examples
$ cd GaudiHive/options
$ gaudirun Hive.opts
```

