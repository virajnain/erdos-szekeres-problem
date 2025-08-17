#----------------------------------------------------------------
# Generated CMake target import file for configuration "Debug".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "MiniSat::libminisat" for configuration "Debug"
set_property(TARGET MiniSat::libminisat APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(MiniSat::libminisat PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_DEBUG "CXX"
  IMPORTED_LOCATION_DEBUG "${_IMPORT_PREFIX}/lib/libminisat.a"
  )

list(APPEND _cmake_import_check_targets MiniSat::libminisat )
list(APPEND _cmake_import_check_files_for_MiniSat::libminisat "${_IMPORT_PREFIX}/lib/libminisat.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
