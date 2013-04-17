#!/bin/sh

PYTHON_VERSION_TWODIGIT=$1
shift
PYTHON_ROOT=$1
shift
BOOST_TOOLSET=$1
shift

echo "using python : ${PYTHON_VERSION_TWODIGIT} : ${PYTHON_ROOT} ;" >| user-config.jam
echo "using ${BOOST_TOOLSET} : : :  " >> user-config.jam
echo "   <linkflags>\"${BOOST_BJAM_LINK_FLAGS}\" " >> user-config.jam
echo "   <compileflags>\"${BOOST_BJAM_COMPILE_FLAGS}\" " >> user-config.jam
echo "   ; " >> user-config.jam

