#-----------------------------------------------------------------------------
set(MODULE_NAME DentImplImaging)

#-----------------------------------------------------------------------------
set(MODULE_PYTHON_SCRIPTS
  ${MODULE_NAME}.py
  )

set(MODULE_PYTHON_RESOURCES
  Resources/Icons/${MODULE_NAME}.png  
  Resources/Icons/di3d.png
  Resources/Icons/dics.png
  Resources/Icons/dieng.png
  Resources/Icons/diGenIImplCr.png
  Resources/Icons/digr.png
  Resources/Icons/diOrSurgMod.png
  Resources/Icons/diOSData.png
  Resources/Icons/dired.png
  Resources/Icons/diRegisterMod.png
  Resources/Icons/dispot.png
  Resources/Icons/diVirtualPr.png
  Resources/Icons/diws.png 
  Resources/UI/${MODULE_NAME}.ui
  )

#-----------------------------------------------------------------------------
slicerMacroBuildScriptedModule(
  NAME ${MODULE_NAME}
  SCRIPTS ${MODULE_PYTHON_SCRIPTS}
  RESOURCES ${MODULE_PYTHON_RESOURCES}
  WITH_GENERIC_TESTS
  )

#-----------------------------------------------------------------------------
if(BUILD_TESTING)

  # Register the unittest subclass in the main script as a ctest.
  # Note that the test will also be available at runtime.
  slicer_add_python_unittest(SCRIPT ${MODULE_NAME}.py)

  # Additional build-time testing
  add_subdirectory(Testing)
endif()
