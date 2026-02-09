import logging
import os, sys
resourcesPath = os.path.join(os.path.dirname(__file__), "Resources")
if resourcesPath not in sys.path:
    sys.path.append(resourcesPath)

import MIS7XD_libUp
import MIS7XD_libLow

from typing import Annotated, Optional
import qt
import vtk
import ctk
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

import random
import numpy as np

# GenericImplCreator
#

class GenericImplCreator(ScriptedLoadableModule):
    """Uses ScriptedLoadableModule base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = _("Generic Implant Creator")  
        
        self.parent.categories = [translate("qSlicerAbstractCoreModule", "Examples")]
        self.parent.dependencies = []  
        self.parent.contributors = ["Dimitris Trikeriotis (Gnathion)"]          
        
        self.parent.helpText = _("""
First to generate pre-implant models, then to align with virtual implants(built-in library), positioned prosthetically-driven.
See more information in <a href="https://github.com/organization/projectname#GenericImplCreator">module documentation</a>.
""")
        self.parent.acknowledgementText = _("""
This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc., Andras Lasso, PerkLab,
and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
""")


#
# GenericImplCreatorParameterNode
#
'''
The parameters needed by the module.
RegisteSubjectHierarchyTreeView and MarkupsToModelNode were commented out
because of the error: "Unable to create serializer for {classtype} member {name}")
probably due to the fact that no GUI connector is yet available. Fix????
'''


@parameterNodeWrapper
class GenericImplCreatorParameterNode:
    # Simple parameters
    selectjawcomboBox: str = "None"
    selectbrandcomboBox: str = "None"
    selectimplantsystemcomboBox: str = "None"
    selectimplantcomboBox: str = "None"
    locationcomboBox: str = "None"

    # UI numeric/bool settings
    tubeRadiusSpinbox: Annotated[float, WithinRange(0.0, 10.0)] = 0.0
    tubeSidesSpinBox:  Annotated[int,   WithinRange(3, 200)]     = 20
    tubeCappingCheckBox: bool = True
    pointDistanceSpinBox: Annotated[float, WithinRange(0.0, 100.0)] = 0.0

    # Node selections
    pointListComboBox: slicer.vtkMRMLMarkupsFiducialNode = None
    #markupsToModelComboBox: slicer.vtkMRMLMarkupsToModelNode = None
    #ImplantSubjectHierarchyTreeView:slicer.qMRMLSubjectHierarchyTreeViewNode
    #RestSubjectHierarchyTreeView:slicer.qMRMLSubjectHierarchyTreeViewNode

'''
Because of the error:AttributeError: 'dict' object has no attribute '__dict__'
instead of passing a dictionary directly to connectGui()
an object/class (self.ui) is used, that contains all the named widgets.
'''  

class GenericImplCreatorGui:
    def __init__(self, ui):
        
        self.selectjawcomboBox = ui.selectjawcomboBox
        self.selectbrandcomboBox = ui.selectbrandcomboBox      
        selectimplantsystemcomboBox = ui.selectimplantsystemcomboBox
        self.selectimplantcomboBox = ui.selectimplantcomboBox
        self.locationcomboBox = ui.locationcomboBox
        
        self.tubeRadiusSpinbox = ui.tubeRadiusSpinbox
        self.tubeSidesSpinBox = ui.tubeSidesSpinBox
        self.tubeCappingCheckBox = ui.tubeCappingCheckBox
        self.pointDistanceSpinBox = ui.pointDistanceSpinBox
        
        self.pointListComboBox = ui.pointListComboBox
        #self.markupsToModelComboBox = ui.markupsToModelComboBox
        #self.ImplantSubjectHierarchyTreeView = ui.ImplantSubjectHierarchyTreeView
        #self.RestSubjectHierarchyTreeView= ui.RestSubjectHierarchyTreeView

#
# GenericImplCreatorWidget
#


class GenericImplCreatorWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):


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
        uiWidget = slicer.util.loadUI(self.resourcePath("UI/GenericImplCreator.ui"))
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
        self.logic = GenericImplCreatorLogic()

        # Connections

        # These connections ensure that we update parameter node when scene is closed
        self.addObserver(slicer.mrmlScene, slicer.mrmlScene.StartCloseEvent, self.onSceneStartClose)
        self.addObserver(slicer.mrmlScene, slicer.mrmlScene.EndCloseEvent, self.onSceneEndClose)
       

        # Other connections, buttons , functions
        self.ui.selectimplantsystemcomboBox.currentTextChanged.connect(self.update_implant_list)
                
        self.ui.preimplant_applyButton.clicked.connect(self.onApply)
        self.ui.modifypointsButton.clicked.connect(self.onmodifypoints)
        
        self.ui.grbutton.connect('clicked(bool)', self.OnGreek)
        self.ui.engbutton.connect('clicked(bool)', self.OnEnglish)
 
        self.greek()
        self.english()  

        self.FilterTreeItems()
        self.FilterTreeItems_2()

        self.ui.generateimplantup.connect("clicked(bool)", self.create_up_generic_implant)
        self.ui.generateimplantlow.connect("clicked(bool)", self.create_low_generic_implant)
        self.ui.exportlocButton.connect("clicked(bool)", self.onredexport)
        self.ui.importlocButton.connect("clicked(bool)", self.onredreset)
        self.ui.exportimplButton.connect("clicked(bool)",self.implant_coords_exp)
        self.ui.importimplButton.connect("clicked(bool)",self.implant_coords_imp)
        self.ui.homeButton.connect("clicked(bool)", self.onhomeButton)
        self.ui.implantstreeButton.connect("clicked(bool)", self.onimplantstreeButton)
        self.ui.modelpoint2Button.connect("clicked(bool)", self.onmodelpoint2Button)

        self.retrievepatient()
        
        self.ui.pointListComboBox.nodeAdded.connect(self.onnewpoint)
        
        self.ui.markupsToModelComboBox.currentNodeChanged.connect(self.onMarkupsToModelNodeChanged)
        self.ui.markupsToModelComboBox.nodeAdded.connect(self.onNodAdd)
        self.currentMarkupsToModelNode = None
        self.updateUI() 

        self.ui.patientnamelabel.hide()
        self.ui.label_14.hide()
        self.ui.tubeSidesSpinBox.hide()
        self.ui.label_13.hide()
        self.ui.tubeCappingCheckBox.hide()


        self.populate_location_List()
        self.populate_jaw_List()
        self.populate_brand_List()
        self.populate_impl_system_List()
        self.populate_mis_7XD_List()
        self.homeButton()

        self.ui.widescreenButton.connect("clicked(bool)", self.onwidescreenButton)
        self.ui.custom1screenButton.connect("clicked(bool)", self.customlayout1)
        self.ui.redcreenButton.connect("clicked(bool)", self.onredcreenButton)
        self.ui.dscreenButton.connect("clicked(bool)", self.ondscreenButton)

        self.widescreenButton()
        self.custom1screenButton()
        self.redcreenButton()
        self.dscreenButton()

        self.ui.dentimButton.connect("clicked(bool)", self.ondentimButton)
        self.ui.registButton.connect("clicked(bool)", self.onregistButton)
        self.ui.virtprButton.connect("clicked(bool)", self.onvirtprButton)
        

        self.dentimButton()
        self.registButton()
        self.virtprButton()


        self.dataButton()
        self.ui.databutton.connect("clicked(bool)", self.ondataButton)         

        self.initializeParameterNode()

    def dataButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "giOSData.png"))
        self.ui.databutton.setIcon(icon)           
    
    def ondataButton(self):
        slicer.util.selectModule("OralSurgData")
        slicer.util.reloadScriptedModule("OralSurgData")


    def onimplantstreeButton(self):
        self.FilterTreeItems()


    def onmodelpoint2Button(self):
        self.FilterTreeItems_2()

    def dentimButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "giDentImplIm.png"))
        self.ui.dentimButton.setIcon(icon)

    def registButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "giRegisterMod.png"))
        self.ui.registButton.setIcon(icon)

    def virtprButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "giVirtualPr.png"))
        self.ui.virtprButton.setIcon(icon)      

    def ondentimButton(self):
        slicer.util.selectModule("DentImplImaging")
        #slicer.util.reloadScriptedModule("DentImplImaging")

    def onregistButton(self):
        slicer.util.selectModule("RegisterModule")
        #slicer.util.reloadScriptedModule("RegisterModule")

    def onvirtprButton(self):
        slicer.util.selectModule("VirtualProsth")
        #slicer.util.reloadScriptedModule("VirtualProsth")
        
    def homeButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "giOrSurgMod.png"))
        self.ui.homeButton.setIcon(icon)
        
    def onhomeButton(self):
        slicer.util.selectModule("OralSurgModuleHome")
        #slicer.util.reloadScriptedModule("OralSurgModuleHome")

    def widescreenButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "giws.png"))        
        self.ui.widescreenButton.setIcon(icon)

    def custom1screenButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "gics.png"))
        self.ui.custom1screenButton.setIcon(icon)

    def redcreenButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "gired.png"))
        self.ui.redcreenButton.setIcon(icon)

    def dscreenButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "gi3d.png"))
        self.ui.dscreenButton.setIcon(icon)

    def onwidescreenButton(self):
        slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutConventionalWidescreenView)

    def onredcreenButton(self):
        slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUpRedSliceView)

    def ondscreenButton(self):
        slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUp3DView)
        

    def populate_location_List(self):                    

        location_list= ['None',
                '17', '16', '15', '14', '13','12','11',
                '21', '22', '23', '24', '25','26','27',
                '37', '36', '35', '34', '33','32','31',
                '41', '42', '43', '44', '45','46','47'
                ]       
        for loc in location_list:
            self.ui.locationcomboBox.addItem(loc)
            
            
    def populate_jaw_List(self):
        
        jaw_list=['None', 'Upper', 'Lower']
        for jaw in jaw_list:
            self.ui.selectjawcomboBox.addItem(jaw)

            
    def populate_brand_List(self):            

        brand_name_list=['None', 'Dentsply Sirona']
        for brand_name in brand_name_list:
            self.ui.selectbrandcomboBox.addItem(brand_name)


    def populate_impl_system_List(self):
            
        implant_system_list = ['None', 'MIS_7 Implant System']
        for implant_system in implant_system_list:
            self.ui.selectimplantsystemcomboBox.addItem(implant_system)
            
    def populate_mis_7XD_List(self):
                
        self.mis_7_XD_implant_list = ['None',
                                 '3.3/10', '3.3/11.5', '3.3/13', '3.3/16',
                                 '3.75/8', '3.75/10', '3.75/11.5', '3.75/13', '3.75/16',
                                 '4.2/6', '4.2/8', '4.2/10', '4.2/11.5', '4.2/13', '4.2/16',
                                 '5/6', '5/8', '5/10', '5/11.5', '5/13', '5/16',
                                 '6/6', '6/8', '6/10', '6/11.5', '6/13']   

    def greek(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "gigr.png"))        
        self.ui.grbutton.setIcon(icon)

    def english(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "gieng.png"))        
        self.ui.engbutton.setIcon(icon)            

    def OnGreek(self):
        
        self.ui.genCollapsibleButton.setText("Δημιουργία προσχεδίου και εικονικού εμφυτεύματος")  
        self.ui.label_13.setText("Πώμα")        
        self.ui.label_14.setText("Πλευρές")        
        self.ui.label_17.setText("Προσθήκη/Επιλογή Εμφυτεύματος:")        
        self.ui.label_16.setText("Σημεία:")        
        self.ui.label_15.setText("Ακτίνα:")        
        self.ui.label_12.setText("Μήκος:")
        self.ui.label_10.setText("Θέση:")        
        self.ui.exportlocButton.setText("Εξαγωγή Τομής")        
        self.ui.importlocButton.setText("Εισαγωγή Τομής")
        self.ui.exportimplButton.setText("Εξαγωγή Εμφυτεύματος")
        self.ui.importimplButton.setText("Εισαγωγή Εμφυτεύματος")        
        self.ui.modifypointsButton.setText("Τροποποίηση Προσχεδίου")        
        self.ui.preimplant_applyButton.setText("Ολοκλήρωση Προσχεδίου")        
        self.ui.label_7.setText("Επιλογή γνάθου:")        
        self.ui.label_6.setText("Εμπορικό όνομα:")        
        self.ui.label_9.setText("Εμφυτευματκό Σύστημα:")        
        self.ui.label_8.setText("Μοντέλο Εμφυτεύματος:")        
        self.ui.generateimplantup.setText("Δημιουργία Εμφυτεύματος(Άνω Γνάθου)")
        self.ui.generateimplantlow.setText("Δημιουργία Εμφυτεύματος(Κάτω Γνάθου)")
        


    def OnEnglish(self):
        
        self.ui.genCollapsibleButton.setText("Create preimplant and generic implant unit")  
        self.ui.label_13.setText("cap")        
        self.ui.label_14.setText("Sides")        
        self.ui.label_17.setText("Add/Select Implant:")        
        self.ui.label_16.setText("Points:")        
        self.ui.label_14.setText("Radius:")        
        self.ui.label_12.setText("Length:")
        self.ui.label_10.setText("Location:")        
        self.ui.exportlocButton.setText("Export Slice")        
        self.ui.importlocButton.setText("Import Slice")
        self.ui.exportimplButton.setText("Export Implant")
        self.ui.importimplButton.setText("Import Implant")        
        self.ui.modifypointsButton.setText("Modify Pre_Implant")        
        self.ui.preimplant_applyButton.setText("Create Pre_implant")        
        self.ui.label_7.setText("Select Jaw:")        
        self.ui.label_6.setText("Brand Name:")        
        self.ui.label_9.setText("Implant System:")        
        self.ui.label_8.setText("Implant Model:")        
        self.ui.generateimplantup.setText("Create Implant(Upper jaw)")
        self.ui.generateimplantlow.setText("Create Implant(Lower jaw)")


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
                 
            
    def onredexport(self) -> None:
               

        def get_slice_plane_coordinates(sliceNode):
            # Get the 4x4 slice to RAS transform matrix
            sliceToRAS = sliceNode.GetSliceToRAS()
            slicePlaneCoordinates = []

            # Extract the origin and axis vectors
            origin = [0, 0, 0, 1]
            xAxis = [1, 0, 0, 0]
            yAxis = [0, 1, 0, 0]
            zAxis = [0, 0, 1, 0]

            originRAS = sliceToRAS.MultiplyPoint(origin)
            xAxisRAS = sliceToRAS.MultiplyPoint(xAxis)
            yAxisRAS = sliceToRAS.MultiplyPoint(yAxis)
            zAxisRAS = sliceToRAS.MultiplyPoint(zAxis)

            slicePlaneCoordinates.append([originRAS[0], originRAS[1], originRAS[2]])
            slicePlaneCoordinates.append([ xAxisRAS[0], xAxisRAS[1], xAxisRAS[2]])
            slicePlaneCoordinates.append([ yAxisRAS[0], yAxisRAS[1], yAxisRAS[2]])
            slicePlaneCoordinates.append([ zAxisRAS[0], zAxisRAS[1], zAxisRAS[2]])

            return slicePlaneCoordinates

        def save_coordinates_to_csv(coordinates, filename):
            with open(filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Point", "X", "Y", "Z"])
                writer.writerows(coordinates)

        sliceNode_Red = slicer.mrmlScene.GetNodeByID('vtkMRMLSliceNodeRed')



        if sliceNode_Red:
            coordinates = get_slice_plane_coordinates(sliceNode_Red)

            slicer_base = slicer.app.slicerHome  
            path = os.path.join(slicer_base, "red_slice", self.ui.patientnamelabel.text)
            isExist = os.path.exists(path)
            if not isExist:
                os.makedirs(path)
                print("The new directory:", path, "is created!")
            else:
                print("The new directory:", path, "is not created!")
                exit
                          
           
            location=self.ui.locationcomboBox.currentText    
            
            file_name = path + '/' + location +'.csv'
            save_coordinates_to_csv(coordinates, file_name)
            print('red_Coordinates:',file_name)
              

    def onredreset(self) -> None:

        slicer_base = slicer.app.slicerHome        
        slice_dir = os.path.join(slicer_base, "red_slice", self.ui.patientnamelabel.text)
        coordinates_list = os.listdir(slice_dir)      
        
        location2=self.ui.locationcomboBox.currentText
        filename=slice_dir +'/' +  location2 +'.csv'
        
        with open(filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            csv_list=[]
            for line in reader:
                csv_list.append(line)
            print(csv_list[1])
            print(csv_list[4])

        position_coord= list(map(float, csv_list[1]))
        print(position_coord)
        normal_coord = list(map(float, csv_list[4]))
        print(normal_coord)        

            
        def setSlicePoseFromSliceNormalAndPosition(sliceNode, sliceNormal, slicePosition, defaultViewUpDirection=None, backupViewRightDirection=None):
          
          # Fix up input directions
          if defaultViewUpDirection is None:
            defaultViewUpDirection = [0,0,1]
          if backupViewRightDirection is None:
            backupViewRightDirection = [-1,0,0]
          if sliceNormal[1]>=0:
            sliceNormalStandardized = sliceNormal
          else:
            sliceNormalStandardized = [-sliceNormal[0], -sliceNormal[1], -sliceNormal[2]]
          # Compute slice axes
          sliceNormalViewUpAngle = vtk.vtkMath.AngleBetweenVectors(sliceNormalStandardized, defaultViewUpDirection)
          angleTooSmallThresholdRad = 0.25 # about 15 degrees
          if sliceNormalViewUpAngle > angleTooSmallThresholdRad and sliceNormalViewUpAngle < vtk.vtkMath.Pi() - angleTooSmallThresholdRad:
            viewUpDirection = defaultViewUpDirection
            sliceAxisY = viewUpDirection
            sliceAxisX = [0, 0, 0]
            vtk.vtkMath.Cross(sliceAxisY, sliceNormalStandardized, sliceAxisX)
          else:
            sliceAxisX = backupViewRightDirection
          # Set slice axes
          sliceNode.SetSliceToRASByNTP(sliceNormalStandardized[0], sliceNormalStandardized[1], sliceNormalStandardized[2],
            sliceAxisX[0], sliceAxisX[1], sliceAxisX[2],
            slicePosition[0], slicePosition[1], slicePosition[2], 0)

          # Example usage:
        sliceNode = slicer.util.getNode("vtkMRMLSliceNodeRed")
        transformNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode.SetDisplayVisibility(False) 
        transformNode.SetName("slicetransform_red")
        transformNode= slicer.util.getNode("slicetransform_red")

        transformMatrix = vtk.vtkMatrix4x4()
        transformNode.GetMatrixTransformToParent(transformMatrix)
          
        sliceNormal = normal_coord
        slicePosition = position_coord

        setSlicePoseFromSliceNormalAndPosition(sliceNode, sliceNormal, slicePosition)




    def implant_coords_exp(self):

        slicer_base = slicer.app.slicerHome   
        path = os.path.join(slicer_base, "implant_coords", self.ui.patientnamelabel.text)
        
        print(path)
        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)
            slicer.util.infoDisplay("Οι συντεταγμένες του εμφυτεύματος αποθηκεύτηκαν(The implant coordinates saved)!")
            #print("The new directory:", path, "is created!")
        else:
            slicer.util.infoDisplay("Οι συντεταγμένες του εμφυτεύματος αποθηκεύτηκαν(The implant coordinates saved)!")
            #print("The new directory:", path, "is not created!")
            exit
         
        implant_location=self.ui.locationcomboBox.currentText

        markupsNode = slicer.util.getNode(self.ui.pointListComboBox.currentNode().GetName())

        file_name = path + '/' + implant_location +'.csv'        
        
        #print(file_name)

        slicer.modules.markups.logic().ExportControlPointsToCSV(markupsNode, file_name)
        

        


    def implant_coords_imp(self):

        slicer_base = slicer.app.slicerHome
        path = os.path.join(slicer_base, "implant_coords", self.ui.patientnamelabel.text)

        
        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)
            print("The new directory:", path, "is created!")
        else:
            print("The new directory:", path, "is not created!")
            exit
         
        implant_location=self.ui.locationcomboBox.currentText
        newname="_" + implant_location
        markupsNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsCurveNode", newname)
        file_name = path + '/' + implant_location +'.csv'       

        slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUpRedSliceView)
        slicer.modules.markups.logic().ImportControlPointsFromCSV(markupsNode, file_name)




    def onMarkupsToModelNodeChanged(self):
        self.currentMarkupsToModelNode = self.ui.markupsToModelComboBox.currentNode()

        if self.currentMarkupsToModelNode:
            # If this is a new node, initialize defaults
            if self.currentMarkupsToModelNode.GetName().startswith("vtkMRMLMarkupsToModelNode"):
                self.currentMarkupsToModelNode.SetTubeRadius(0.0)
                self.currentMarkupsToModelNode.SetTubeNumberOfSides(20)
                self.currentMarkupsToModelNode.SetTubeCapping(True)
                self.currentMarkupsToModelNode.SetAndObserveInputNodeID(None)
                self.currentMarkupsToModelNode.SetAndObserveOutputModelNodeID(None)
                self.currentMarkupsToModelNode.SetAttribute("Location", "None")
                self.currentMarkupsToModelNode.SetAttribute("TargetDistance", "0")

        self.updateUI()


    def updateUI(self):
        if not self.currentMarkupsToModelNode:
            # Reset UI to defaults
            self.ui.tubeRadiusSpinbox.setValue(0)
            self.ui.tubeSidesSpinBox.setValue(20)
            self.ui.tubeCappingCheckBox.setChecked(True)
            self.ui.pointDistanceSpinBox.setValue(0)
            self.ui.pointListComboBox.setCurrentNode(None)
            self.ui.locationcomboBox.setCurrentText("None")
            return

        # Restore tube parameters
        self.ui.tubeRadiusSpinbox.setValue(self.currentMarkupsToModelNode.GetTubeRadius())
        self.ui.tubeSidesSpinBox.setValue(self.currentMarkupsToModelNode.GetTubeNumberOfSides())
        self.ui.tubeCappingCheckBox.setChecked(self.currentMarkupsToModelNode.GetTubeCapping())

        # Restore location
        location = self.currentMarkupsToModelNode.GetAttribute("Location")
        if location:
            self.ui.locationcomboBox.setCurrentText(location)
        else:
            self.ui.locationcomboBox.setCurrentText("None")

        # Restore target distance
        targetDistance = self.currentMarkupsToModelNode.GetAttribute("TargetDistance")
        if targetDistance is not None:
            self.ui.pointDistanceSpinBox.setValue(float(targetDistance))

        # Restore input node
        inputNode = self.currentMarkupsToModelNode.GetInputNode()
        if inputNode:
            self.ui.pointListComboBox.setCurrentNode(inputNode)
        else:
            self.ui.pointListComboBox.setCurrentNode(None)


    def onNodAdd(self, addedNode):
        if isinstance(addedNode, slicer.vtkMRMLMarkupsToModelNode):
            addedNode.SetTubeRadius(0.0)
            addedNode.SetTubeNumberOfSides(20)
            addedNode.SetTubeCapping(True)
            addedNode.SetAndObserveInputNodeID(None)
            addedNode.SetAndObserveOutputModelNodeID(None)
            addedNode.SetAttribute("TargetDistance", "0")
            addedNode.SetAttribute("Location", "None")



    def onApply(self):
        if not self.currentMarkupsToModelNode or not isinstance(self.currentMarkupsToModelNode, slicer.vtkMRMLMarkupsToModelNode):
            slicer.util.errorDisplay("Invalid MarkupsToModel node selected.")
            return

        # Configure node as curve
        self.currentMarkupsToModelNode.SetModelType(self.currentMarkupsToModelNode.Curve)

        # Update parameters
        self.currentMarkupsToModelNode.SetTubeRadius(self.ui.tubeRadiusSpinbox.value)
        self.currentMarkupsToModelNode.SetTubeNumberOfSides(self.ui.tubeSidesSpinBox.value)
        self.currentMarkupsToModelNode.SetTubeCapping(self.ui.tubeCappingCheckBox.isChecked())

        # Save location
        location_name = self.ui.locationcomboBox.currentText.strip()
        if not location_name or location_name.lower() == "none":
            slicer.util.errorDisplay("Please select a valid Location before applying.")
            return
        self.currentMarkupsToModelNode.SetAttribute("Location", location_name)

        # Ensure input node is set
        pointListNodeID = self.ui.pointListComboBox.currentNodeID
        if not pointListNodeID:
            slicer.util.errorDisplay("No point list selected.")
            return
        self.currentMarkupsToModelNode.SetAndObserveInputNodeID(pointListNodeID)

        # Find or create output model by location name
        existing_models = [
            node for node in slicer.util.getNodesByClass("vtkMRMLModelNode")
            if node.GetName() == location_name
        ]
        if existing_models:
            outputModelNode = existing_models[0]
        else:
            outputModelNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelNode", location_name)

        self.currentMarkupsToModelNode.SetAndObserveOutputModelNodeID(outputModelNode.GetID())

        # Save target distance
        targetDistance = self.ui.pointDistanceSpinBox.value
        self.currentMarkupsToModelNode.SetAttribute("TargetDistance", str(targetDistance))

        # Adjust points
        pointListNode = self.ui.pointListComboBox.currentNode()
        if pointListNode:
            self.adjust_points_to_maintain_distance(pointListNode, targetDistance)

        # Generate model
        slicer.modules.markupstomodel.logic().UpdateOutputModel(self.currentMarkupsToModelNode)

        # Set display properties
        displayNode = outputModelNode.GetDisplayNode()
        if displayNode:
            displayNode.SetOpacity(1.0)
            displayNode.SetVisibility3D(True)
            displayNode.SetVisibility2D(True)

        slicer.util.infoDisplay("Pre_implant updated!")
        self.FilterTreeItems_2()

        

    def onnewpoint(self):       
       
        placeModePersistence = 1
        slicer.modules.markups.logic().StartPlaceMode(placeModePersistence) # Ensure 'Place multiple control points' is active        




    def adjust_points_to_maintain_distance(self, pointListNode, targetDistance):
        import numpy as np

        numPoints = pointListNode.GetNumberOfControlPoints()
        if numPoints < 2:
            return

        points = []
        for i in range(numPoints):
            point = [0.0, 0.0, 0.0]
            pointListNode.GetNthControlPointPosition(i, point)
            points.append(point)

        adjustedPoints = [points[0]]
        for i in range(1, len(points)):
            direction = np.array(points[i]) - np.array(adjustedPoints[-1])
            directionLength = np.linalg.norm(direction)
            if directionLength > 0:
                direction = direction / directionLength
            newPoint = np.array(adjustedPoints[-1]) + direction * targetDistance
            adjustedPoints.append(newPoint.tolist())

        pointListNode.RemoveAllControlPoints()
        for point in adjustedPoints:
            pointListNode.AddControlPoint(point)



    def alignModelToVector(self, modelNode, pointListNode):
        import numpy as np
        import vtk

        pointA = [0.0, 0.0, 0.0]
        pointB = [0.0, 0.0, 0.0]
        pointListNode.GetNthControlPointPosition(0, pointA)
        pointListNode.GetNthControlPointPosition(1, pointB)

        direction = np.array(pointB) - np.array(pointA)
        direction_norm = np.linalg.norm(direction)
        if direction_norm == 0:
            slicer.util.errorDisplay("Control points are identical — cannot compute direction.")
            return
        direction_unit = direction / direction_norm

        z_axis = np.array([0, 0, 1])
        rotation_axis = np.cross(z_axis, direction_unit)
        rotation_axis_norm = np.linalg.norm(rotation_axis)
        if rotation_axis_norm != 0:
            rotation_axis /= rotation_axis_norm
        angle_rad = np.arccos(np.clip(np.dot(z_axis, direction_unit), -1.0, 1.0))
        angle_deg = np.degrees(angle_rad)

        alignmentTransform = vtk.vtkTransform()
        alignmentTransform.RotateWXYZ(angle_deg, *rotation_axis)
        alignmentTransform.Translate(pointA)

        transformNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode.SetAndObserveTransformToParent(alignmentTransform)
        modelNode.SetAndObserveTransformNodeID(transformNode.GetID())

        return transformNode


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
                if any(keyword in name for keyword in ["maxilla", "upper", "lower","mandible","canal","model", "v", "guide"]):               
                    shItemID = shNode.GetItemByDataNode(modelNode)
                    if shItemID:
                        shNode.SetItemAttribute(shItemID, "Category", categoryName)

            # Assign category to relevant TRANSFORM nodes
            for markupsNode in slicer.util.getNodesByClass("vtkMRMLMarkupsFiducialNode"):
                name = markupsNode.GetName().lower()
                if "p" in name:  # Only transforms with 'p'
                    shItemID = shNode.GetItemByDataNode(markupsNode)
                    if shItemID:
                        shNode.SetItemAttribute(shItemID, "Category", categoryName)

            # Refresh the subject hierarchy tree filter
            tree = self.ui.RestSubjectHierarchyTreeView
            tree.setMRMLScene(None)  # Temporarily detach to clear previous filters
            tree.addItemAttributeFilter("Category", categoryName)  # Apply updated filter
            tree.setContextMenuEnabled(True)
            tree.setMRMLScene(slicer.mrmlScene)  # Re-attach scene to refresh
    

    # Define the implant list function
    def update_implant_list(self, selected_brand):
        
        self.ui.selectimplantcomboBox.clear() 
        if selected_brand == 'MIS_7 Implant System':
            self.ui.selectimplantcomboBox.addItems(self.mis_7_XD_implant_list)
        else:
            self.ui.selectimplantcomboBox.addItem('None')


    def createCenteredSolidTaperedTube(self,D1, D2, length):
        # Compute taper angle
        angle_rad = math.atan((D1 - D2) / (2 * length))
        taper_angle_deg = math.degrees(angle_rad)
        print(f"Taper angle: {taper_angle_deg:.2f} degrees")

        resolution = 60

        # Base circle
        circle1 = vtk.vtkRegularPolygonSource()
        circle1.SetRadius(D1 / 2.0)
        circle1.SetNumberOfSides(resolution)
        circle1.SetCenter(0, 0, 0)
        circle1.GeneratePolygonOff()
        circle1.Update()

        # Top circle
        circle2 = vtk.vtkRegularPolygonSource()
        circle2.SetRadius(D2 / 2.0)
        circle2.SetNumberOfSides(resolution)
        circle2.SetCenter(0, 0, length)
        circle2.GeneratePolygonOff()
        circle2.Update()

        # Side surface
        appendEdges = vtk.vtkAppendPolyData()
        appendEdges.AddInputData(circle1.GetOutput())
        appendEdges.AddInputData(circle2.GetOutput())
        appendEdges.Update()

        tube = vtk.vtkRuledSurfaceFilter()
        tube.SetInputData(appendEdges.GetOutput())
        tube.SetResolution(resolution, 1)
        tube.SetRuledModeToResample()
        tube.Update()

        # Caps
        cap1 = vtk.vtkDiskSource()
        cap1.SetInnerRadius(0.0)
        cap1.SetOuterRadius(D1 / 2.0)
        cap1.SetRadialResolution(1)
        cap1.SetCircumferentialResolution(resolution)
        cap1.Update()

        cap2 = vtk.vtkDiskSource()
        cap2.SetInnerRadius(0.0)
        cap2.SetOuterRadius(D2 / 2.0)
        cap2.SetRadialResolution(1)
        cap2.SetCircumferentialResolution(resolution)
        cap2.Update()

        transform = vtk.vtkTransform()
        transform.Translate(0, 0, length)
        transformFilter = vtk.vtkTransformPolyDataFilter()
        transformFilter.SetTransform(transform)
        transformFilter.SetInputData(cap2.GetOutput())
        transformFilter.Update()

        # Combine all parts
        combined = vtk.vtkAppendPolyData()
        combined.AddInputData(tube.GetOutput())
        combined.AddInputData(cap1.GetOutput())
        combined.AddInputData(transformFilter.GetOutput())
        combined.Update()

        # Clean up
        clean = vtk.vtkCleanPolyData()
        clean.SetInputData(combined.GetOutput())
        clean.Update()

        # Center the model
        polyData = clean.GetOutput()
        bounds = [0]*6
        polyData.GetBounds(bounds)
        center = [
            (bounds[0] + bounds[1]) / 2.0,
            (bounds[2] + bounds[3]) / 2.0,
            (bounds[4] + bounds[5]) / 2.0,
        ]

        transformCenter = vtk.vtkTransform()
        transformCenter.Translate(-center[0], -center[1], -center[2])

        transformCenterFilter = vtk.vtkTransformPolyDataFilter()
        transformCenterFilter.SetTransform(transformCenter)
        transformCenterFilter.SetInputData(polyData)
        transformCenterFilter.Update()

        # Create model node
        modelNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelNode", "CenteredCappedTaperedTube")
        modelNode.SetAndObservePolyData(transformCenterFilter.GetOutput())

        displayNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelDisplayNode")
        slicer.mrmlScene.AddNode(displayNode)
        modelNode.SetAndObserveDisplayNodeID(displayNode.GetID())
        displayNode.SetColor(0.2, 1.0, 0.8)
        displayNode.SetOpacity(1.0)
        displayNode.SetVisibility2D(True)
        displayNode.SetVisibility3D(True)

        slicer.util.resetThreeDViews()

        return taper_angle_deg, modelNode


        
    def createimplantaxis(self, radius, height, resolution):
        axisnode = vtk.vtkCylinderSource()
        axisnode.SetRadius(radius)
        axisnode.SetHeight(height)
        axisnode.SetResolution(resolution)
        axisnode.Update()

        # Rotate from Y-axis to Z-axis
        transform = vtk.vtkTransform()
        transform.RotateX(-90)
        transformFilter = vtk.vtkTransformPolyDataFilter()
        transformFilter.SetTransform(transform)
        transformFilter.SetInputConnection(axisnode.GetOutputPort())
        transformFilter.Update()

        # Clean the result
        clean = vtk.vtkCleanPolyData()
        clean.SetInputData(transformFilter.GetOutput())
        clean.Update()

        # Center the model
        polyData = clean.GetOutput()
        bounds = [0]*6
        polyData.GetBounds(bounds)
        center = [
            (bounds[0] + bounds[1]) / 2.0,
            (bounds[2] + bounds[3]) / 2.0,
            (bounds[4] + bounds[5]) / 2.0,
        ]

        transformCenter = vtk.vtkTransform()
        transformCenter.Translate(-center[0], -center[1], -center[2])

        transformCenterFilter = vtk.vtkTransformPolyDataFilter()
        transformCenterFilter.SetTransform(transformCenter)
        transformCenterFilter.SetInputData(polyData)
        transformCenterFilter.Update()        

        modelNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelNode", 'Implant Axis')
        modelNode.SetAndObservePolyData(transformFilter.GetOutput())

        displayNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelDisplayNode")
        slicer.mrmlScene.AddNode(displayNode)
        modelNode.SetAndObserveDisplayNodeID(displayNode.GetID())
        displayNode.SetColor(0.2, 0.6, 1.1)
        displayNode.SetOpacity(1.0)
        displayNode.SetVisibility2D(True)
        displayNode.SetVisibility3D(True)

        slicer.util.resetThreeDViews()

        return radius, height, resolution, modelNode



    def createHollowTaperedTube(self, OD1, OD2, ID1, ID2, height, pointListNode=None):
        resolution = 60

        # Outer bottom circle
        outerBottom = vtk.vtkRegularPolygonSource()
        outerBottom.SetRadius(OD1 / 2.0)
        outerBottom.SetNumberOfSides(resolution)
        outerBottom.SetCenter(0, 0, 0)
        outerBottom.GeneratePolygonOff()
        outerBottom.Update()
        #print(outerBottom)

        # Outer top circle
        outerTop = vtk.vtkRegularPolygonSource()
        outerTop.SetRadius(OD2 / 2.0)
        outerTop.SetNumberOfSides(resolution)
        outerTop.SetCenter(0, 0, height)
        outerTop.GeneratePolygonOff()
        outerTop.Update()
        #print(outerTop)

        # Inner bottom circle (reversed)
        innerBottom = vtk.vtkRegularPolygonSource()
        innerBottom.SetRadius(ID1 / 2.0)
        innerBottom.SetNumberOfSides(resolution)
        innerBottom.SetCenter(0, 0, 0)
        innerBottom.GeneratePolygonOff()
        innerBottom.Update()
        #print(innerBottom)

        # Reverse the inner bottom circle direction
        revInnerBottom = vtk.vtkReverseSense()
        revInnerBottom.SetInputData(innerBottom.GetOutput())
        revInnerBottom.ReverseCellsOn()
        revInnerBottom.ReverseNormalsOn()
        revInnerBottom.Update()
        
        # Inner top circle (reversed)
        innerTop = vtk.vtkRegularPolygonSource()
        innerTop.SetRadius(ID2 / 2.0)
        innerTop.SetNumberOfSides(resolution)
        innerTop.SetCenter(0, 0, height)
        innerTop.GeneratePolygonOff()
        innerTop.Update()

        revInnerTop = vtk.vtkReverseSense()
        revInnerTop.SetInputData(innerTop.GetOutput())
        revInnerTop.ReverseCellsOn()
        revInnerTop.ReverseNormalsOn()
        revInnerTop.Update()

        # Loft outer wall
        appendOuter = vtk.vtkAppendPolyData()
        appendOuter.AddInputData(outerBottom.GetOutput())
        appendOuter.AddInputData(outerTop.GetOutput())
        appendOuter.Update()

        outerWall = vtk.vtkRuledSurfaceFilter()
        outerWall.SetInputData(appendOuter.GetOutput())
        outerWall.SetResolution(resolution, 1)
        outerWall.SetRuledModeToResample()
        outerWall.Update()

        # Loft inner wall (reversed to face inward)
        appendInner = vtk.vtkAppendPolyData()
        appendInner.AddInputData(revInnerBottom.GetOutput())
        appendInner.AddInputData(revInnerTop.GetOutput())
        appendInner.Update()

        innerWall = vtk.vtkRuledSurfaceFilter()
        innerWall.SetInputData(appendInner.GetOutput())
        innerWall.SetResolution(resolution, 1)
        innerWall.SetRuledModeToResample()
        innerWall.Update()

        # Cap bottom ring
        capBottom = vtk.vtkDiskSource()
        capBottom.SetInnerRadius(ID1 / 2.0)
        capBottom.SetOuterRadius(OD1 / 2.0)
        capBottom.SetRadialResolution(1)
        capBottom.SetCircumferentialResolution(resolution)
        capBottom.Update()

        # Cap top ring (translated up)
        capTop = vtk.vtkDiskSource()
        capTop.SetInnerRadius(ID2 / 2.0)
        capTop.SetOuterRadius(OD2 / 2.0)
        capTop.SetRadialResolution(1)
        capTop.SetCircumferentialResolution(resolution)
        capTop.Update()

        transformTop = vtk.vtkTransform()
        transformTop.Translate(0, 0, height)
        transformTopFilter = vtk.vtkTransformPolyDataFilter()
        transformTopFilter.SetTransform(transformTop)
        transformTopFilter.SetInputData(capTop.GetOutput())
        transformTopFilter.Update()

        # Combine all surfaces
        combined = vtk.vtkAppendPolyData()
        combined.AddInputData(outerWall.GetOutput())
        combined.AddInputData(innerWall.GetOutput())
        combined.AddInputData(capBottom.GetOutput())
        combined.AddInputData(transformTopFilter.GetOutput())
        combined.Update()

        # Clean the result
        clean = vtk.vtkCleanPolyData()
        clean.SetInputData(combined.GetOutput())
        clean.Update()

        # Center the model
        polyData = clean.GetOutput()
        bounds = [0]*6
        polyData.GetBounds(bounds)
        center = [
            (bounds[0] + bounds[1]) / 2.0,
            (bounds[2] + bounds[3]) / 2.0,
            (bounds[4] + bounds[5]) / 2.0,
        ]

        transformCenter = vtk.vtkTransform()
        transformCenter.Translate(-center[0], -center[1], -center[2])

        transformCenterFilter = vtk.vtkTransformPolyDataFilter()
        transformCenterFilter.SetTransform(transformCenter)
        transformCenterFilter.SetInputData(polyData)
        transformCenterFilter.Update()

        # Create Slicer model
        modelNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelNode", "HollowTaperedTube")
        modelNode.SetAndObservePolyData(transformCenterFilter.GetOutput())
       

        # Align to vector if pointListNode is provided
        if pointListNode:
            self.alignModelToVector(modelNode, pointListNode)
            
        displayNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelDisplayNode")
        slicer.mrmlScene.AddNode(displayNode)
        modelNode.SetAndObserveDisplayNodeID(displayNode.GetID())
        displayNode.SetColor(0.2, 0.6, 1.0)  # orange
        displayNode.SetOpacity(1.0)
        displayNode.SetVisibility2D(True)        
        displayNode.SetVisibility3D(True)

        slicer.util.resetThreeDViews()
            

        return modelNode, outerBottom, outerTop,innerBottom     
    

    def createimplantcylinder(self, radius, height, resolution, pointListNode=None):
        import vtk
        import numpy as np

        # Create cylinder
        axisnode = vtk.vtkCylinderSource()
        axisnode.SetRadius(radius)
        axisnode.SetHeight(height)
        axisnode.SetResolution(resolution)
        axisnode.Update()

        # Rotate from Y-axis to Z-axis
        transform = vtk.vtkTransform()
        transform.RotateX(-90)
        transformFilter = vtk.vtkTransformPolyDataFilter()
        transformFilter.SetTransform(transform)
        transformFilter.SetInputConnection(axisnode.GetOutputPort())
        transformFilter.Update()

        # Clean and center
        clean = vtk.vtkCleanPolyData()
        clean.SetInputData(transformFilter.GetOutput())
        clean.Update()

        polyData = clean.GetOutput()
        bounds = [0]*6
        polyData.GetBounds(bounds)
        center = [(bounds[i] + bounds[i+1]) / 2.0 for i in range(0, 6, 2)]

        transformCenter = vtk.vtkTransform()
        transformCenter.Translate(-center[0], -center[1], -center[2])

        transformCenterFilter = vtk.vtkTransformPolyDataFilter()
        transformCenterFilter.SetTransform(transformCenter)
        transformCenterFilter.SetInputData(polyData)
        transformCenterFilter.Update()

        # Create model node
        modelNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelNode", 'Implant Cylinder')
        modelNode.SetAndObservePolyData(transformCenterFilter.GetOutput())

        # Align to vector if pointListNode is provided
        if pointListNode:
            self.alignModelToVector(modelNode, pointListNode)


        displayNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelDisplayNode")
        slicer.mrmlScene.AddNode(displayNode)
        modelNode.SetAndObserveDisplayNodeID(displayNode.GetID())
        displayNode.SetVisibility2D(False)
        displayNode.SetVisibility3D(False)

        slicer.util.resetThreeDViews()    

        return radius, height, resolution, modelNode   

    def onmodifypoints(self):        
      
        pointnode=self.ui.pointListComboBox.currentNode()
        slicer.mrmlScene.RemoveNode(pointnode)
        self.ui.pointListComboBox.setCurrentNode(None)


        for modelNode in slicer.util.getNodesByClass("vtkMRMLModelNode"):
            name = modelNode.GetName()
            if name == self.ui.locationcomboBox.currentText:
                slicer.mrmlScene.RemoveNode(modelNode)
                self.FilterTreeItems_2()

    def create_up_generic_implant(self):
        MIS7XD_libUp.create_generic_implant_MIS7XD(self.ui, self)

    def create_low_generic_implant(self):
        MIS7XD_libLow.create_generic_implant_MIS7XD(self.ui, self)


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
        
            
    def setParameterNode(self, inputParameterNode: Optional[GenericImplCreatorParameterNode]) -> None:
        if self._parameterNode:
            try:
                self._parameterNode.disconnectGui(self._parameterNodeGuiTag)
            except Exception:
                pass
            self._parameterNodeGuiTag = None

        self._parameterNode = inputParameterNode

        if self._parameterNode:
            guiWrapper = GenericImplCreatorGui(self.ui)
            self._parameterNodeGuiTag = self._parameterNode.connectGui(guiWrapper)


# GenericImplCreatorLogic
#


class GenericImplCreatorLogic(ScriptedLoadableModuleLogic):
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
        return GenericImplCreatorParameterNode(super().getParameterNode())


# GenericImplCreatorTest
#

class GenericImplCreatorTest(ScriptedLoadableModuleTest):
    pass




