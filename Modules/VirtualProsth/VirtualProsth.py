import logging
import os
from typing import Annotated, Optional
import csv
import vtk
import ctk
import random
import numpy as np
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
from slicer.parameterNodeWrapper import parameterNodeWrapper
from slicer import vtkMRMLScalarVolumeNode
import re
import random

#
# VirtualProsth
#


class VirtualProsth(ScriptedLoadableModule):

    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = _("Virtual Prosthetics")  
        self.parent.categories = [translate("qSlicerAbstractCoreModule", "Examples")]
        self.parent.dependencies = []  
        self.parent.contributors = ["Dimitris Trikeriotis (Gnathion)"]  
        self.parent.helpText = _("""
Simulate the rehabilitation process by placing prosthetic parts, ensuring prosthetic-driven implant planning (‘top-down’ approach).
See more information in <a href="https://github.com/organization/projectname#VirtualProsth">module documentation</a>.
""")
        self.parent.acknowledgementText = _("""
This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc., Andras Lasso, PerkLab,
and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
""")

# VirtualProsthParameterNode

'''
The parameters needed by the module.
RegisteSubjectHierarchyTreeView was commented out
because of the error: "Unable to create serializer for {classtype} member {name}")
probably due to the fact that no GUI connector is yet available. Fix????
'''

@parameterNodeWrapper
class VirtualProsthParameterNode:

    prosthcomboBox:str = "None"
    implantlocscomboBox: str = "None"
    locationcomboBox: str = "None"
    rotationslider:  Annotated[int, WithinRange(-50, 50)]  = 0
    translationslider: Annotated[int, WithinRange(-50, 50)]  = 0
    axisX: bool = False
    axisY: bool = False
    axisZ: bool = False
    translonX: bool = False
    translonY: bool = False
    translonZ: bool = False  
    #ProsthTreeViewSubjectHierarchyTreeView:slicer.qMRMLSubjectHierarchyTreeView= None

'''
Because of the error:AttributeError: 'dict' object has no attribute '__dict__'
instead of passing a dictionary directly to connectGui()
an object/class (self.ui) is used, that contains all the named widgets.
'''    

class VirtualProsthGui:
    def __init__(self, ui):
        
        self.prosthcomboBox = ui.prosthcomboBox
        self.implantlocscomboBox = ui.implantlocscomboBox
        self.locationcomboBox = ui.locationcomboBox

        self.rotationslider = ui.rotationslider
        self.translationslider = ui.translationslider

        self.axisX = ui.axisX
        self.axisY = ui.axisY
        self.axisZ = ui.axisZ
        self.translonX = ui.translonX
        self.translonY = ui.translonY
        self.translonZ = ui.translonZ
        
        #self.ProsthTreeViewSubjectHierarchyTreeView = ui.ProsthTreeViewSubjectHierarchyTreeView

     

class VirtualProsthWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):


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
    """Uses ScriptedLoadableModule base class, available at:
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
        uiWidget = slicer.util.loadUI(self.resourcePath("UI/VirtualProsth.ui"))
        print(self.resourcePath("UI/VirtualProsth.ui"))
        print(self.resourcePath("Icons"))
        path=self.resourcePath("Icons")

        icon_itemList = os.listdir(path)
        for item in icon_itemList:
            print(item)
            #self.ui.prosthcomboBox.addItem(item)

            
        path2=self.resourcePath("teeth")

        teeth_itemList = os.listdir(path2)
        for item in teeth_itemList:
            print(item)
            #self.ui.prosthcomboBox.addItem(item)
            
        
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
        self.logic = VirtualProsthLogic()

        # Connections

        # These connections ensure that we update parameter node when scene is closed
        self.addObserver(slicer.mrmlScene, slicer.mrmlScene.StartCloseEvent, self.onSceneStartClose)
        self.addObserver(slicer.mrmlScene, slicer.mrmlScene.EndCloseEvent, self.onSceneEndClose)

        # Buttons
        
        self.ui.selectprosthpointButton.connect("clicked(bool)", self.onselectprosthpointButton)
        self.ui.exportlocButton.connect("clicked(bool)", self.onredexport)
        self.ui.importlocButton.connect("clicked(bool)", self.onredreset)
        self.ui.modeltreeButton.connect("clicked(bool)", self.onmodeltreeButton)
        
        self.redSliceNode = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeRed")

        # Connect rotation slider
        self.lastRotation = {"x": 0, "y": 0, "z": 0}
        self.currentAxis = "x"  # default
          
        self.ui.rotationslider.valueChanged.connect(self.onRotationSliderChanged)

        # Connect rotation checkboxes
        self.ui.axisX.toggled.connect(lambda checked: self.onAxisSelected("X", checked))
        self.ui.axisY.toggled.connect(lambda checked: self.onAxisSelected("Y", checked))
        self.ui.axisZ.toggled.connect(lambda checked: self.onAxisSelected("Z", checked))

        # Connect translation slider
        # Track last translations per axis
        self.lastTranslation = {"x": 0, "y": 0, "z": 0}
        self.currentTransAxis = "x"  # default

        self.ui.translationslider.valueChanged.connect(self.onTranslationSliderChanged)

        # Connect translation checkboxes
        self.ui.translonX.toggled.connect(self.ontranslonX)
        self.ui.translonY.toggled.connect(self.ontranslonY)
        self.ui.translonZ.toggled.connect(self.ontranslonZ)

        # Track current axis
        self.currentAxis = None

        self.ui.implantlocscomboBox.currentTextChanged.connect(self.on_implantlocscomboBox_changed)          
        self.ui.implantlocscomboBox.addItem('None')
        self.update_implocationlist()
        
        self.populate_locationList()
        
        self.retrievepatient()
        #self.ui.prosthcomboBox.addItem('None')
        self.update_implocationlist()

        self.FilterTreeItems_4()

        self.ui.grbutton.connect('clicked(bool)', self.OnGreek)
        self.ui.engbutton.connect('clicked(bool)', self.OnEnglish)
        self.ui.homeButton.connect("clicked(bool)", self.onhomeButton)

        self.ui.widescreenButton.connect("clicked(bool)", self.onwidescreenButton)
        self.ui.custom1screenButton.connect("clicked(bool)", self.customlayout1)
        self.ui.redcreenButton.connect("clicked(bool)", self.onredcreenButton)
        self.ui.dscreenButton.connect("clicked(bool)", self.ondscreenButton)

        self.widescreenButton()
        self.custom1screenButton()
        self.redcreenButton()
        self.dscreenButton()
 
        self.greek()
        self.english()
        
        self.ui.patientnamelabel.hide()

        self.ui.dentimButton.connect("clicked(bool)", self.ondentimButton)
        self.ui.registButton.connect("clicked(bool)", self.onregistButton)
        self.ui.genimplButton.connect("clicked(bool)", self.ongenimplButton)

        self.dentimButton()
        self.registButton()
        self.genimplButton()
        self.homeButton()
        self.populate_teeth()

        self.dataButton()
        self.ui.databutton.connect("clicked(bool)", self.ondataButton)  




        

        # Make sure parameter node is initialized (needed for module reload)
        self.initializeParameterNode()

        # Get the base Slicer installation directory
        slicer_base = slicer.app.slicerHome 


    def dataButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "vpOSData.png"))
        self.ui.databutton.setIcon(icon)           
    
    def ondataButton(self):
        slicer.util.selectModule("OralSurgData")
        slicer.util.reloadScriptedModule("OralSurgData")


    def populate_teeth(self):        
        
        path3=self.resourcePath("teeth")
        teeth3_itemList = os.listdir(path3)
        for item in teeth3_itemList:
            print(item)
            self.ui.prosthcomboBox.addItem(item)            

    def homeButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "vpOrSurgMod.png"))
        self.ui.homeButton.setIcon(icon)

    def dentimButton(self):        
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "vpDentImplIm.png"))
        self.ui.dentimButton.setIcon(icon)

    def registButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "vpRegisterMod.png"))
        self.ui.registButton.setIcon(icon)
    
    def genimplButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "vpGenIImplCr.png"))
        self.ui.genimplButton.setIcon(icon)

    def ondentimButton(self):
        slicer.util.selectModule("DentImplImaging")
        #slicer.util.reloadScriptedModule("DentImplImaging")

    def onregistButton(self):
        slicer.util.selectModule("RegisterModule")
        #slicer.util.reloadScriptedModule("RegisterModule")

    
    def ongenimplButton(self):
        slicer.util.selectModule("GenericImplCreator")
        #slicer.util.reloadScriptedModule("GenericImplCreator")                


    def widescreenButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "vpws.png"))        
        self.ui.widescreenButton.setIcon(icon)

    def custom1screenButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "vpcs.png"))
        self.ui.custom1screenButton.setIcon(icon)


    def redcreenButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "vpred.png"))
        self.ui.redcreenButton.setIcon(icon)

    def dscreenButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "vp3d.png"))
        self.ui.dscreenButton.setIcon(icon)

    def onwidescreenButton(self):
        slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutConventionalWidescreenView)

    def onredcreenButton(self):
        slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUpRedSliceView)

    def ondscreenButton(self):
        slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUp3DView)                  

    def update_implocationlist(self):
        slicer_base = slicer.app.slicerHome
        #slice_dir = slicer_base + 'red_slice' + '/' + self.ui.patientnamelabel.text + '/'
        slice_dir = os.path.join(slicer_base, "red_slice", self.ui.patientnamelabel.text)
        

        self.ui.implantlocscomboBox.clear()  # clear old items

        if not os.path.exists(slice_dir):
            print('Folder:', slice_dir, 'does not exist!')
            return

        # Sort list so latest files are last (optional, depending on how you want it)
        locations_itemList = sorted(os.listdir(slice_dir))

        for item in locations_itemList:
            print(item)
            self.ui.implantlocscomboBox.addItem(item)
               

        if locations_itemList:
            # Select the last item by default
            self.ui.implantlocscomboBox.setCurrentIndex(len(locations_itemList)-1)
                                
            print(self.ui.implantlocscomboBox.count)
            print(len(locations_itemList))


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



    def populate_locationList(self):
        location_list= ['None',
                '17', '16', '15', '14', '13','12','11',
                '21', '22', '23', '24', '25','26','27',
                '37', '36', '35', '34', '33','32','31',
                '41', '42', '43', '44', '45','46','47'
                ]       
        for loc in location_list:
            self.ui.locationcomboBox.addItem(loc) 

            
        
    def onhomeButton(self):
        slicer.util.selectModule("OralSurgModuleHome")
        #slicer.util.reloadScriptedModule("OralSurgModuleHome")      


    def greek(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "vpgr.png"))        
        self.ui.grbutton.setIcon(icon)


    def english(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "vpeng.png"))
        self.ui.engbutton.setIcon(icon)   


    def OnEnglish(self):
        
        self.ui.prosthCollapsibleButton.setText("Prosthetic rehabilitation simulation")    
        self.ui.label.setText("Select Prosthesis:")        
        self.ui.selectprosthpointButton.setText("Import Prosthesis by Clicking to a Point")
        self.ui.rotationValueLabel.setText("Rotate Slice:")
        self.ui.translationValueLabel.setText("Translate Slice:")
        self.ui.label_16.setText("Implant Location:")
        self.ui.exportlocButton.setText("Export Slice")
        self.ui.importlocButton.setText("Import Slice")
        self.ui.label_17.setText("Slice Coords:")
       

    def OnGreek(self):
    
        self.ui.prosthCollapsibleButton.setText("Προσομοίωση προσθετικής αποκατάστασης")    
        self.ui.label.setText("Επιλογή προσθετικής:")        
        self.ui.selectprosthpointButton.setText("Εισαγωγή Προσθετικής με click σε ένα Σημείο")
        self.ui.rotationValueLabel.setText("Περιστροφή τομής:")
        self.ui.translationValueLabel.setText("Μετατόπιση τομής:")
        self.ui.label_16.setText("Θέση προς εμφύτευση:")
        self.ui.exportlocButton.setText("Εξαγωγή Τομής")
        self.ui.importlocButton.setText("Εισαγωγή Τομής")
        self.ui.label_17.setText("Συντεταγμένες Τομής:")


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

        # Replace 'Red', 'red', or 'Yellow' with the actual slice node name you want to extract coordinates from
        sliceNode_Red = slicer.mrmlScene.GetNodeByID('vtkMRMLSliceNodeRed')



        if sliceNode_Red:
            coordinates = get_slice_plane_coordinates(sliceNode_Red)

            slicer_base = slicer.app.slicerHome

  
            #path=slicer_base + 'red_slice' + '/' + self.ui.patientnamelabel.text
            path = os.path.join(slicer_base, "red_slice", self.ui.patientnamelabel.text)
            isExist = os.path.exists(path)
            if not isExist:
                os.makedirs(path)
                #print("The new directory:", path, "is created!")
            else:
                #print("The new directory:", path, "is not created!")
                exit
                          
            

            # Save the filename you just created
            location = self.ui.locationcomboBox.currentText
            new_file_name = location + '.csv'

            # Save coordinates
            file_path = os.path.join(path, new_file_name)
            save_coordinates_to_csv(coordinates, file_path)

            # Refresh list
            self.update_implocationlist()

            # Explicitly set ComboBox to the newly added file
            index = self.ui.implantlocscomboBox.findText(new_file_name, qt.Qt.MatchExactly)
            if index != -1:
                self.ui.implantlocscomboBox.setCurrentIndex(index)
      
            
            

    def onredreset(self) -> None:

        slicer_base = slicer.app.slicerHome

        #slice_dir=slicer_base + 'red_slice' + '/' + self.ui.patientnamelabel.text + '/'
        slice_dir = os.path.join(slicer_base, "red_slice", self.ui.patientnamelabel.text)

        coordinates_list = os.listdir(slice_dir)
       
        #location2=self.ui.primplmodelNodeComboBox.currentNode()
        #location2=self.ui.primplmodelNodeComboBox.currentNode().GetName()
        location2=self.ui.locationcomboBox.currentText

        filename=slice_dir +'/' +  location2 +'.csv'

        #'green_slice_plane_coordinates3.csv'
        with open(filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            csv_list=[]
            for line in reader:
                csv_list.append(line)
            #print(csv_list[1])
            #print(csv_list[4])


        position_coord= list(map(float, csv_list[1]))
        #print(position_coord)
        normal_coord = list(map(float, csv_list[4]))
        #print(normal_coord)        

            
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


    def angulate_slice(self, sliceNode, angleDegrees, axis):
        
       
        """
        Angulate a specific slice node by a given angle and axis.

        :param sliceNode: vtkMRMLSliceNode, the slice node to angulate.
        :param angleDegrees: float, angle in degrees to rotate.
        :param axis: list or numpy array of 3 elements, the axis of rotation (e.g., [1, 0, 0]).
        """
        # Normalize the axis of rotation
        axis = np.array(axis)
        axis = axis / np.linalg.norm(axis)

        # Create a transform object to compute the rotation
        transform = vtk.vtkTransform()
        transform.RotateWXYZ(angleDegrees, axis[0], axis[1], axis[2])

        # Get the current SliceToRAS matrix
        currentMatrix = sliceNode.GetSliceToRAS()

        # Apply the rotation to the current matrix
        rotationMatrix = vtk.vtkMatrix4x4()
        transform.GetMatrix(rotationMatrix)

        newMatrix = vtk.vtkMatrix4x4()
        vtk.vtkMatrix4x4.Multiply4x4(rotationMatrix, currentMatrix, newMatrix)

        # Update the slice node with the new matrix
        sliceNode.GetSliceToRAS().DeepCopy(newMatrix)
        sliceNode.UpdateMatrices()


    def onAxisSelected(self, axisName, checked):
        if checked:
            # Only allow one axis at a time
            if axisName == "X":
                self.ui.axisY.setChecked(False)
                self.ui.axisZ.setChecked(False)
                self.currentAxis = [1, 0, 0]
            elif axisName == "Y":
                self.ui.axisX.setChecked(False)
                self.ui.axisZ.setChecked(False)
                self.currentAxis = [0, 1, 0]
            elif axisName == "Z":
                self.ui.axisX.setChecked(False)
                self.ui.axisY.setChecked(False)
                self.currentAxis = [0, 0, 1]

            # Reset slider to 0 whenever switching axis
            self.ui.rotationslider.blockSignals(True)
            self.ui.rotationslider.setValue(0)
            self.ui.rotationslider.blockSignals(False)
        else:
            self.currentAxis = None
            self.ui.rotationslider.setValue(0)  # Reset


    def onRotationSliderChanged(self, value):
        axis = None
        axisName = None

        if self.ui.axisX.isChecked():
            axis = [1, 0, 0]
            axisName = "x"
        elif self.ui.axisY.isChecked():
            axis = [0, 1, 0]
            axisName = "y"
        elif self.ui.axisZ.isChecked():
            axis = [0, 0, 1]
            axisName = "z"

        if axis:
            # Compute delta only for this axis
            delta = value - self.lastRotation[axisName]
            self.lastRotation[axisName] = value  # update stored value

            sliceNode = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeRed")
            self.angulate_slice(sliceNode, angleDegrees=delta, axis=axis)

        self.ui.rotationValueLabel.setText(f"{value}°")


    def onX(self):
        self.ui.axisY.setChecked(False)
        self.ui.axisZ.setChecked(False)
        self.currentAxis = "x"
        self.ui.rotationslider.setValue(self.lastRotation["x"])  # restore last slider value

    def onY(self):
        self.ui.axisX.setChecked(False)
        self.ui.axisZ.setChecked(False)
        self.currentAxis = "y"
        self.ui.rotationslider.setValue(self.lastRotation["y"])

    def onZ(self):
        self.ui.axisX.setChecked(False)
        self.ui.axisY.setChecked(False)
        self.currentAxis = "z"
        self.ui.rotationslider.setValue(self.lastRotation["z"])


    def onTranslationSliderChanged(self, value):
        if not self.currentTransAxis:
            return  # no axis selected → ignore slider

        axis = self.currentTransAxis
        sliceNode = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeRed")
        if not sliceNode:
            return

        delta = value - self.lastTranslation[axis]
        self.lastTranslation[axis] = value
        self.applyTranslation(sliceNode, delta, axis)

        self.ui.translationValueLabel.setText(f"{value} mm ({axis})")


    def applyTranslation(self, sliceNode, delta, axis):
        """
        Translate slice in RAS along the given axis.
        axis = "x", "y" or "z"
        """
        # Build translation transform
        transform = vtk.vtkTransform()
        if axis == "x":
            transform.Translate(delta, 0, 0)
        elif axis == "y":
            transform.Translate(0, delta, 0)
        elif axis == "z":
            transform.Translate(0, 0, delta)

        # Apply to SliceToRAS
        currentMatrix = sliceNode.GetSliceToRAS()
        translationMatrix = vtk.vtkMatrix4x4()
        transform.GetMatrix(translationMatrix)

        newMatrix = vtk.vtkMatrix4x4()
        vtk.vtkMatrix4x4.Multiply4x4(translationMatrix, currentMatrix, newMatrix)

        sliceNode.GetSliceToRAS().DeepCopy(newMatrix)
        sliceNode.UpdateMatrices()


    def ontranslonX(self, checked):
        if checked:
            # Uncheck others
            self.ui.translonY.blockSignals(True)
            self.ui.translonZ.blockSignals(True)
            self.ui.translonY.setChecked(False)
            self.ui.translonZ.setChecked(False)
            self.ui.translonY.blockSignals(False)
            self.ui.translonZ.blockSignals(False)

            self.currentTransAxis = "x"
            self.ui.translationslider.setValue(self.lastTranslation["x"])
        else:
            if self.currentTransAxis == "x":
                self.currentTransAxis = None


    def ontranslonY(self, checked):
        if checked:
            self.ui.translonX.blockSignals(True)
            self.ui.translonZ.blockSignals(True)
            self.ui.translonX.setChecked(False)
            self.ui.translonZ.setChecked(False)
            self.ui.translonX.blockSignals(False)
            self.ui.translonZ.blockSignals(False)

            self.currentTransAxis = "y"
            self.ui.translationslider.setValue(self.lastTranslation["y"])
        else:
            if self.currentTransAxis == "y":
                self.currentTransAxis = None


    def ontranslonZ(self, checked):
        if checked:
            self.ui.translonX.blockSignals(True)
            self.ui.translonY.blockSignals(True)
            self.ui.translonX.setChecked(False)
            self.ui.translonY.setChecked(False)
            self.ui.translonX.blockSignals(False)
            self.ui.translonY.blockSignals(False)

            self.currentTransAxis = "z"
            self.ui.translationslider.setValue(self.lastTranslation["z"])
        else:
            if self.currentTransAxis == "z":
                self.currentTransAxis = None


    def on_implantlocscomboBox_changed(self):

        slicer_base = slicer.app.slicerHome

        
        #slice_dir = slicer_base + 'red_slice/' + self.ui.patientnamelabel.text + '/'
        slice_dir = os.path.join(slicer_base, "red_slice", self.ui.patientnamelabel.text)

        filename = os.path.join(slice_dir, self.ui.implantlocscomboBox.currentText)

        if not os.path.isfile(filename):
            #print("Not a valid file:", filename)
            return

        with open(filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            csv_list = [line for line in reader]

        print(csv_list[1])  # position row
        print(csv_list[4])  # normal row

        position_coord = list(map(float, csv_list[1]))
        normal_coord = list(map(float, csv_list[4]))

 
        # --- helper function ---

        def setSlicePoseFromSliceNormalAndPosition(sliceNode, sliceNormal, slicePosition, defaultViewUpDirection=None, backupViewRightDirection=None):
            if defaultViewUpDirection is None:
                defaultViewUpDirection = [0,0,1]
            if backupViewRightDirection is None:
                backupViewRightDirection = [-1,0,0]

            # Ensure consistent normal orientation
            if sliceNormal[1] >= 0:
                sliceNormalStandardized = sliceNormal
            else:
                sliceNormalStandardized = [-sliceNormal[0], -sliceNormal[1], -sliceNormal[2]]

            # Compute slice axes
            sliceNormalViewUpAngle = vtk.vtkMath.AngleBetweenVectors(sliceNormalStandardized, defaultViewUpDirection)
            angleTooSmallThresholdRad = 0.25  # ~15 deg
            if angleTooSmallThresholdRad < sliceNormalViewUpAngle < vtk.vtkMath.Pi() - angleTooSmallThresholdRad:
                sliceAxisY = defaultViewUpDirection
                sliceAxisX = [0, 0, 0]
                vtk.vtkMath.Cross(sliceAxisY, sliceNormalStandardized, sliceAxisX)
            else:
                sliceAxisX = backupViewRightDirection

            # Apply to slice
            sliceNode.SetSliceToRASByNTP(sliceNormalStandardized[0], sliceNormalStandardized[1], sliceNormalStandardized[2],
                                         sliceAxisX[0], sliceAxisX[1], sliceAxisX[2],
                                         slicePosition[0], slicePosition[1], slicePosition[2], 0)

        # --- apply to red slice ---
        sliceNode = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeRed")
        setSlicePoseFromSliceNormalAndPosition(sliceNode, normal_coord, position_coord)

        #print("Red slice updated to implant location")

        
    def onmodeltreeButton(self):
        self.FilterTreeItems_4()          


    def FilterTreeItems_4(self):
        
        shNode = slicer.vtkMRMLSubjectHierarchyNode.GetSubjectHierarchyNode(slicer.mrmlScene)

        categoryName = "FilteredNodes_4"  # Unified category for both types

        # Assign category to relevant TRANSFORM nodes
        for modelNode in slicer.util.getNodesByClass("vtkMRMLModelNode"):
            name = modelNode.GetName().lower()
            if any(keyword in name for keyword in ["v", "guidebase", "maxilla", "mandible", "upper", "lower", "mandibular canal","model"]): 
                shItemID = shNode.GetItemByDataNode(modelNode)
                if shItemID:
                    shNode.SetItemAttribute(shItemID, "Category", categoryName)

        # Refresh the subject hierarchy tree filter
        tree = self.ui.ProsthTreeViewSubjectHierarchyTreeView
        tree.setMRMLScene(None)  # Temporarily detach to clear previous filters
        tree.addItemAttributeFilter("Category", categoryName)  # Apply updated filter
        tree.setContextMenuEnabled(True)
        tree.setMRMLScene(slicer.mrmlScene)  # Re-attach scene to refresh

    def removeHiddenFiducials(self):
        # Loop over all fiducial nodes in the scene
        allFiducials = slicer.util.getNodesByClass("vtkMRMLMarkupsFiducialNode")
        for fiducialNode in allFiducials:
            name = fiducialNode.GetName()
            # If the name matches your "hidden marker" pattern, remove it
            if name.startswith("_") or name.startswith("ProsthPoint_"):
                print(f"Removing hidden fiducial: {name}")
                slicer.mrmlScene.RemoveNode(fiducialNode)

    def onComboBoxChanged(self,newText):
        
        self._parameterNode.selectedOption = newText


    def onselectprosthpointButton(self):

        customLayout = """
        <layout type="horizontal" split="true">
            <!-- Left: 3D View -->
            <item>
                <view class="vtkMRMLViewNode" singletontag="1">
                    <property name="viewlabel" action="default">1</property>
                </view>
            </item>

            <!-- Right: Vertical stack of Red + Axial -->
            <item>
                <layout type="vertical" split="true">
                    <item>
                        <view class="vtkMRMLSliceNode" singletontag="Red">
                            <property name="orientation" action="default">Axial</property>
                            <property name="viewlabel" action="default">R</property>
                        </view>
                    </item>
                    <item>
                        <view class="vtkMRMLSliceNode" singletontag="Axial">
                            <property name="orientation" action="default">Axial</property>
                            <property name="viewlabel" action="default">A</property>
                        </view>
                    </item>
                </layout>
            </item>
        </layout>
        """
        # Register the custom layout
        layoutManager = slicer.app.layoutManager()
        customLayoutId = random.randint(502, 5000)
        layoutManager.layoutLogic().GetLayoutNode().AddLayoutDescription(customLayoutId, customLayout)

        # Switch to it
        layoutManager.setLayout(customLayoutId)

        # Optionally configure axial slice
        currentVolume = slicer.util.getNode('vtkMRMLScalarVolumeNode*')
        axialSliceWidget = layoutManager.sliceWidget("Axial")
        if axialSliceWidget and currentVolume:
            axialSliceLogic = axialSliceWidget.sliceLogic()
            axialSliceLogic.GetSliceCompositeNode().SetBackgroundVolumeID(currentVolume.GetID())
            axialSliceLogic.FitSliceToAll()

       # Enable placement mode for fiducials
        placeModePersistence = 0  # Allow multiple placements if needed
        slicer.modules.markups.logic().StartPlaceMode(placeModePersistence)


        # Display a message to the user
        slicer.util.delayDisplay(
            "In 4'' click the point where you want to place the virtual model!", 4000
        )

        self.removeHiddenFiducials()       


        # Wait for user to place at least one fiducial point
        
        fiducialNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsFiducialNode", "_")
        
        print(f"New fiducial node created: {fiducialNode.GetName()} (ID: {fiducialNode.GetID()})")

        # Wait for the user to place at least one point
        numControlPoints = fiducialNode.GetNumberOfControlPoints()
        while numControlPoints == 0:
            slicer.app.processEvents()  # Keep the UI responsive while waiting
            numControlPoints = fiducialNode.GetNumberOfControlPoints()

        # Get the position of the first control point
        ras_vector = vtk.vtkVector3d(0, 0, 0)
        fiducialNode.GetNthControlPointPosition(0, ras_vector)
        ras = [ras_vector.GetX(), ras_vector.GetY(), ras_vector.GetZ()]
        print("Fiducial Coordinates:", ras)
        
        fiducialNode.GetDisplayNode().SetVisibility(False)
        #slicer.mrmlScene.RemoveNode(fiducialNode)

        #Load a stl with tooth-name
        tooth_name=self.ui.prosthcomboBox.currentText
        slicer_base = slicer.app.slicerHome

        tooth_dir=self.resourcePath("teeth/")
        #tooth_dir=os.path.join(slicer_base, "teeth/")
        #tooth_dir=slicer_base + 'teeth' + '/'
        
        filename=tooth_dir+ tooth_name

        # Load with returnNode=True to get the node reference directly
        model_node = slicer.util.loadNodeFromFile(filename, filetype=None, properties={}, returnNode=False)
        
        # Get name and ID
      
        print("Node Name:", model_node.GetName())
        print("Node ID:", model_node.GetID())
        
        model_node = slicer.util.getNode(model_node.GetName())
       
        # Calculate the model's center
        model_polydata = model_node.GetPolyData()
        bounds = [0.0] * 6
        model_polydata.GetBounds(bounds)
        model_center = [
            (bounds[0] + bounds[1]) / 2,
            (bounds[2] + bounds[3]) / 2,
            (bounds[4] + bounds[5]) / 2,
        ]

        print("Model Center:", model_center)

        import numpy as np
        # Calculate the translation vector
        translation = np.subtract(ras, model_center)

        # Create a transform node to move the model
        transform_node = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLLinearTransformNode", "TranslationTransform")
        transform_matrix = vtk.vtkMatrix4x4()
        transform_matrix.Identity()
        for i in range(3):
            transform_matrix.SetElement(i, 3, translation[i])

        # Apply the transform to the model
        transform_node.SetMatrixTransformToParent(transform_matrix)
        model_node.SetAndObserveTransformNodeID(transform_node.GetID())


        # Log the transformation application
        print("Transform applied. Use the Transforms module to fine-tune the position.")
        

        # Add a display node if it does not exist
        TransformDisplayNode = transform_node.GetDisplayNode()
        if not TransformDisplayNode:
            TransformDisplayNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformDisplayNode")
            transform_node.SetAndObserveDisplayNodeID(TransformDisplayNode.GetID())

        # Configure the interaction handles
        TransformDisplayNode.SetEditorVisibility(True)

        displayNode = model_node.GetDisplayNode()
        if displayNode:
            displayNode.SetOpacity(0.7)
            displayNode.SetVisibility3D(True)
            displayNode.SetVisibility2D(True)       
        
 
        self.TransformDisplayNode = TransformDisplayNode
        self.FilterTreeItems_4()        

        return TransformDisplayNode



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


    def setParameterNode(self, inputParameterNode: Optional[VirtualProsthParameterNode]) -> None:
        if self._parameterNode:
            try:
                self._parameterNode.disconnectGui(self._parameterNodeGuiTag)
            except Exception:
                pass
            self._parameterNodeGuiTag = None

        self._parameterNode = inputParameterNode

        if self._parameterNode:
            guiWrapper = VirtualProsthGui(self.ui)
            self._parameterNodeGuiTag = self._parameterNode.connectGui(guiWrapper)

        
 #
# VirtualProsthLogic#


class VirtualProsthLogic(ScriptedLoadableModuleLogic):
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
        return VirtualProsthParameterNode(super().getParameterNode())

#
# VirtualProsthTest
#

class VirtualProsthTest(ScriptedLoadableModuleTest):
    pass
