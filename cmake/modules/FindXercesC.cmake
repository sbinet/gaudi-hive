# - Locate XercesC library
# Defines:
#
#  XERCESC_FOUND
#  XERCESC_INCLUDE_DIR
#  XERCESC_INCLUDE_DIRS (not cached)
#  XERCESC_LIBRARIES

find_path(XERCESC_INCLUDE_DIR xercesc/util/XercesVersion.hpp
          HINTS $ENV{XERCESC_ROOT_DIR}/include  ${XERCESC_ROOT_DIR}/include )
find_library(XERCESC_LIBRARIES NAMES xerces-c
             HINTS $ENV{XERCESC_ROOT_DIR}/lib ${XERCESC_ROOT_DIR}/lib )

set(XERCESC_INCLUDE_DIRS ${XERCESC_INCLUDE_DIR})

# handle the QUIETLY and REQUIRED arguments and set XERCESC_FOUND to TRUE if
# all listed variables are TRUE
INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(XercesC DEFAULT_MSG XERCESC_INCLUDE_DIR XERCESC_LIBRARIES)

mark_as_advanced(XERCESC_FOUND XERCESC_INCLUDE_DIR XERCESC_LIBRARIES)
