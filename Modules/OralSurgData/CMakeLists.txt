#-----------------------------------------------------------------------------
set(MODULE_NAME OralSurgData)

#-----------------------------------------------------------------------------
set(MODULE_PYTHON_SCRIPTS
  ${MODULE_NAME}.py
  )

set(MODULE_PYTHON_RESOURCES
  Resources/Icons/${MODULE_NAME}.png
  Resources/Icons/da3d.png
  Resources/Icons/dacs.png
  Resources/Icons/daeng.png
  Resources/Icons/daDentImplIm.png
  Resources/Icons/dagr.png
  Resources/Icons/daGenIImplCr.png
  Resources/Icons/daOrSurgMod.png
  Resources/Icons/dared.png
  Resources/Icons/daRegisterMod.png
  Resources/Icons/daVirtualPr.png
  Resources/Icons/daws.png 
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
