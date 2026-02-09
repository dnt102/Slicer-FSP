#-----------------------------------------------------------------------------
set(MODULE_NAME VirtualProsth)

#-----------------------------------------------------------------------------
set(MODULE_PYTHON_SCRIPTS
  ${MODULE_NAME}.py
)

set(MODULE_PYTHON_RESOURCES
  Resources/Icons/${MODULE_NAME}.png
  Resources/Icons/vp3d.png
  Resources/Icons/vpcs.png
  Resources/Icons/vpeng.png
  Resources/Icons/vpDentImplIm.png
  Resources/Icons/vpgr.png
  Resources/Icons/vpGenIImplCr.png
  Resources/Icons/vpOSData.png
  Resources/Icons/vpred.png
  Resources/Icons/vpRegisterMod.png
  Resources/Icons/vpOrSurgMod.png
  Resources/Icons/vpws.png
  Resources/UI/${MODULE_NAME}.ui
  Resources/teeth/11v.stl
  Resources/teeth/12v.stl
  Resources/teeth/13v.stl
  Resources/teeth/14v.stl
  Resources/teeth/15v.stl
  Resources/teeth/16v.stl
  Resources/teeth/17v.stl
  Resources/teeth/21v.stl
  Resources/teeth/22v.stl
  Resources/teeth/23v.stl
  Resources/teeth/24v.stl
  Resources/teeth/25v.stl
  Resources/teeth/26v.stl
  Resources/teeth/27v.stl
  Resources/teeth/31v.stl
  Resources/teeth/32v.stl
  Resources/teeth/33v.stl
  Resources/teeth/34v.stl
  Resources/teeth/35v.stl
  Resources/teeth/36v.stl
  Resources/teeth/37v.stl
  Resources/teeth/41v.stl
  Resources/teeth/42v.stl
  Resources/teeth/43v.stl
  Resources/teeth/44v.stl
  Resources/teeth/45v.stl
  Resources/teeth/46v.stl
  Resources/teeth/47v.stl
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
  slicer_add_python_unittest(SCRIPT ${MODULE_NAME}.py)
  add_subdirectory(Testing)
endif()
