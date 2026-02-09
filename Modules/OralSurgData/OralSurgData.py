import logging
import os
from typing import Annotated, Optional

import vtk
import ctk
import slicer
from slicer.i18n import tr as _
from slicer.i18n import translate
from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin
from slicer.parameterNodeWrapper import (
    parameterNodeWrapper,
    WithinRange,
)

import qt
import random

#
# OralSurgData
#


class OralSurgData(ScriptedLoadableModule):
    """Uses ScriptedLoadableModule base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = _("Oral Surgery Data")  
        self.parent.categories = [translate("qSlicerAbstractCoreModule", "Examples")]
        self.parent.dependencies = []  
        self.parent.contributors = ["Dimitris Trikeriotis (Gnathion)"]
        self.parent.helpText = _("""
To display and interact with data.
See more information in <a href="https://github.com/organization/projectname#OralSurgModuleHome">module documentation</a>.
""")
        
        self.parent.acknowledgementText = _("""
This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc., Andras Lasso, PerkLab,
and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
""")

       


# OralSurgDataParameterNode
#


@parameterNodeWrapper
class OralSurgDataParameterNode:
    pass
    
#
# OralSurgDataWidget
#


class OralSurgDataWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):
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
        uiWidget = slicer.util.loadUI(self.resourcePath("UI/OralSurgData.ui"))
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
        self.logic = OralSurgDataLogic()

        # Connections

        # These connections ensure that we update parameter node when scene is closed
        self.addObserver(slicer.mrmlScene, slicer.mrmlScene.StartCloseEvent, self.onSceneStartClose)
        self.addObserver(slicer.mrmlScene, slicer.mrmlScene.EndCloseEvent, self.onSceneEndClose)

        # Buttons
        
        self.FilterTreeItems()
        self.FilterTreeItems_2()

        self.ui.updatedata.connect("clicked(bool)", self.ondatatree)

        self.ui.updateimplants.connect("clicked(bool)", self.onimplantstree)

        self.greek()
        self.english()
        self.homeButton()
        self.widescreenButton()
        self.custom1screenButton()
        self.redcreenButton()
        self.dscreenButton()

        self.registButton()
        self.virtprButton()
        self.genimplButton()
        self.dentimButton()

        self.ui.grbutton.connect('clicked(bool)', self.OnGreek)
        self.ui.engbutton.connect('clicked(bool)', self.OnEnglish)

        self.ui.homeButton.connect("clicked(bool)", self.onhomeButton)
        self.ui.registButton.connect("clicked(bool)", self.onregistButton)
        self.ui.virtprButton.connect("clicked(bool)", self.onvirtprButton)
        self.ui.genimplButton.connect("clicked(bool)", self.ongenimplButton)
        self.ui.dentimButton.connect("clicked(bool)", self.ondentimButton)


        self.ui.widescreenButton.connect("clicked(bool)", self.onwidescreenButton)
        self.ui.custom1screenButton.connect("clicked(bool)", self.customlayout1)
        self.ui.redcreenButton.connect("clicked(bool)", self.onredcreenButton)
        self.ui.dscreenButton.connect("clicked(bool)", self.ondscreenButton)



        
        # Make sure parameter node is initialized (needed for module reload)
        self.initializeParameterNode()



    def greek(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "dagr.png"))        
        self.ui.grbutton.setIcon(icon)


    def english(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "daeng.png"))        
        self.ui.engbutton.setIcon(icon)  

    def homeButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "daOrSurgMod.png"))
        self.ui.homeButton.setIcon(icon)      


    def dentimButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "daDentImplIm.png"))
        self.ui.dentimButton.setIcon(icon)

    def registButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "daRegisterMod.png"))
        self.ui.registButton.setIcon(icon)


    def virtprButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "daVirtualPr.png"))
        self.ui.virtprButton.setIcon(icon)


    def genimplButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "daGenIImplCr.png"))
        self.ui.genimplButton.setIcon(icon)  
    
    def widescreenButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "daws.png"))        
        self.ui.widescreenButton.setIcon(icon)

    def custom1screenButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "dacs.png"))
        self.ui.custom1screenButton.setIcon(icon)


    def redcreenButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "dared.png"))
        self.ui.redcreenButton.setIcon(icon)

    def dscreenButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "da3d.png"))
        self.ui.dscreenButton.setIcon(icon)
        
    def onhomeButton(self):
        slicer.util.selectModule("OralSurgModuleHome")
        #slicer.util.reloadScriptedModule("OralSurgModuleHome")

    def onregistButton(self):
        slicer.util.selectModule("RegisterModule")
        #slicer.util.reloadScriptedModule("RegisterModule")

    def onvirtprButton(self):
        slicer.util.selectModule("VirtualProsth")
        #slicer.util.reloadScriptedModule("VirtualProsth")

    def ongenimplButton(self):
        slicer.util.selectModule("GenericImplCreator")
        #slicer.util.reloadScriptedModule("GenericImplCreator")
        
    def ondentimButton(self):
        slicer.util.selectModule("DentImplImaging")
        #slicer.util.reloadScriptedModule("DentImplImaging")


    


    def onwidescreenButton(self):
        slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutConventionalWidescreenView)

    def onredcreenButton(self):
        slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUpRedSliceView)

    def ondscreenButton(self):
        slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUp3DView) 



        


    def OnGreek(self):
    
        self.ui.implantsCollapsibleButton.setText("ΕΜΦΥΤΕΥΜΑΤΑ")
        self.ui. RestCollapsibleButton.setText("ΜΟΝΤΕΛΑ - ΣΗΜΕΙΑ - ΚΑΜΠΥΛΕΣ")
        self.ui. SegmentationCollapsibleButton.setText("ΚΑΤΑΤΜΗΣΕΙΣ")        
        self.ui.updateimplants.setText("ΕΝΗΜΕΡΩΣΗ")
        self.ui.updatedata.setText("ΕΝΗΜΕΡΩΣΗ")
        
    def OnEnglish(self):

        self.ui.implantsCollapsibleButton.setText("IMPLANTS")
        self.ui. RestCollapsibleButton.setText("MODELS - FIDUCIALS - CURVES")
        self.ui. SegmentationCollapsibleButton.setText("SEGMENTATIONS")        
        self.ui.updateimplants.setText("UPDATE")
        self.ui.updatedata.setText("UPDATE")        




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

        




















        


        

    def onimplantstree(self):
        self.FilterTreeItems()


    def ondatatree(self):
        self.FilterTreeItems_2()



    def FilterTreeItems(self):
        shNode = slicer.vtkMRMLSubjectHierarchyNode.GetSubjectHierarchyNode(slicer.mrmlScene)

        categoryName = "FilteredNodes"  # Unified category for both types

        # Assign category to relevant MODEL nodes
        for modelNode in slicer.util.getNodesByClass("vtkMRMLModelNode"):
            name = modelNode.GetName().lower()
            #if "implant" in name or "ring" in name or "axis" in name:            
            if any(keyword in name for keyword in ["implant", "ring", "axis"]):
                shItemID = shNode.GetItemByDataNode(modelNode)
                if shItemID:
                    shNode.SetItemAttribute(shItemID, "Category", categoryName)

        # Assign category to relevant TRANSFORM nodes
        for transformNode in slicer.util.getNodesByClass("vtkMRMLTransformNode"):
            name = transformNode.GetName().lower()
            #if any(keyword in name for keyword in ["unit"]):
            if "unit" in name:  # Only transforms with 'Unit' 
                shItemID = shNode.GetItemByDataNode(transformNode)
                if shItemID:
                    shNode.SetItemAttribute(shItemID, "Category", categoryName)

        # Refresh the subject hierarchy tree filter
        tree = self.ui.ImplantSubjectHierarchyTreeView
        tree.setMRMLScene(None)  # Temporarily detach to clear previous filters
        tree.addItemAttributeFilter("Category", categoryName)  # Apply updated filter
        tree.setContextMenuEnabled(True)
        tree.setMRMLScene(slicer.mrmlScene)  # Re-attach scene to refresh
        


    def FilterTreeItems_2(self):
            shNode = slicer.vtkMRMLSubjectHierarchyNode.GetSubjectHierarchyNode(slicer.mrmlScene)

            categoryName = "FilteredNodes_2"  # Unified category for both types

            # Assign category to relevant MODEL nodes
            for modelNode in slicer.util.getNodesByClass("vtkMRMLModelNode"):
                name = modelNode.GetName().lower()
                if any(keyword in name for keyword in ["maxilla", "mandible", "upper", "lower", "canal", "model", "v", "guide", "occlusion","remeshed","undercutSurface","hollowedundercut","guidebase"]):               
                    shItemID = shNode.GetItemByDataNode(modelNode)
                    if shItemID:
                        shNode.SetItemAttribute(shItemID, "Category", categoryName)

            # Assign category to relevant TRANSFORM nodes
            for markupsNode in slicer.util.getNodesByClass("vtkMRMLMarkupsFiducialNode"):
                name = markupsNode.GetName().lower()
                if any(keyword in name for keyword in ["p", "mark"]):  
                    shItemID = shNode.GetItemByDataNode(markupsNode)
                    if shItemID:
                        shNode.SetItemAttribute(shItemID, "Category", categoryName)

            # Assign category to relevant TRANSFORM nodes
            for markupsNode in slicer.util.getNodesByClass("vtkMRMLMarkupsCurveNode"):
                name = markupsNode.GetName().lower()
                if any(keyword in name for keyword in ["c"]):  
                    shItemID = shNode.GetItemByDataNode(markupsNode)
                    if shItemID:
                        shNode.SetItemAttribute(shItemID, "Category", categoryName)

                       

            # Refresh the subject hierarchy tree filter
            tree = self.ui.Rest2SubjectHierarchyTreeView
            tree.setMRMLScene(None)  # Temporarily detach to clear previous filters
            tree.addItemAttributeFilter("Category", categoryName)  # Apply updated filter
            tree.setContextMenuEnabled(True)
            tree.setMRMLScene(slicer.mrmlScene)  # Re-attach scene to refresh


        

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

      

    def setParameterNode(self, inputParameterNode: Optional[OralSurgDataParameterNode]) -> None:
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
# OralSurgDataLogic
#


class OralSurgDataLogic(ScriptedLoadableModuleLogic):
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
        return OralSurgDataParameterNode(super().getParameterNode())

   
#
# OralSurgDataTest
#


class OralSurgDataTest(ScriptedLoadableModuleTest):
    pass
   
