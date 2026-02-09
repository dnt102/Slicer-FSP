#-----------------------------------------------------------------------------
set(MODULE_NAME GenericImplCreator)

#-----------------------------------------------------------------------------
set(MODULE_PYTHON_SCRIPTS
  ${MODULE_NAME}.py   
  )

set(MODULE_PYTHON_RESOURCES
  Resources/MIS7XD_libUp.py
  Resources/MIS7XD_libLow.py
  Resources/Icons/${MODULE_NAME}.png
  Resources/Icons/gi3d.png
  Resources/Icons/gics.png
  Resources/Icons/gieng.png
  Resources/Icons/giDentImplIm.png
  Resources/Icons/gigr.png
  Resources/Icons/giOrSurgMod.png
  Resources/Icons/giOSData.png
  Resources/Icons/gired.png
  Resources/Icons/giRegisterMod.png  
  Resources/Icons/giVirtualPr.png
  Resources/Icons/giws.png
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
