gaudi_subdir(GaudiCoreSvc v1r3)

gaudi_depends_on_subdirs(GaudiKernel)

find_package(Boost COMPONENTS system filesystem regex thread python)
find_package(TBB)
find_package(PythonLibs)
include_directories (${PYTHON_INCLUDE_DIRS})

#---Libraries---------------------------------------------------------------
gaudi_add_module(GaudiCoreSvc
                 src/ApplicationMgr/*.cpp
                 src/EventSelector/*.cpp
                 src/IncidentSvc/*.cpp
                 src/JobOptionsSvc/*.cpp
                 src/MessageSvc/*.cpp
                 LINK_LIBRARIES GaudiKernel Boost TBB ${PYTHON_LIBRARIES}
                 INCLUDE_DIRS TBB)

