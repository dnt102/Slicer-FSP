import logging
import os
from typing import Annotated, Optional
import qt
import vtk
import time
import ctk
from vtk.util import numpy_support  # Correct import for conversion
import pyacvd
import pyvista as pv
import re
import math
import csv
import slicer
from slicer.i18n import tr as _
from slicer.i18n import translate
from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin
from slicer.parameterNodeWrapper import (
    parameterNodeWrapper,
    WithinRange,
)

from slicer import vtkMRMLScalarVolumeNode
from qt import QButtonGroup
import numpy as np
import random


#
# RegisterModule
#


class RegisterModule(ScriptedLoadableModule):
    """Uses ScriptedLoadableModule base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = _("Registation Module")  
        self.parent.categories = [translate("qSlicerAbstractCoreModule", "Examples")]
        self.parent.dependencies = []  
        self.parent.contributors = ["Dimitris Trikeriotis (Gnathion)"]  
        self.parent.helpText = _("""
To align scan models with CBCT data and prepare for prosthetic/implant simulation and surgical guide design.
See more information in <a href="https://github.com/organization/projectname#RegisterModule">module documentation</a>.
""")
        self.parent.acknowledgementText = _("""
This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc., Andras Lasso, PerkLab,
and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
""")


#
# RegisterModuleParameterNode

'''
The parameters needed by the module.
RegisteSubjectHierarchyTreeView was commented out
because of the error: "Unable to create serializer for {classtype} member {name}")
probably due to the fact that no GUI connector is yet available. Fix????
'''
@parameterNodeWrapper
class RegisterModuleParameterNode:

    scancomboBox:str = "None"
    listWidget:str = "None"
    targetpointselector:slicer.vtkMRMLMarkupsFiducialNode=None
    sourcepointselector:slicer.vtkMRMLMarkupsFiducialNode=None
    sourcemodelselector:slicer.vtkMRMLModelNode=None
    XYanglethresholdSlider:Annotated[int, WithinRange(0, 180)] = 0
    XanglethresholdSlider:Annotated[int, WithinRange(0, 180)] = 0
    YanglethresholdSlider:Annotated[int, WithinRange(0, 180)] = 0
    ZanglethresholdSlider:Annotated[int, WithinRange(0, 180)] = 0
    anglethresholdSpinBox:Annotated[int, WithinRange(0, 99)] = 0
    XYundercutcheckBox: bool = False
    XundercutcheckBox: bool = False
    YundercutcheckBox: bool = False
    ZundercutcheckBox: bool = False
    #RegisteSubjectHierarchyTreeView:slicer.qMRMLSubjectHierarchyTreeView= None

'''
Because of the error:AttributeError: 'dict' object has no attribute '__dict__'
instead of passing a dictionary directly to connectGui()
an object/class (self.ui) is used, that contains all the named widgets.
'''

class RegisterModuleGui:
    
    def __init__(self, ui):
        
        self.scancomboBox = ui.scancomboBox
        self.listWidget = ui.listWidget        
        self.targetpointselector = ui.targetpointselector
        self.sourcepointselector = ui.sourcepointselector
        self.sourcemodelselector = ui.sourcemodelselector        
        self.XYanglethresholdSlider = ui.XYanglethresholdSlider
        self.XanglethresholdSlider = ui.XanglethresholdSlider
        self.YanglethresholdSlider = ui.YanglethresholdSlider
        self.ZanglethresholdSlider = ui.ZanglethresholdSlider        
        self.anglethresholdSpinBox = ui.anglethresholdSpinBox        
        self. XYundercutcheckBox = ui. XYundercutcheckBox
        self. XundercutcheckBox = ui. XundercutcheckBox
        self. YundercutcheckBox = ui. YundercutcheckBox
        self. ZundercutcheckBox = ui. ZundercutcheckBox        
        #self.RegisteSubjectHierarchyTreeView = ui.RegisteSubjectHierarchyTreeView

#
# RegisterModuleWidget
#


class RegisterModuleWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):


    greek_to_latin = {
            'Α':'A','Β':'V','Γ':'G','Δ':'D','Ε':'E','Ζ':'Z','Η':'I','Θ':'Th',
            'Ι':'I','Κ':'K','Λ':'L','Μ':'M','Ν':'N','Ξ':'X','Ο':'O','Π':'P',
            'Ρ':'R','Σ':'S','Τ':'T','Υ':'Y','Φ':'F','Χ':'Ch','Ψ':'Ps','Ω':'O',
            'α':'a','β':'v','γ':'g','δ':'d','ε':'e','ζ':'z','η':'i','θ':'th',
            'ι':'i','κ':'k','λ':'l','μ':'m','ν':'n','ξ':'x','ο':'o','π':'p',
            'ρ':'r','σ':'s','ς':'s','τ':'t','υ':'y','φ':'f','χ':'ch','ψ':'ps','ω':'o',
            'ά':'a','έ':'e','ί':'i','ό':'o','ύ':'y','ή':'i','ώ':'o',
            'ϊ':'i','ΐ':'i','ϋ':'y','ΰ':'y'
        }

    def greek_to_latin_transliterate(self, text):
        return ''.join(self.greek_to_latin.get(ch, ch) for ch in text)
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
        uiWidget = slicer.util.loadUI(self.resourcePath("UI/RegisterModule.ui"))
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
        self.logic = RegisterModuleLogic()

        # These connections ensure that we update parameter node when scene is closed
        self.addObserver(slicer.mrmlScene, slicer.mrmlScene.StartCloseEvent, self.onSceneStartClose)
        self.addObserver(slicer.mrmlScene, slicer.mrmlScene.EndCloseEvent, self.onSceneEndClose)

        #Buttons and other connections

        self.ui.grbutton.connect('clicked(bool)', self.OnGreek)
        self.ui.engbutton.connect('clicked(bool)', self.OnEnglish)
        self.ui.homeButton.connect("clicked(bool)", self.onhomeButton)

        self.ui.targetpointselector.nodeAdded.connect(self.onnewtargetpoint)
        self.ui.sourcepointselector.nodeAdded.connect(self.onnewsourcepoint)
        self.ui.fidreg.connect("clicked(bool)", self.onfidreg)
        self.ui.undofidreg.connect("clicked(bool)", self.onundofidreg)
        self.ui.hardenfidreg.connect("clicked(bool)", self.onhardenfidreg)
        self.ui.loadscanButton.connect("clicked(bool)", self.loadscanmodel)
        self.ui.scanmodelrepairButton.connect("clicked(bool)", self.OnscanmodelrepairButton)

        self.ui.widescreenButton.connect("clicked(bool)", self.onwidescreenButton)
        self.ui.custom1screenButton.connect("clicked(bool)", self.customlayout1)
        self.ui.redcreenButton.connect("clicked(bool)", self.onredcreenButton)
        self.ui.dscreenButton.connect("clicked(bool)", self.ondscreenButton)

        self.ui.modelpointreeButton.connect("clicked(bool)", self.onmodelpointreeButton)

        self.widescreenButton()
        self.custom1screenButton()
        self.redcreenButton()
        self.dscreenButton()
       
        self.retrievepatient()
        self.FilterTreeItems_3()
        self.findscanmodel()        

        self.ui.XundercutcheckBox.stateChanged.connect(self.onXundercutcheckBox)
        self.ui.YundercutcheckBox.stateChanged.connect(self.onYundercutcheckBox)
        self.ui.ZundercutcheckBox.stateChanged.connect(self.onZundercutcheckBox)
        self.ui.XYundercutcheckBox.stateChanged.connect(self.onXYundercutcheckBox)
        self.ui.XanglethresholdSlider.valueChanged.connect(self.undercutX)
        self.ui.YanglethresholdSlider.valueChanged.connect(self.undercutY)
        self.ui.ZanglethresholdSlider.valueChanged.connect(self.undercutZ)
        self.ui.XYanglethresholdSlider.valueChanged.connect(self.undercutXY)     

        self.ui.minus70XYButtton.connect("clicked(bool)", self.onminus70XYButtton)

        self.ui.U_undercutsblockButton.connect("clicked(bool)", self.onUpper_undercutsblockButton)
        self.ui.L_undercutsblockButton.connect("clicked(bool)", self.onLower_undercutsblockButton)
        self.ui.ModelPlusUndercutsButton.connect("clicked(bool)", self.OnModelPlusUndercutsButton)

        self.greek()
        self.english()
        self.homeButton()

        self.ui.dentimButton.connect("clicked(bool)", self.ondentimButton)        
        self.ui.virtprButton.connect("clicked(bool)", self.onvirtprButton)
        self.ui.genimplButton.connect("clicked(bool)", self.ongenimplButton)

        self.dentimButton()        
        self.virtprButton()
        self.genimplButton()
        

        self.ui.patientnamelabel.hide()


        self.dataButton()
        self.ui.databutton.connect("clicked(bool)", self.ondataButton)    


        
        
        #Make sure parameter node is initialized (needed for module reload)
        self.initializeParameterNode()


    def dataButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "rmOSData.png"))
        self.ui.databutton.setIcon(icon)           
    
    def ondataButton(self):
        slicer.util.selectModule("OralSurgData")
        slicer.util.reloadScriptedModule("OralSurgData")

        

    def onmodelpointreeButton(self):
        self.FilterTreeItems_3()  

    def dentimButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "rmDentImplIm.png"))
        self.ui.dentimButton.setIcon(icon)

    def virtprButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "rmVirtualPr.png"))
        self.ui.virtprButton.setIcon(icon)

    def genimplButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "rmGenIImplCr.png"))
        self.ui.genimplButton.setIcon(icon)
        

    def ondentimButton(self):
        slicer.util.selectModule("DentImplImaging")
        #slicer.util.reloadScriptedModule("DentImplImaging")

    def onvirtprButton(self):
        slicer.util.selectModule("VirtualProsth")
        #slicer.util.reloadScriptedModule("VirtualProsth")

    def ongenimplButton(self):
        slicer.util.selectModule("GenericImplCreator")
        #slicer.util.reloadScriptedModule("GenericImplCreator")
 

    def homeButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "rmOrSurgMod.png"))
        self.ui.homeButton.setIcon(icon)
        
    def onhomeButton(self):
        slicer.util.selectModule("OralSurgModuleHome")
        #slicer.util.reloadScriptedModule("OralSurgModuleHome")   

    def greek(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "rmgr.png"))        
        self.ui.grbutton.setIcon(icon)


    def english(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "rmeng.png"))        
        self.ui.engbutton.setIcon(icon)


    def OnGreek(self):
    
        self.ui.regCollapsibleButton.setText("Ευθυγράμμιση μοντέλου σάρωσης με CBCT")        
        self.ui.loadscanButton.setText("Εισαγωγή Μοντέλου Σάρωσης")        
        self.ui.label_29.setText("Σημεία στο σταθερό(στόχος¨):")        
        self.ui.label_28.setText("Σημεία στο κινητό(πηγή)::")        
        self.ui.label_40.setText("Μοντέλο:")        
        self.ui.fidreg.setText("Υπολογισμός")        
        self.ui.undofidreg.setText("Αναίρεση")        
        self.ui.hardenfidreg.setText("Ολοκλήρωση Ευθυγράμισης")        
        self.ui.scanmodelrepairButton.setText("Επιδιόρθωση Μοντέλου")        
        self.ui.label_2.setText("Υποσκαφές στους άξονες XY:")        
        self.ui.label_3.setText("Υποσκαφές στον άξονα X:")        
        self.ui.label_4.setText("Υποσκαφές στον άξονα Y:")        
        self.ui.label_5.setText("Υποσκαφές στον άξονα Z:")        
        self.ui.minus70XYButtton.setText("Υποσκαφές στους άξονες XY(30°)")
        self.ui.U_undercutsblockButton.setText("Block Υποσκαφών(Άνω Γνάθος)")
        self.ui.L_undercutsblockButton.setText("Block Υποσκαφών(Κάτω Γνάθος)")
        self.ui.ModelPlusUndercutsButton.setText("Δημιουργία Βάσης Χειρουργικού Οδηγού") 


    def OnEnglish(self):

        self.ui.regCollapsibleButton.setText("Scan model registration to CBCT")        
        self.ui.loadscanButton.setText("Import Scan Model")        
        self.ui.label_29.setText("Points on fixed(target):")        
        self.ui.label_28.setText("Points on moving(source)::")        
        self.ui.label_40.setText("Model:")
        self.ui.fidreg.setText("Compute:")        
        self.ui.undofidreg.setText("Undo:")        
        self.ui.hardenfidreg.setText("Harden Alignment:")        
        self.ui.scanmodelrepairButton.setText("Repair Model:")        
        self.ui.label_2.setText("Undercuts on XY axes:")        
        self.ui.label_3.setText("Undercuts on X axis:")        
        self.ui.label_4.setText("Undercuts on Y axis:")        
        self.ui.label_5.setText("Undercuts on Z axis:")        
        self.ui.minus70XYButtton.setText("Undercuts(XY/30 deg)")
        self.ui.U_undercutsblockButton.setText("Upper Undercuts Block")
        self.ui.L_undercutsblockButton.setText("Lower Undercuts Block")
        self.ui.ModelPlusUndercutsButton.setText("Create Surgical Guide Base")


    def widescreenButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "rmws.png"))        
        self.ui.widescreenButton.setIcon(icon)

    def custom1screenButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "rmcs.png"))
        self.ui.custom1screenButton.setIcon(icon)

    def redcreenButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "rmred.png"))
        self.ui.redcreenButton.setIcon(icon)

    def dscreenButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "rm3d.png"))
        self.ui.dscreenButton.setIcon(icon)  

    def onwidescreenButton(self):
        slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutConventionalWidescreenView)

    def onredcreenButton(self):
        slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUpRedSliceView)

    def ondscreenButton(self):
        slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUp3DView)   

    def retrievepatient(self):
        patient_itemList = []
        shNode = slicer.vtkMRMLSubjectHierarchyNode.GetSubjectHierarchyNode(slicer.mrmlScene)

        # Get all items in scene hierarchy
        allItemIDs = vtk.vtkIdList()
        shNode.GetItemChildren(shNode.GetSceneItemID(), allItemIDs, True)

        # Find first patient name
        patient_name = None
        for i in range(allItemIDs.GetNumberOfIds()):
            itemID = allItemIDs.GetId(i)
            level = shNode.GetItemLevel(itemID)
            if level == "Patient":
                patient_name = shNode.GetItemName(itemID)
                patient_itemList.append(patient_name)
                print(patient_itemList)
                break

        if not patient_itemList:
            logging.warning("Δεν υπάρχει εξέταση ασθενή! - No patient found in the current scene!")
            return

        patientName = (patient_itemList[0])[:20]

        # Μετατροπή ελληνικών χαρακτήρων σε λατινικούς
        latinPatientName = self.greek_to_latin_transliterate(patientName)

        # Sanitize patient name for filesystem
        safePatientName = re.sub(r'[^A-Za-z0-9_\- ]+', '_', latinPatientName).strip()
        print("Sanitized patient name:", safePatientName)

        # Update label in UI
        self.ui.patientnamelabel.setText(safePatientName)

        # Base directories
        slicer_base = slicer.app.slicerHome
        path = os.path.join(slicer_base, "red_slice", safePatientName)
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            print("The new directory:", path, "already exists and so it is not created!")

        # Retrieve Volume Info
        volumeNode = slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLScalarVolumeNode")
        if not volumeNode:
            slicer.util.errorDisplay("Δεν υπάρχει CT για τον ασθενή! - No volume loaded for this patient!")
            return

        imageData = volumeNode.GetImageData()
        if not imageData:
            slicer.util.errorDisplay("Δεν υπάρχουν εικόνες στην εξέταση! - Volume has no image data!")
            return



    def findscanmodel(self):       


        #path = 'C:/Users/dnt10/Downloads/'
        path = os.path.join(os.environ['USERPROFILE'], 'Downloads')

        # Name filters
        name_filters = ["upper", "lower", "occlusion"]

        # Allowed extensions
        valid_exts = [".stl", ".obj", ".ply"]

        self.ui.scancomboBox.clear()  # Clear previous entries

        for item in os.listdir(path):
            itemLower = item.lower()  # Case-insensitive
            # Check if name matches AND extension is allowed
            if any(tag in itemLower for tag in name_filters) and any(itemLower.endswith(ext) for ext in valid_exts):
                print("Adding:", item)
                self.ui.scancomboBox.addItem(item)
        self.ui.scancomboBox.addItem('None')
        self.ui.scancomboBox.currentText='None' 


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

            

    def loadscanmodel(self):
        import os
        import vtk

        # Define path and filename
        path = os.path.join(os.environ['USERPROFILE'], 'Downloads')
        filename = os.path.join(path, self.ui.scancomboBox.currentText)
        print(f"Loading model from: {filename}")

        # Load model
        modelNode = slicer.util.loadModel(filename, returnNode=False)

        if modelNode:
            # Convert from LPS to RAS by flipping X and Y axes
            lpsToRasTransform = vtk.vtkTransform()
            lpsToRasTransform.Scale(-1, -1, 1)

            transformFilter = vtk.vtkTransformPolyDataFilter()
            transformFilter.SetTransform(lpsToRasTransform)
            transformFilter.SetInputData(modelNode.GetPolyData())
            transformFilter.Update()

            modelNode.SetAndObservePolyData(transformFilter.GetOutput())

            # Update UI and display
            self.ui.sourcemodelselector.setCurrentNode(modelNode)
            displayNode = modelNode.GetDisplayNode()
            displayNode.SetOpacity(1.0)
            displayNode.SetVisibility2D(True)

            self.FilterTreeItems_3()

        else:
            slicer.util.errorDisplay(f"Failed to load model from {filename}")


    def FilterTreeItems_3(self):
        shNode = slicer.vtkMRMLSubjectHierarchyNode.GetSubjectHierarchyNode(slicer.mrmlScene)

        categoryName = "FilteredNodes_3"  # Unified category for both types

        # Assign category to relevant MODEL nodes
        for modelNode in slicer.util.getNodesByClass("vtkMRMLModelNode"):
            name = modelNode.GetName().lower()  
            if any(keyword in name for keyword in ["maxilla", "mandible", "upper", "lower", "canal","occlusion","Remeshed","UndercutSurface","HollowedUndercut","GuideBase","model"]):
                shItemID = shNode.GetItemByDataNode(modelNode)
                if shItemID:
                    shNode.SetItemAttribute(shItemID, "Category", categoryName)

        # Assign category to relevant Markups nodes
        for markupsNode in slicer.util.getNodesByClass("vtkMRMLMarkupsFiducialNode"):
            name = markupsNode.GetName().lower()
            if any(keyword in name for keyword in ["p", "mark"]):            
                shItemID = shNode.GetItemByDataNode(markupsNode)
                if shItemID:
                    shNode.SetItemAttribute(shItemID, "Category", categoryName)

        # Refresh the subject hierarchy tree filter
        tree = self.ui.RegisteSubjectHierarchyTreeView
        tree.setMRMLScene(None)  # Temporarily detach to clear previous filters
        tree.addItemAttributeFilter("Category", categoryName)  # Apply updated filter
        tree.setContextMenuEnabled(True)
        tree.setMRMLScene(slicer.mrmlScene)  # Re-attach scene to refresh



    def onnewtargetpoint(self):
            placeModePersistence = 1
            slicer.modules.markups.logic().StartPlaceMode(placeModePersistence) # Ensure 'Place multiple control points' is active
       
    def onnewsourcepoint(self):
        placeModePersistence = 1
        slicer.modules.markups.logic().StartPlaceMode(placeModePersistence) # Ensure 'Place multiple control points' is active        


    def onfidreg(self)-> None: 

        model_to_reg=self.ui.sourcemodelselector.currentNode().GetName()
        # Get fiducial nodes
        targetnode=self.ui.targetpointselector.currentNode().GetName()
        print(targetnode)
        sourcenode=self.ui.sourcepointselector.currentNode().GetName()
        print(sourcenode)
        fiducialNode1 = slicer.util.getNode(sourcenode)
        fiducialNode2 = slicer.util.getNode(targetnode)

         # Ensure the number of fiducials is the same
        nPoints1 = fiducialNode1.GetNumberOfControlPoints()
        nPoints2 = fiducialNode2.GetNumberOfControlPoints()
        if nPoints1 != nPoints2:
            raise ValueError("Fiducial lists do not have the same number of points.")
        # Extract fiducial coordinates
        points1 = np.zeros((nPoints1, 3))
        points2 = np.zeros((nPoints2, 3))
        for i in range(nPoints1):
            fiducialNode1.GetNthControlPointPosition(i, points1[i])
            fiducialNode2.GetNthControlPointPosition(i, points2[i])
        # Create VTK point sets
        sourcePoints = vtk.vtkPoints()
        targetPoints = vtk.vtkPoints()
        for i in range(nPoints1):
            sourcePoints.InsertNextPoint(points1[i])
            targetPoints.InsertNextPoint(points2[i])
        # Perform the registration using vtkLandmarkTransform
        landmarkTransform = vtk.vtkLandmarkTransform()
        landmarkTransform.SetSourceLandmarks(sourcePoints)
        landmarkTransform.SetTargetLandmarks(targetPoints)
        landmarkTransform.SetModeToRigidBody()  # Use Rigid Body, Similarity, or Affine as needed
        landmarkTransform.Update()
        # Apply the transform to the source model
        transformMatrix = vtk.vtkMatrix4x4()
        landmarkTransform.GetMatrix(transformMatrix)
        transformNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode", "FiducialRegistrationTransform")
        transformNode.SetMatrixTransformToParent(transformMatrix)

        sourceModel = slicer.util.getNode(model_to_reg)  # Replace with the name of your source model-moving
        sourcefiducialNode = slicer.util.getNode(sourcenode)  # Replace 
        sourceModel.SetAndObserveTransformNodeID(transformNode.GetID())
        sourcefiducialNode.SetAndObserveTransformNodeID(transformNode.GetID())
        print(sourcefiducialNode.SetAndObserveTransformNodeID(transformNode.GetID()))
        self.FilterTreeItems_3()

        self.oncalcdist()
        
    def onundofidreg(self)-> None:
        # Get the TransformNode by name (replace 'TransformName' with your transform node's name)
        transformNode = slicer.util.getNode('FiducialRegistrationTransform')

        # Check if the node exists
        if transformNode:
           slicer.mrmlScene.RemoveNode(transformNode)  #Remove the node from the scene
           self.FilterTreeItems_3()
        else:
            print("Transform node not found.")
       

    def onhardenfidreg(self)-> None:
        
        # Get the model node (replace 'ModelName' with your model node's name)
        model_to_harden=((self.ui.sourcemodelselector.currentNode()).GetName())
        modelNode = slicer.util.getNode(model_to_harden)

        # Check if the model node exists
        if modelNode:
            modelNode.HardenTransform() # Apply the harden transform
            print("Transform has been hardened for model")
        else:
            print("Model node not found.")

        targetnode=self.ui.targetpointselector.currentNode().GetName()
        print(targetnode)
        sourcenode=self.ui.sourcepointselector.currentNode().GetName()
        print(sourcenode)
        fiducialNode1 = slicer.util.getNode(sourcenode)
        fiducialNode2 = slicer.util.getNode(targetnode)
        slicer.mrmlScene.RemoveNode(fiducialNode1)
        slicer.mrmlScene.RemoveNode(fiducialNode2)
        
             
    def oncalcdist(self)-> None:        

        # Function to compute distances between transformed source points and target points
        def computeDistancesBetweenFiducials(sourceFiducialName, targetFiducialName):
            # Get the source and target fiducial nodes

            targetnode=self.ui.targetpointselector.currentNode().GetName()
            print(targetnode)
            sourcenode=self.ui.sourcepointselector.currentNode().GetName()
            print(sourcenode)
            
            sourceFiducialNode = slicer.util.getNode(sourcenode)
            targetFiducialNode = slicer.util.getNode(targetnode)

            if not sourceFiducialNode or not targetFiducialNode:
                print("Error: Source or Target Fiducial node not found.")
                return

            # Check if both fiducial nodes have the same number of control points
            if sourceFiducialNode.GetNumberOfControlPoints() != targetFiducialNode.GetNumberOfControlPoints():
                print("Error: Source and Target Fiducial nodes have a different number of control points.")
                return

            # Get the parent transform node for the source fiducial
            #sourceTransformNode = sourceFiducialNode.GetParentTransformNode()
            sourceTransformNode  = slicer.util.getNode('FiducialRegistrationTransform')

            # Initialize a list to store distances
            distances = []

            # Loop through all control points
            for i in range(sourceFiducialNode.GetNumberOfControlPoints()):
                # Get the source control point's original coordinates
                sourceOriginalCoordinates = np.zeros(3)
                sourceFiducialNode.GetNthControlPointPosition(i, sourceOriginalCoordinates)

                # Initialize transformed coordinates for the source point
                sourceTransformedCoordinates = np.zeros(3)

                if sourceTransformNode:
                    # Apply the parent transform to get the transformed source coordinates
                    sourceTransformMatrix = vtk.vtkMatrix4x4()
                    sourceTransformNode.GetMatrixTransformToWorld(sourceTransformMatrix)
                    sourceTransformedCoordinates = sourceTransformMatrix.MultiplyPoint(
                        np.append(sourceOriginalCoordinates, 1.0)
                    )[:3]
                else:
                    # If no transform, transformed coordinates are the same as the original
                    sourceTransformedCoordinates = sourceOriginalCoordinates

                # Get the target control point's coordinates
                targetCoordinates = np.zeros(3)
                targetFiducialNode.GetNthControlPointPosition(i, targetCoordinates)

                # Compute the distance between the transformed source and target points
                distance = np.linalg.norm(sourceTransformedCoordinates - targetCoordinates)
                distances.append(distance)
  
                print(f"   {i}: {distance}")

            meanDistance = np.mean(distances)
            
            #self.ui.label.text=(i, distances[i])                      
            print("Mean distance:", meanDistance)

            # Clear the list widget before adding new results
            self.ui.listWidget.clear()

            # Loop through distances and add them to the list widget
            for i, distance in enumerate(distances):
                self.ui.listWidget.addItem(f"Point {i}: {distance:.3f} mm")

            # Add the mean distance as the last item
            self.ui.listWidget.addItem(f"Mean distance: {meanDistance:.3f} mm")

            # Optionally, display a message if the mean distance is below a threshold
                       
            if meanDistance <= 0.2:
                slicer.util.infoDisplay("Μέση απόκλιση(Mean distance) < 0.2 mm!") 
            
            return distances

        # Example usage

        targetnode=self.ui.targetpointselector.currentNode().GetName()
        print(targetnode)
        sourcenode=self.ui.sourcepointselector.currentNode().GetName()
        print(sourcenode)

        sourceFiducialName = slicer.util.getNode(sourcenode)  # Replace with the name of your source fiducial node
        targetFiducialName = slicer.util.getNode(targetnode)  # Replace with the name of your target fiducial node
        computeDistancesBetweenFiducials(sourceFiducialName, targetFiducialName)


    def remesh_with_pyacvd(self, model_node, number_of_points=2000, subdivision_level=1):
        
        try:
            start_time = time.time()
            
            # Get input polydata
            input_polydata = model_node.GetPolyData()
            print(f"Original mesh: {input_polydata.GetNumberOfPoints()} points")

            # Initial decimation
            decimator = vtk.vtkQuadricDecimation()
            decimator.SetInputData(input_polydata)
            decimator.SetTargetReduction(0.9)
            decimator.Update()
            simplified_poly = decimator.GetOutput()
            print(f"Decimated to: {simplified_poly.GetNumberOfPoints()} points")

            # Convert to PyVista mesh and pre-process
            pv_mesh = pv.wrap(simplified_poly)
            print("Filling holes...")
            pv_mesh = pv_mesh.triangulate().clean().fill_holes(1000)  # Added hole filling
            
            # Setup clustering
            print("Initializing clustering...")
            cluster = pyacvd.Clustering(pv_mesh)
            
            print(f"Subdividing (level {subdivision_level})...")
            cluster.subdivide(subdivision_level)
            
            print(f"Clustering to {number_of_points} points...")
            slicer.app.processEvents()
            cluster.cluster(number_of_points)
            
            # Get remeshed mesh
            remeshed_pv_mesh = cluster.create_mesh()
            points = remeshed_pv_mesh.points
            faces = remeshed_pv_mesh.faces.reshape(-1, 4)[:, 1:4]
            
            # Convert points using VTK's numpy_support
            vtk_points = vtk.vtkPoints()
            vtk_array = numpy_support.numpy_to_vtk(points, deep=True)  # Correct conversion
            vtk_points.SetData(vtk_array)
            
            # Create VTK polydata
            vtk_poly = vtk.vtkPolyData()
            vtk_poly.SetPoints(vtk_points)
            
            cells = vtk.vtkCellArray()
            for face in faces:
                if len(face) == 3:
                    triangle = vtk.vtkTriangle()
                    triangle.GetPointIds().SetId(0, face[0])
                    triangle.GetPointIds().SetId(1, face[1])
                    triangle.GetPointIds().SetId(2, face[2])
                    cells.InsertNextCell(triangle)
            vtk_poly.SetPolys(cells)
            
            print(f"Remeshed to: {vtk_poly.GetNumberOfPoints()} points")

            # Create output node
            remeshed_model = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelNode", 
                                                             f"{model_node.GetName()}_Remeshed")
            remeshed_model.SetAndObservePolyData(vtk_poly)
            remeshed_model.CreateDefaultDisplayNodes()
            
            print(f"Completed in {time.time()-start_time:.1f} seconds")
            return remeshed_model

        except Exception as e:
            slicer.util.errorDisplay(f"Remeshing failed at step: {str(e)}")
            return None


    def OnscanmodelrepairButton(self):
         
        model_to_repair=self.ui.sourcemodelselector.currentNode().GetName()        
        self.model_node = slicer.util.getNode(model_to_repair)
        
        self.remeshed_model = self.remesh_with_pyacvd(
            self.model_node,
            number_of_points=60000,  # Start very small
            subdivision_level=1
        )
        self.model_node.GetDisplayNode().SetVisibility(False)
        if self.remeshed_model:
            self.ui.sourcemodelselector.setCurrentNode(self.remeshed_model)
            displayNode = self.remeshed_model.GetDisplayNode()
            displayNode.SetOpacity(1.0)  # Set opacity to fully opaque
            displayNode.SetVisibility2D(True)  # Set opacity to fully opaque
            self.FilterTreeItems_3()


    def undercutX(self):

        
        self.ui.YanglethresholdSlider.value=0
        self.ui.ZanglethresholdSlider.value=0
        self.ui.XYanglethresholdSlider.value=0

        self.ui.YundercutcheckBox.setChecked(False)
        self.ui.ZundercutcheckBox.setChecked(False)
        self.ui.XYundercutcheckBox.setChecked(False)
        
        # Get remeshed model       

        model_to_undercut=self.ui.sourcemodelselector.currentNode().GetName()        
        originalModelNode = slicer.util.getNode(model_to_undercut)
        originalPolyData = originalModelNode.GetPolyData()
        
        existingUndercutNode = slicer.mrmlScene.GetFirstNodeByName("UndercutSurface")
        if existingUndercutNode:
            slicer.mrmlScene.RemoveNode(existingUndercutNode)     
 
        # Compute normals if missing
        if not originalPolyData.GetPointData().GetNormals():
            print("Computing normals for remeshed model...")
            normals_filter = vtk.vtkPolyDataNormals()
            normals_filter.SetInputData(originalPolyData)
            normals_filter.ComputePointNormalsOn()
            normals_filter.Update()
            originalPolyData = normals_filter.GetOutput()

        # Normalize tool direction properly
        toolDirection = np.array([1.0, 0.0, 0.0], dtype=np.float64)  # Explicit float type
        tool_norm = np.linalg.norm(toolDirection)
        if tool_norm > 1e-6:  # Prevent division by zero
            toolDirection /= tool_norm
        else:
            raise ValueError("Tool direction vector is zero-length")

        thresholdAngle = self.ui.anglethresholdSpinBox.value   # Degrees

        undercutPoints = []
        normals = originalPolyData.GetPointData().GetNormals()

        for i in range(originalPolyData.GetNumberOfPoints()):
            # Get and normalize normal vector
            normal = np.array(normals.GetTuple3(i), dtype=np.float64)
            normal_norm = np.linalg.norm(normal)
            if normal_norm > 1e-6:
                normal /= normal_norm
            else:
                continue  # Skip invalid normals
            
            # Calculate angle safely
            cos_theta = np.dot(normal, toolDirection)
            cos_theta = np.clip(cos_theta, -1.0, 1.0)  # Prevent numerical errors
            theta = np.arccos(cos_theta) * (180 / np.pi)
            
            if theta > thresholdAngle:
                undercutPoints.append(i)


        # Continue with cell extraction as before...
        # Now create the undercut surface model from the ORIGINAL mesh
        # (Not from NormalsVisualization)
        undercutPointSet = set(undercutPoints)
        newCells = vtk.vtkCellArray()

        for i in range(originalPolyData.GetNumberOfCells()):
            cell = originalPolyData.GetCell(i)
            if cell.GetCellType() != vtk.VTK_TRIANGLE:
                continue
            # Check if any vertex of the triangle is an undercut point
            pid0 = cell.GetPointId(0)
            pid1 = cell.GetPointId(1)
            pid2 = cell.GetPointId(2)
            if pid0 in undercutPointSet or pid1 in undercutPointSet or pid2 in undercutPointSet:
                newCells.InsertNextCell(cell)

        # Create the undercut surface polydata
        undercutSurfacePolyData = vtk.vtkPolyData()
        undercutSurfacePolyData.SetPoints(originalPolyData.GetPoints())  # Original points
        undercutSurfacePolyData.SetPolys(newCells)  # Filtered triangles

        # Clean unused points (optional but recommended)
        cleanFilter = vtk.vtkCleanPolyData()
        cleanFilter.SetInputData(undercutSurfacePolyData)
        cleanFilter.Update()
        cleanedPolyData = cleanFilter.GetOutput()

        # Add to 3D Slicer
        undercutSurfaceNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelNode", "UndercutSurface")
        undercutSurfaceNode.SetAndObservePolyData(cleanedPolyData)

        # Configure display
        undercutSurfaceDisplayNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelDisplayNode")
        undercutSurfaceDisplayNode.SetColor(1, 0, 0)  # Red
        undercutSurfaceDisplayNode.SetOpacity(1.0)
        undercutSurfaceDisplayNode.SetVisibility(True)
        undercutSurfaceNode.SetAndObserveDisplayNodeID(undercutSurfaceDisplayNode.GetID())

        slicer.util.forceRenderAllViews()

    def onXundercutcheckBox(self):
        if self.ui.XundercutcheckBox.isChecked():
            self.ui.YundercutcheckBox.setChecked(False)
            self.ui.ZundercutcheckBox.setChecked(False)
            self.ui.XYundercutcheckBox.setChecked(False)
            self.undercutX()
    
    def undercutXY(self):        
        
        self.ui.XanglethresholdSlider.value=0
        self.ui.YanglethresholdSlider.value=0
        self.ui.ZanglethresholdSlider.value=0

        self.ui.XundercutcheckBox.setChecked(False)
        self.ui.YundercutcheckBox.setChecked(False)
        self.ui.ZundercutcheckBox.setChecked(False)
        
        # Get remeshed model
        model_to_undercut=self.ui.sourcemodelselector.currentNode().GetName()        
        originalModelNode = slicer.util.getNode(model_to_undercut)
        originalPolyData = originalModelNode.GetPolyData()
        
        existingUndercutNode = slicer.mrmlScene.GetFirstNodeByName("UndercutSurface")
        if existingUndercutNode:
            slicer.mrmlScene.RemoveNode(existingUndercutNode)     
 
        # Compute normals if missing
        if not originalPolyData.GetPointData().GetNormals():
            print("Computing normals for remeshed model...")
            normals_filter = vtk.vtkPolyDataNormals()
            normals_filter.SetInputData(originalPolyData)
            normals_filter.ComputePointNormalsOn()
            normals_filter.Update()
            originalPolyData = normals_filter.GetOutput()

        # Normalize tool direction properly
        toolDirection = np.array([1.0, 1.0, 0.0], dtype=np.float64)  # Explicit float type
        tool_norm = np.linalg.norm(toolDirection)
        if tool_norm > 1e-6:  # Prevent division by zero
            toolDirection /= tool_norm
        else:
            raise ValueError("Tool direction vector is zero-length")

        thresholdAngle = self.ui.anglethresholdSpinBox.value   # Degrees

        undercutPoints = []
        normals = originalPolyData.GetPointData().GetNormals()

        for i in range(originalPolyData.GetNumberOfPoints()):
            # Get and normalize normal vector
            normal = np.array(normals.GetTuple3(i), dtype=np.float64)
            normal_norm = np.linalg.norm(normal)
            if normal_norm > 1e-6:
                normal /= normal_norm
            else:
                continue  # Skip invalid normals
            
            # Calculate angle safely
            cos_theta = np.dot(normal, toolDirection)
            cos_theta = np.clip(cos_theta, -1.0, 1.0)  # Prevent numerical errors
            theta = np.arccos(cos_theta) * (180 / np.pi)
            
            if theta > thresholdAngle:
                undercutPoints.append(i)

        # Continue with cell extraction as before...
        # Now create the undercut surface model from the ORIGINAL mesh
        # (Not from NormalsVisualization)
        undercutPointSet = set(undercutPoints)
        newCells = vtk.vtkCellArray()

        for i in range(originalPolyData.GetNumberOfCells()):
            cell = originalPolyData.GetCell(i)
            if cell.GetCellType() != vtk.VTK_TRIANGLE:
                continue
            # Check if any vertex of the triangle is an undercut point
            pid0 = cell.GetPointId(0)
            pid1 = cell.GetPointId(1)
            pid2 = cell.GetPointId(2)
            if pid0 in undercutPointSet or pid1 in undercutPointSet or pid2 in undercutPointSet:
                newCells.InsertNextCell(cell)

        # Create the undercut surface polydata
        undercutSurfacePolyData = vtk.vtkPolyData()
        undercutSurfacePolyData.SetPoints(originalPolyData.GetPoints())  # Original points
        undercutSurfacePolyData.SetPolys(newCells)  # Filtered triangles

        # Clean unused points (optional but recommended)
        cleanFilter = vtk.vtkCleanPolyData()
        cleanFilter.SetInputData(undercutSurfacePolyData)
        cleanFilter.Update()
        cleanedPolyData = cleanFilter.GetOutput()

        # Add to 3D Slicer
        undercutSurfaceNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelNode", "UndercutSurface")
        undercutSurfaceNode.SetAndObservePolyData(cleanedPolyData)

        # Configure display
        undercutSurfaceDisplayNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelDisplayNode")
        undercutSurfaceDisplayNode.SetColor(1, 0, 0)  # Red
        undercutSurfaceDisplayNode.SetOpacity(1.0)
        undercutSurfaceDisplayNode.SetVisibility(True)
        undercutSurfaceNode.SetAndObserveDisplayNodeID(undercutSurfaceDisplayNode.GetID())

        slicer.util.forceRenderAllViews()


    def onXYundercutcheckBox(self):
        if self.ui.XYundercutcheckBox.isChecked():
            self.ui.XundercutcheckBox.setChecked(False)
            self.ui.YundercutcheckBox.setChecked(False)
            self.ui.ZundercutcheckBox.setChecked(False)
            self.undercutXY()    

    def undercutY(self):
 
        self.ui.XanglethresholdSlider.value=0
        self.ui.ZanglethresholdSlider.value=0
        self.ui.XYanglethresholdSlider.value=0

        self.ui.XundercutcheckBox.setChecked(False)
        self.ui.ZundercutcheckBox.setChecked(False)
        self.ui.XYundercutcheckBox.setChecked(False)
        
        # Get remeshed model
        model_to_undercut=self.ui.sourcemodelselector.currentNode().GetName()        
        originalModelNode = slicer.util.getNode(model_to_undercut)
        originalPolyData = originalModelNode.GetPolyData()
        
        existingUndercutNode = slicer.mrmlScene.GetFirstNodeByName("UndercutSurface")
        if existingUndercutNode:
            slicer.mrmlScene.RemoveNode(existingUndercutNode) 
        

        # Compute normals if missing
        if not originalPolyData.GetPointData().GetNormals():
            print("Computing normals for remeshed model...")
            normals_filter = vtk.vtkPolyDataNormals()
            normals_filter.SetInputData(originalPolyData)
            normals_filter.ComputePointNormalsOn()
            normals_filter.Update()
            originalPolyData = normals_filter.GetOutput()

        # Normalize tool direction properly
        toolDirection = np.array([0.0, 1.0, 0.0], dtype=np.float64)  # Explicit float type
        tool_norm = np.linalg.norm(toolDirection)
        if tool_norm > 1e-6:  # Prevent division by zero
            toolDirection /= tool_norm
        else:
            raise ValueError("Tool direction vector is zero-length")

        thresholdAngle = self.ui.anglethresholdSpinBox.value   # Degrees

        undercutPoints = []
        normals = originalPolyData.GetPointData().GetNormals()

        for i in range(originalPolyData.GetNumberOfPoints()):
            # Get and normalize normal vector
            normal = np.array(normals.GetTuple3(i), dtype=np.float64)
            normal_norm = np.linalg.norm(normal)
            if normal_norm > 1e-6:
                normal /= normal_norm
            else:
                continue  # Skip invalid normals
            
            # Calculate angle safely
            cos_theta = np.dot(normal, toolDirection)
            cos_theta = np.clip(cos_theta, -1.0, 1.0)  # Prevent numerical errors
            theta = np.arccos(cos_theta) * (180 / np.pi)
            
            if theta > thresholdAngle:
                undercutPoints.append(i)
       
        # Continue with cell extraction as before...
        # Now create the undercut surface model from the ORIGINAL mesh
        # (Not from NormalsVisualization)
        undercutPointSet = set(undercutPoints)
        newCells = vtk.vtkCellArray()

        for i in range(originalPolyData.GetNumberOfCells()):
            cell = originalPolyData.GetCell(i)
            if cell.GetCellType() != vtk.VTK_TRIANGLE:
                continue
            # Check if any vertex of the triangle is an undercut point
            pid0 = cell.GetPointId(0)
            pid1 = cell.GetPointId(1)
            pid2 = cell.GetPointId(2)
            if pid0 in undercutPointSet or pid1 in undercutPointSet or pid2 in undercutPointSet:
                newCells.InsertNextCell(cell)

        # Create the undercut surface polydata
        undercutSurfacePolyData = vtk.vtkPolyData()
        undercutSurfacePolyData.SetPoints(originalPolyData.GetPoints())  # Original points
        undercutSurfacePolyData.SetPolys(newCells)  # Filtered triangles

        # Clean unused points (optional but recommended)
        cleanFilter = vtk.vtkCleanPolyData()
        cleanFilter.SetInputData(undercutSurfacePolyData)
        cleanFilter.Update()
        cleanedPolyData = cleanFilter.GetOutput()

        # Add to 3D Slicer
        undercutSurfaceNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelNode", "UndercutSurface")
        undercutSurfaceNode.SetAndObservePolyData(cleanedPolyData)

        # Configure display
        undercutSurfaceDisplayNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelDisplayNode")
        undercutSurfaceDisplayNode.SetColor(1, 0, 0)  # Red
        undercutSurfaceDisplayNode.SetOpacity(1.0)
        undercutSurfaceDisplayNode.SetVisibility(True)
        undercutSurfaceNode.SetAndObserveDisplayNodeID(undercutSurfaceDisplayNode.GetID())

        slicer.util.forceRenderAllViews()


    def onYundercutcheckBox(self):
        if self.ui.YundercutcheckBox.isChecked():
            self.ui.XundercutcheckBox.setChecked(False)
            self.ui.ZundercutcheckBox.setChecked(False)
            self.ui.XYundercutcheckBox.setChecked(False)
            self.undercutY()    
    
    def undercutZ(self):
 
        self.ui.XanglethresholdSlider.value=0
        self.ui.YanglethresholdSlider.value=0
        self.ui.XYanglethresholdSlider.value=0

        self.ui.XundercutcheckBox.setChecked(False)
        self.ui.YundercutcheckBox.setChecked(False)
        self.ui.XYundercutcheckBox.setChecked(False)
        
        # Get remeshed model
        model_to_undercut=self.ui.sourcemodelselector.currentNode().GetName()        
        originalModelNode = slicer.util.getNode(model_to_undercut)
        originalPolyData = originalModelNode.GetPolyData()
        
        existingUndercutNode = slicer.mrmlScene.GetFirstNodeByName("UndercutSurface")
        if existingUndercutNode:
            slicer.mrmlScene.RemoveNode(existingUndercutNode)    
        

        # Compute normals if missing
        if not originalPolyData.GetPointData().GetNormals():
            print("Computing normals for remeshed model...")
            normals_filter = vtk.vtkPolyDataNormals()
            normals_filter.SetInputData(originalPolyData)
            normals_filter.ComputePointNormalsOn()
            normals_filter.Update()
            originalPolyData = normals_filter.GetOutput()

        # Normalize tool direction properly
        toolDirection = np.array([0.0, 0.0, 1.0], dtype=np.float64)  # Explicit float type
        tool_norm = np.linalg.norm(toolDirection)
        if tool_norm > 1e-6:  # Prevent division by zero
            toolDirection /= tool_norm
        else:
            raise ValueError("Tool direction vector is zero-length")

        thresholdAngle = self.ui.anglethresholdSpinBox.value   # Degrees

        undercutPoints = []
        normals = originalPolyData.GetPointData().GetNormals()

        for i in range(originalPolyData.GetNumberOfPoints()):
            # Get and normalize normal vector
            normal = np.array(normals.GetTuple3(i), dtype=np.float64)
            normal_norm = np.linalg.norm(normal)
            if normal_norm > 1e-6:
                normal /= normal_norm
            else:
                continue  # Skip invalid normals
            
            # Calculate angle safely
            cos_theta = np.dot(normal, toolDirection)
            cos_theta = np.clip(cos_theta, -1.0, 1.0)  # Prevent numerical errors
            theta = np.arccos(cos_theta) * (180 / np.pi)
            
            if theta > thresholdAngle:
                undercutPoints.append(i)

        # Continue with cell extraction as before...
        # Now create the undercut surface model from the ORIGINAL mesh
        # (Not from NormalsVisualization)
        undercutPointSet = set(undercutPoints)
        newCells = vtk.vtkCellArray()

        for i in range(originalPolyData.GetNumberOfCells()):
            cell = originalPolyData.GetCell(i)
            if cell.GetCellType() != vtk.VTK_TRIANGLE:
                continue
            # Check if any vertex of the triangle is an undercut point
            pid0 = cell.GetPointId(0)
            pid1 = cell.GetPointId(1)
            pid2 = cell.GetPointId(2)
            if pid0 in undercutPointSet or pid1 in undercutPointSet or pid2 in undercutPointSet:
                newCells.InsertNextCell(cell)

        # Create the undercut surface polydata
        undercutSurfacePolyData = vtk.vtkPolyData()
        undercutSurfacePolyData.SetPoints(originalPolyData.GetPoints())  # Original points
        undercutSurfacePolyData.SetPolys(newCells)  # Filtered triangles

        # Clean unused points (optional but recommended)
        cleanFilter = vtk.vtkCleanPolyData()
        cleanFilter.SetInputData(undercutSurfacePolyData)
        cleanFilter.Update()
        cleanedPolyData = cleanFilter.GetOutput()

        # Add to 3D Slicer
        undercutSurfaceNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelNode", "UndercutSurface")
        undercutSurfaceNode.SetAndObservePolyData(cleanedPolyData)

        # Configure display
        undercutSurfaceDisplayNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelDisplayNode")
        undercutSurfaceDisplayNode.SetColor(1, 0, 0)  # Red
        undercutSurfaceDisplayNode.SetOpacity(1.0)
        undercutSurfaceDisplayNode.SetVisibility(True)
        undercutSurfaceNode.SetAndObserveDisplayNodeID(undercutSurfaceDisplayNode.GetID())

        slicer.util.forceRenderAllViews()


    def onZundercutcheckBox(self):
        if self.ui.ZundercutcheckBox.isChecked():
            self.ui.XundercutcheckBox.setChecked(False)
            self.ui.YundercutcheckBox.setChecked(False)
            self.ui.XYundercutcheckBox.setChecked(False)
            self.undercutZ()

    def onminus70XYButtton(self):        

        self.ui.XanglethresholdSlider.value=0
        self.ui.YanglethresholdSlider.value=0
        self.ui.ZanglethresholdSlider.value=0
        self.ui.XYanglethresholdSlider.value=0

        self.ui.XundercutcheckBox.setChecked(False)
        self.ui.YundercutcheckBox.setChecked(False)
        self.ui.ZundercutcheckBox.setChecked(False)
        self.ui.XYundercutcheckBox.setChecked(False)
        
        # Get remeshed model
       
        model_to_undercut=self.ui.sourcemodelselector.currentNode().GetName()        
        originalModelNode = slicer.util.getNode(model_to_undercut)
        originalPolyData = originalModelNode.GetPolyData()

        existingUndercutNode = slicer.mrmlScene.GetFirstNodeByName("UndercutSurface")
        if existingUndercutNode:
            slicer.mrmlScene.RemoveNode(existingUndercutNode)   
        

        # Compute normals if missing
        if not originalPolyData.GetPointData().GetNormals():
            print("Computing normals for remeshed model...")
            normals_filter = vtk.vtkPolyDataNormals()
            normals_filter.SetInputData(originalPolyData)
            normals_filter.ComputePointNormalsOn()
            normals_filter.Update()
            originalPolyData = normals_filter.GetOutput()

        # Normalize tool direction properly
        toolDirection = np.array([1.0, 1.0, 0.0], dtype=np.float64)  # Explicit float type
        tool_norm = np.linalg.norm(toolDirection)
        if tool_norm > 1e-6:  # Prevent division by zero
            toolDirection /= tool_norm
        else:
            raise ValueError("Tool direction vector is zero-length")

        thresholdAngle = 30 # temporary default value for Degrees

        undercutPoints = []
        normals = originalPolyData.GetPointData().GetNormals()

        for i in range(originalPolyData.GetNumberOfPoints()):
            # Get and normalize normal vector
            normal = np.array(normals.GetTuple3(i), dtype=np.float64)
            normal_norm = np.linalg.norm(normal)
            if normal_norm > 1e-6:
                normal /= normal_norm
            else:
                continue  # Skip invalid normals
            
            # Calculate angle safely
            cos_theta = np.dot(normal, toolDirection)
            cos_theta = np.clip(cos_theta, -1.0, 1.0)  # Prevent numerical errors
            theta = np.arccos(cos_theta) * (180 / np.pi)
            
            if theta > thresholdAngle:
                undercutPoints.append(i)

        # Continue with cell extraction as before...
        # Now create the undercut surface model from the ORIGINAL mesh
        # (Not from NormalsVisualization)
        undercutPointSet = set(undercutPoints)
        newCells = vtk.vtkCellArray()

        for i in range(originalPolyData.GetNumberOfCells()):
            cell = originalPolyData.GetCell(i)
            if cell.GetCellType() != vtk.VTK_TRIANGLE:
                continue
            # Check if any vertex of the triangle is an undercut point
            pid0 = cell.GetPointId(0)
            pid1 = cell.GetPointId(1)
            pid2 = cell.GetPointId(2)
            if pid0 in undercutPointSet or pid1 in undercutPointSet or pid2 in undercutPointSet:
                newCells.InsertNextCell(cell)

        # Create the undercut surface polydata
        undercutSurfacePolyData = vtk.vtkPolyData()
        undercutSurfacePolyData.SetPoints(originalPolyData.GetPoints())  # Original points
        undercutSurfacePolyData.SetPolys(newCells)  # Filtered triangles

        # Clean unused points (optional but recommended)
        cleanFilter = vtk.vtkCleanPolyData()
        cleanFilter.SetInputData(undercutSurfacePolyData)
        cleanFilter.Update()
        cleanedPolyData = cleanFilter.GetOutput()

        # Add to 3D Slicer
        undercutSurfaceNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelNode", "UndercutSurface")
        undercutSurfaceNode.SetAndObservePolyData(cleanedPolyData)

        # Configure display
        undercutSurfaceDisplayNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelDisplayNode")
        undercutSurfaceDisplayNode.SetColor(1, 0, 0)  # Red
        undercutSurfaceDisplayNode.SetOpacity(1.0)
        undercutSurfaceDisplayNode.SetVisibility(True)
        undercutSurfaceNode.SetAndObserveDisplayNodeID(undercutSurfaceDisplayNode.GetID())

        slicer.util.forceRenderAllViews()
        self.FilterTreeItems_3()

    def onUpper_undercutsblockButton(self):
        
        modelNode = slicer.util.getNode('UndercutSurface')
        existingUndercutNode = slicer.mrmlScene.GetFirstNodeByName("HollowedUndercut")
        if existingUndercutNode:
            slicer.mrmlScene.RemoveNode(existingUndercutNode)

        hollowModeler = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLDynamicModelerNode")
        hollowModeler.SetToolName("Hollow")
        hollowModeler.SetNodeReferenceID("Hollow.InputModel", modelNode.GetID())

        hollowedModelNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelNode", "HollowedUndercut")
        hollowModeler.SetNodeReferenceID("Hollow.OutputModel", hollowedModelNode.GetID())
        hollowModeler.SetAttribute("ShellThickness", "1.0")  # Positive = outward, Negative = inward
        hollowModeler.SetAttribute("ShellOffsetDirection", "Inside")  # "Inside" or "Outside"
        hollowModeler.SetContinuousUpdate(True)  # Disable for stability

        hollowedModelNode.GetDisplayNode().SetColor(0, 1, 0)  # Red
        hollowedModelNode.GetDisplayNode().SetOpacity(1.0)
        self.FilterTreeItems_3()

    def onLower_undercutsblockButton(self):

        modelNode = slicer.util.getNode('UndercutSurface')
        existingUndercutNode = slicer.mrmlScene.GetFirstNodeByName("HollowedUndercut")
        if existingUndercutNode:
            slicer.mrmlScene.RemoveNode(existingUndercutNode)

        hollowModeler = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLDynamicModelerNode")
        hollowModeler.SetToolName("Hollow")
        hollowModeler.SetNodeReferenceID("Hollow.InputModel", modelNode.GetID())

        hollowedModelNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelNode", "HollowedUndercut")
        hollowModeler.SetNodeReferenceID("Hollow.OutputModel", hollowedModelNode.GetID())
        hollowModeler.SetAttribute("ShellThickness", "-1.0")  # Positive = outward, Negative = inward
        hollowModeler.SetAttribute("ShellOffsetDirection", "Inside")  # "Inside" or "Outside"
        hollowModeler.SetContinuousUpdate(True)  # Disable for stability

        hollowedModelNode.GetDisplayNode().SetColor(0, 1, 0)  # Red
        hollowedModelNode.GetDisplayNode().SetOpacity(1.0)
        self.FilterTreeItems_3()        



    def OnModelPlusUndercutsButton(self):
        
        masterVolumeNode = slicer.util.getNode('vtkMRMLScalarVolumeNode*')
        modelNode1 = slicer.util.getNode(self.ui.sourcemodelselector.currentNode().GetName())
        modelNode2 = slicer.util.getNode('HollowedUndercut')

        # Create segmentation
        segmentationNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationNode")
        segmentationNode.CreateDefaultDisplayNodes()  # only needed for display
        segmentationNode.SetReferenceImageGeometryParameterFromVolumeNode(masterVolumeNode)

        # Import the model into the segmentation node
        slicer.modules.segmentations.logic().ImportModelToSegmentationNode(modelNode1, segmentationNode)
        slicer.modules.segmentations.logic().ImportModelToSegmentationNode(modelNode2, segmentationNode)

        # Get Segment IDs
        scancut2ID = segmentationNode.GetSegmentation().GetSegmentIdBySegmentName(self.ui.sourcemodelselector.currentNode().GetName())
        hollowedUndercutID = segmentationNode.GetSegmentation().GetSegmentIdBySegmentName("HollowedUndercut")

        # Configure Segment Editor
        segmentEditorWidget = slicer.modules.segmenteditor.widgetRepresentation().self().editor
        segmentEditorNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentEditorNode")

        try:
            # Set up Segment Editor
            segmentEditorWidget.setMRMLSegmentEditorNode(segmentEditorNode)
            segmentEditorWidget.setSegmentationNode(segmentationNode)
            segmentEditorWidget.setSourceVolumeNode(masterVolumeNode)  # Set the reference volume node
            
            # Allow overlap
            segmentEditorNode.SetOverwriteMode(slicer.vtkMRMLSegmentEditorNode.OverwriteNone)
            
            # Select target segment
            segmentEditorWidget.setCurrentSegmentID(scancut2ID)
            
            # Apply Logical Operators Effect
            segmentEditorWidget.setActiveEffectByName("Logical operators")
            unionEffect = segmentEditorWidget.activeEffect()
            
            if unionEffect:
                # Configure union operation
                unionEffect.setParameter("Operation", "UNION")
                unionEffect.setParameter("ModifierSegmentID", hollowedUndercutID)
                
                # Apply union effect
                unionEffect.self().onApply()
                print("[INFO] Successfully applied union effect between 'scancut2' and 'HollowedUndercut'.")
                sourceSeg = slicer.util.getNode(segmentationNode.GetID())
                print(sourceSeg.GetName())
                segmentNames = [self.ui.sourcemodelselector.currentNode().GetName()]
                destSeg = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLSegmentationNode', 'SelectedSegments')
                # Copy the selected segments to the new segmentation
                for segmentName in segmentNames:
                    segmentId = sourceSeg.GetSegmentation().GetSegmentIdBySegmentName(segmentName)
                    if segmentId:
                        removeFromSource = False  # Set to True if you want to remove the segment from the source
                        destSeg.GetSegmentation().CopySegmentFromSegmentation(sourceSeg.GetSegmentation(), segmentId, removeFromSource)
                    else:
                        print(f"Segment '{segmentName}' not found in the source segmentation.")
                # Export the selected segments to models
                shNode = slicer.mrmlScene.GetSubjectHierarchyNode()
                exportFolderItemId = shNode.CreateFolderItem(shNode.GetSceneItemID(), "GuideBase_Segment")
                slicer.modules.segmentations.logic().ExportAllSegmentsToModels(destSeg, exportFolderItemId)

                node=slicer.util.getNode(self.ui.sourcemodelselector.currentNode().GetName())
                node.SetName("GuideBase")
                node.GetDisplayNode().SetColor(0, 1, 1)
                self.FilterTreeItems_3()   
                
            else:
                print("[ERROR] Logical Operators effect could not be activated.")
        finally:
            
            print(f"Selected segments exported to models under folder 'Segments'!")

            # Remove the temporary destination segmentation node
            slicer.mrmlScene.RemoveNode(sourceSeg)
            slicer.mrmlScene.RemoveNode(destSeg)
            
            f_model = slicer.mrmlScene.GetFirstNodeByName(self.ui.sourcemodelselector.currentNode().GetName())
            if f_model:
                f_model.GetDisplayNode().SetVisibility(False)
              
            i_model = slicer.mrmlScene.GetFirstNodeByName("HollowedUndercut")
            if i_model:
                i_model.GetDisplayNode().SetVisibility(False)            

            h_model = slicer.mrmlScene.GetFirstNodeByName("UndercutSurface")
            if h_model:
                h_model.GetDisplayNode().SetVisibility(False)               


                
            print("Temporary segmentation node removed.")           


        
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
        
            
    def setParameterNode(self, inputParameterNode: Optional[RegisterModuleParameterNode]) -> None:
        if self._parameterNode:
            try:
                self._parameterNode.disconnectGui(self._parameterNodeGuiTag)
            except Exception:
                pass
            self._parameterNodeGuiTag = None

        self._parameterNode = inputParameterNode

        if self._parameterNode:
            guiWrapper = RegisterModuleGui(self.ui)
            self._parameterNodeGuiTag = self._parameterNode.connectGui(guiWrapper)

#
# RegisterModuleLogic
#


class RegisterModuleLogic(ScriptedLoadableModuleLogic):
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
        return RegisterModuleParameterNode(super().getParameterNode())


# RegisterModuleTest
#

class RegisterModuleTest(ScriptedLoadableModuleTest):
    pass
