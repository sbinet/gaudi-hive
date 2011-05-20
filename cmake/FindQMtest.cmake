include(Configuration)

set(QMtest_FOUND 1)

if(WIN32)
  set(QMtest_environment QM_home=${QMtest_home}
                         PATH+=${QMtest_home}/Scripts
                         PATH+=${QMtest_home}/Lib/site-packages/pywin32_system32
                         PYTHONPATH+=${QMtest_home}/Lib/site-packages
     )
else()
  set(QMtest_environment QM_home=${QMtest_home}
                         PATH+=${QMtest_home}/bin
                         PYTHONPATH+=${QMtest_home}/lib/python${Python_config_version_twodigit}/site-packages
     )
endif()

