export CMTCONFIG=${CMTCONFIG:-x86_64-slc5-gcc46-opt}
export CMTPROJECTPATH=${CMTPROJECTPATH:-/afs/cern.ch/sw/lcg/app/releases}
export PATH=/afs/cern.ch/sw/lcg/external/CMake/2.8.6/$CMTCONFIG/bin:$PATH

echo "::: CMTCONFIG=[${CMTCONFIG}]"
echo "::: CMTPROJECTPATH=[${CMTPROJECTPATH}]"
. /afs/cern.ch/sw/lcg/external/gcc/4.6.2/${CMTCONFIG}/setup.sh

