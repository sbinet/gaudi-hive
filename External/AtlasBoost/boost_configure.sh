#!/bin/sh

#cd tools/jam/src || exit 1
#LOCATE_TARGET=${BOOST_BJAM_LOCATE_TARGET} ./build.sh || exit 1
cd tools/build/v2 || exit 1
LOCATE_TARGET=${BOOST_BJAM_LOCATE_TARGET} ./bootstrap.sh || exit 1
