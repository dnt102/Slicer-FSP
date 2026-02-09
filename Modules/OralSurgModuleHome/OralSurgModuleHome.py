import logging
import os
from typing import Annotated, Optional
import ctk
import vtk
import qt
import slicer
from slicer.i18n import tr as _
from slicer.i18n import translate
from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin
from slicer.parameterNodeWrapper import (
    parameterNodeWrapper,
    WithinRange,
)
import random
#
# OralSurgModuleHome
#

class OralSurgModuleHome(ScriptedLoadableModule):
    """Uses ScriptedLoadableModule base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = _("Oral Surgery Module Home")  
        self.parent.categories = [translate("qSlicerAbstractCoreModule", "Examples")]
        self.parent.dependencies = []  
        self.parent.contributors = ["Dimitris Trikeriotis (Gnathion)"]
        self.parent.helpText = _("""
To open the related modules.
See more information in <a href="https://github.com/organization/projectname#OralSurgModuleHome">module documentation</a>.
""")
        # TODO: replace with organization, grant and thanks
        self.parent.acknowledgementText = _("""
This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc., Andras Lasso, PerkLab,
and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
""")

 
#
# OralSurgModuleHomeParameterNode
#


@parameterNodeWrapper
class OralSurgModuleHomeParameterNode:
    pass
    


#
# OralSurgModuleHomeWidget
#


class OralSurgModuleHomeWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):
    """Uses ScriptedLoadableModuleWidget base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent=None) -> None:
        """Called when the user opens the module the first time and the widget is initialized."""
        ScriptedLoadableModuleWidget.__init__(self, parent)
        VTKObservationMixin.__init__(self)  # needed for parameter node observation
        self.logic = None
        self._parameterNode = None
        self._parameterNodeGuiTag = None

    def setup(self) -> None:
        """Called when the user opens the module the first time and the widget is initialized."""
        ScriptedLoadableModuleWidget.setup(self)

        # Load widget from .ui file (created by Qt Designer).
        # Additional widgets can be instantiated manually and added to self.layout.
        uiWidget = slicer.util.loadUI(self.resourcePath("UI/OralSurgModuleHome.ui"))
        self.layout.addWidget(uiWidget)
        self.ui = slicer.util.childWidgetVariables(uiWidget)

        # Βρες το developer collapsible button
        self.ui.devCollapsible = self.layout.itemAt(0).widget()

        if isinstance(self.ui.devCollapsible, ctk.ctkCollapsibleButton):
            self.ui.devCollapsible.setProperty("collapsed", True) # το κλείνεις by default

        # Set scene in MRML widgets. Make sure that in Qt designer the top-level qMRMLWidget's
        # "mrmlSceneChanged(vtkMRMLScene*)" signal in is connected to each MRML widget's.
        # "setMRMLScene(vtkMRMLScene*)" slot.
        uiWidget.setMRMLScene(slicer.mrmlScene)

        # Create logic class. Logic implements all computations that should be possible to run
        # in batch mode, without a graphical user interface.
        self.logic = OralSurgModuleHomeLogic()

        # Connections

        # These connections ensure that we update parameter node when scene is closed
        self.addObserver(slicer.mrmlScene, slicer.mrmlScene.StartCloseEvent, self.onSceneStartClose)
        self.addObserver(slicer.mrmlScene, slicer.mrmlScene.EndCloseEvent, self.onSceneEndClose)

        # Buttons
        self.ui.osdataButton.connect("clicked(bool)", self.onosdataButton)
        self.ui.dentalsegmButton.connect("clicked(bool)", self.ondentalsegmButton)
        self.ui.dentimplimagButton.connect("clicked(bool)", self.ondentimplimagButton)
        self.ui.registemodButton.connect("clicked(bool)", self.onregistemodButton)
        self.ui.fastmodalButton.connect("clicked(bool)", self.onfastmodalButton)
        self.ui.virtualprButton.connect("clicked(bool)", self.onvirtualprButton)
        self.ui.genimplcrButton.connect("clicked(bool)", self.ongenimplcrButton)


        self.dentimplicon()
        self.reglicon()
        self.virticon()
        self.genimpicon()
        self.fastmodalicon()
        self.dentsegmicon()
        self.osdataicon()

        self.ui.widescreenButton.connect("clicked(bool)", self.onwidescreenButton)
        self.ui.custom1screenButton.connect("clicked(bool)", self.customlayout1)
        self.ui.redcreenButton.connect("clicked(bool)", self.onredcreenButton)
        self.ui.dscreenButton.connect("clicked(bool)", self.ondscreenButton)

        self.widescreenButton()
        self.custom1screenButton()
        self.redcreenButton()
        self.dscreenButton()


        # Make sure parameter node is initialized (needed for module reload)
        self.initializeParameterNode()
        

    def onosdataButton(self):
        slicer.util.selectModule("OralSurgData")
        slicer.util.reloadScriptedModule("OralSurgData")
    
    def osdataicon(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "hoOSdata.png"))        
        self.ui.osdataButton.setIcon(icon)

    def widescreenButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "hows.png"))        
        self.ui.widescreenButton.setIcon(icon)


    def custom1screenButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "hocs.png"))
        self.ui.custom1screenButton.setIcon(icon)

    def redcreenButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "hored.png"))
        self.ui.redcreenButton.setIcon(icon)

    def dscreenButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "ho3d.png"))
        self.ui.dscreenButton.setIcon(icon)

    def onwidescreenButton(self):
        slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutConventionalWidescreenView)

    def onredcreenButton(self):
        slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUpRedSliceView)

    def ondscreenButton(self):
        slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUp3DView)        
 
    def dentimplicon(self):
        slicer_base = slicer.app.slicerHome        
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "hoDentImplIm.png"))
        self.ui.dentimplimagButton.setIcon(icon)

    def dentsegmicon(self):
        slicer_base = slicer.app.slicerHome        
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "hodentsegm.png"))
        self.ui.dentalsegmButton.setIcon(icon)        

    def reglicon(self):
        slicer_base = slicer.app.slicerHome        
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "hoRegisterMod.png"))
        self.ui.registemodButton.setIcon(icon)
        
    def fastmodalicon(self):
        slicer_base = slicer.app.slicerHome
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "hoFastModAlign.png"))
        self.ui.fastmodalButton.setIcon(icon)        

    def virticon(self):
        slicer_base = slicer.app.slicerHome        
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "hoVirtualPr.png"))
        self.ui.virtualprButton.setIcon(icon)

    def genimpicon(self):
        slicer_base = slicer.app.slicerHome        
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "hoGenIImplCr.png"))
        self.ui.genimplcrButton.setIcon(icon) 


    def ondentalsegmButton(self):
        slicer.util.selectModule("DentalSegmentator")
        #slicer.util.reloadScriptedModule("DentalSegmentator")

    def ondentimplimagButton(self):
        slicer.util.selectModule("DentImplImaging")
        #slicer.util.reloadScriptedModule("DentImplImaging")

    def onregistemodButton(self):
        slicer.util.selectModule("RegisterModule")
        #slicer.util.reloadScriptedModule("RegisterModule")

    def onfastmodalButton(self):
        slicer.util.selectModule("FastModelAlign")
        #slicer.util.reloadScriptedModule("FastModelAlign")

    def onvirtualprButton(self):
        slicer.util.selectModule("VirtualProsth")
        #slicer.util.reloadScriptedModule("VirtualProsth")

    def ongenimplcrButton(self):
        slicer.util.selectModule("GenericImplCreator")
        #slicer.util.reloadScriptedModule("GenericImplCreator")


    def customlayout1(self):        
        
   
        # Define a custom layout with 3D, Axial, Red, and Yellow slices
        customLayout = """
        <layout type="horizontal" split="true">

            <item>
                <layout type="vertical">
                    <item>
                        <view class="vtkMRMLSliceNode" singletontag="Axial">
                            <property name="orientation" action="default">Axial</property>
                            <property name="viewlabel" action="default">A</property>
                        </view>
                    </item>
                    <item>
                        <view class="vtkMRMLSliceNode" singletontag="Yellow">
                            <property name="orientation" action="default">Sagittal</property>
                            <property name="viewlabel" action="default">Y</property>
                        </view>
                    </item>
                </layout>
            </item>
            
            <item>
                <view class="vtkMRMLViewNode" singletontag="1">
                    <property name="viewlabel" action="default">3D</property>
                </view>
            </item>
            
            <item>
                <view class="vtkMRMLSliceNode" singletontag="Red">
                    <property name="orientation" action="default">Axial</property>
                    <property name="viewlabel" action="default">R</property>
                </view>
            </item>
            
        </layout>
        """

        # Register the custom layout
        layoutManager = slicer.app.layoutManager()
        customLayoutId = random.randint(502, 5000)  # Ensure it doesn't conflict with existing layouts
        layoutManager.layoutLogic().GetLayoutNode().AddLayoutDescription(customLayoutId, customLayout)

        # Switch to the custom layout
        layoutManager.setLayout(customLayoutId)

        # Adjust slice visibility
        redSliceWidget = layoutManager.sliceWidget("Red")
        yellowSliceWidget = layoutManager.sliceWidget("Yellow")

        if redSliceWidget:
            redSliceWidget.sliceLogic().FitSliceToAll()

        if yellowSliceWidget:
            yellowSliceWidget.sliceLogic().FitSliceToAll()

        # Configure the axial view
        currentVolume = slicer.util.getNode('vtkMRMLScalarVolumeNode*')
        axialSliceWidget = layoutManager.sliceWidget("Axial")

        if axialSliceWidget and currentVolume:
            axialSliceLogic = axialSliceWidget.sliceLogic()
            axialSliceLogic.GetSliceCompositeNode().SetBackgroundVolumeID(currentVolume.GetID())
            axialSliceLogic.FitSliceToAll() 
        

    def cleanup(self) -> None:
        """Called when the application closes and the module widget is destroyed."""
        self.removeObservers()

    def enter(self) -> None:
        """Called each time the user opens this module."""
        # Make sure parameter node exists and observed
        self.initializeParameterNode()

    def exit(self) -> None:
        """Called each time the user opens a different module."""
        # Do not react to parameter node changes (GUI will be updated when the user enters into the module)
        if self._parameterNode:
            self._parameterNode.disconnectGui(self._parameterNodeGuiTag)
            self._parameterNodeGuiTag = None
            

    def onSceneStartClose(self, caller, event) -> None:
        """Called just before the scene is closed."""
        # Parameter node will be reset, do not use it anymore
        self.setParameterNode(None)

    def onSceneEndClose(self, caller, event) -> None:
        """Called just after the scene is closed."""
        # If this module is shown while the scene is closed then recreate a new parameter node immediately
        if self.parent.isEntered:
            self.initializeParameterNode()

    def initializeParameterNode(self) -> None:
        """Ensure parameter node exists and observed."""
        # Parameter node stores all user choices in parameter values, node selections, etc.
        # so that when the scene is saved and reloaded, these settings are restored.

        self.setParameterNode(self.logic.getParameterNode())
        

    def setParameterNode(self, inputParameterNode: Optional[OralSurgModuleHomeParameterNode]) -> None:
        """
        Set and observe parameter node.
        Observation is needed because when the parameter node is changed then the GUI must be updated immediately.
        """

        if self._parameterNode:
            self._parameterNode.disconnectGui(self._parameterNodeGuiTag)
            self._parameterNode = inputParameterNode
        if self._parameterNode:
            # Note: in the .ui file, a Qt dynamic property called "SlicerParameterName" is set on each
            # ui element that needs connection.
            self._parameterNodeGuiTag = self._parameterNode.connectGui(self.ui)           
    

#
# OralSurgModuleHomeLogic
#


class OralSurgModuleHomeLogic(ScriptedLoadableModuleLogic):
    """This class should implement all the actual
    computation done by your module.  The interface
    should be such that other python code can import
    this class and make use of the functionality without
    requiring an instance of the Widget.
    Uses ScriptedLoadableModuleLogic base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self) -> None:
        """Called when the logic class is instantiated. Can be used for initializing member variables."""
        ScriptedLoadableModuleLogic.__init__(self)

    def getParameterNode(self):
        return OralSurgModuleHomeParameterNode(super().getParameterNode())

 
#
# OralSurgModuleHomeTest
#


class OralSurgModuleHomeTest(ScriptedLoadableModuleTest):
    pass
 
