import sys
import logging
import os
from typing import Annotated, Optional
import csv
import pyacvd
import pyvista as pv
import vtk
from vtk.util import numpy_support  
import time
import ctk
import qt
import slicer
from slicer import util
from slicer.i18n import tr as _
from slicer.i18n import translate
from slicer.ScriptedLoadableModule import *
from slicer.util import getNode
from slicer.util import VTKObservationMixin
from slicer.parameterNodeWrapper import (
    parameterNodeWrapper,
    WithinRange,
)
import datetime
from pydicom import dcmread
import importlib
import numpy as np
import random
import re
import ScreenCapture
from fpdf import FPDF
import math
import SegmentStatistics
#from unidecode import unidecode

class DentImplImaging(ScriptedLoadableModule):
    """Uses ScriptedLoadableModule base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = _("Dental Implant Imaging")  
        
        self.parent.categories = [translate("qSlicerAbstractCoreModule", "Examples")]
        self.parent.dependencies = []  
        self.parent.contributors = ["Dimitris Trikeriotis (Gnathion)"]  
        self.parent.helpText = _("""
To process CBCT data and prepare customized working layouts for the simulation of dental implant placement.
See more information in <a href="https://github.com/organization/projectname#DentImplImaging">module documentation</a>.
""")
        self.parent.acknowledgementText = _("""
This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc., Andras Lasso, PerkLab,
and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
""")
#
# DentImplImagingParameterNode

'''
The parameters needed by the module.
RegisteSubjectHierarchyTreeView was commented out
because of the error: "Unable to create serializer for {classtype} member {name}")
probably due to the fact that no GUI connector is yet available. Fix????
'''
#
@parameterNodeWrapper
class DentImplImagingParameterNode:    

    customsliceview: str = "None"
    implantlocscomboBox: str = "None"
    locationcomboBox: str = "None"
    dicomcomboBox:str = "None"
    segmentBox:str = "None"
    statList:str = "None"
    
    resampleSpinBox: Annotated[float, WithinRange(0.0, 500.0)] = 0.0
    Slider: Annotated[int, WithinRange(0, 32)] = 0
    rotationslider:  Annotated[int, WithinRange(-50, 50)]  = 0
    translationslider: Annotated[int, WithinRange(-50, 50)]  = 0
    axisX: bool = False
    axisY: bool = False
    axisZ: bool = False
    translonX: bool = False
    translonY: bool = False
    translonZ: bool = False
    
    addcurveComboBox: slicer.vtkMRMLMarkupsCurveNode = None
    selectcurvecomboBox: slicer.vtkMRMLMarkupsCurveNode = None
    volumeBox: slicer.vtkMRMLScalarVolumeNode = None
    segmentationBox: slicer.vtkMRMLSegmentationNode = None
    

    

    
    #CurveSubjectHierarchyTreeView_1Node:slicer.qMRMLSubjectHierarchyTreeView= None

'''
Because of the error:AttributeError: 'dict' object has no attribute '__dict__'
instead of passing a dictionary directly to connectGui()
an object/class (self.ui) is used, that contains all the named widgets.
'''    

class DentImplImagingGui:
    def __init__(self, ui):
        self.customsliceview = ui.customsliceview
        self.implantlocscomboBox = ui.implantlocscomboBox
        self.locationcomboBox = ui.locationcomboBox
        self.dicomcomboBox=ui.dicomcomboBox
        self.segmentBox = ui.segmentBox

        self.Slider = ui.Slider
        self.rotationslider = ui.rotationslider
        self.translationslider = ui.translationslider

        self.axisX = ui.axisX
        self.axisY = ui.axisY
        self.axisZ = ui.axisZ
        self.translonX = ui.translonX
        self.translonY = ui.translonY
        self.translonZ = ui.translonZ

        self.addcurveComboBox = ui.addcurveComboBox
        self.selectcurvecomboBox = ui.selectcurvecomboBox
        self.volumeBox = ui.volumeBox
        self.segmentationBox = ui.segmentationBox
        self.statList = ui.statList
        
        #self.CurveSubjectHierarchyTreeView_1Node = ui.CurveSubjectHierarchyTreeView


#


class DentImplImagingWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):


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
        uiWidget = slicer.util.loadUI(self.resourcePath("UI/DentImplImaging.ui"))
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
        self.logic = DentImplImagingLogic()

        # Connections

        # These connections ensure that we update parameter node when scene is closed
        self.addObserver(slicer.mrmlScene, slicer.mrmlScene.StartCloseEvent, self.onSceneStartClose)
        self.addObserver(slicer.mrmlScene, slicer.mrmlScene.EndCloseEvent, self.onSceneEndClose)

        # Buttons

        self.ui.getsegmButton.clicked.connect(self.onGetSegmentStats)
        self.ui.volumeBox.currentNodeChanged.connect(self.onVolumeChanged)
        self.ui.selectexamButton.connect('clicked(bool)', self.OnselectexamButton)
        self.ui.grbutton.connect('clicked(bool)', self.OnGreek)
        self.ui.engbutton.connect('clicked(bool)', self.OnEnglish)
        self.ui.homeButton.connect("clicked(bool)", self.onhomeButton)
        self.ui.widescreenButton.connect("clicked(bool)", self.onwidescreenButton)
        self.ui.custom1screenButton.connect("clicked(bool)", self.customlayout1)
        self.ui.redcreenButton.connect("clicked(bool)", self.onredcreenButton)
        self.ui.dscreenButton.connect("clicked(bool)", self.ondscreenButton)
        self.ui.modelcurvetreeButton.connect("clicked(bool)", self.onmodelcurvetreeButton) 
        self.ui.exportlocButton.connect("clicked(bool)", self.onredexport)
        self.ui.importlocButton.connect("clicked(bool)", self.onredreset)
        self.ui.AImodelsCreateButton.clicked.connect(self.AImodelsCreate)
        self.ui.dicomButton.connect('clicked(bool)', self.dicom_element_information)       
        self.ui.implreport.connect('clicked(bool)', self.createImplantReport)               
        self.ui.resampleSpinBox.valueChanged.connect(self.resamplecurve)
        self.retrievepatient()

        self.ui.addcurveComboBox.nodeAdded.connect(self.onnewcurvepoint)
        self.ui.selectcurvecomboBox.currentNodeChanged.connect(self.onCurveNodeChanged)
        self.ui.selectcurvecomboBox.noneEnabled = True
        self.FilterTreeItems_6()
                
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

        # Σύνδεση του signal όταν αλλάζει το segmentation node
        self.ui.segmentationBox.currentNodeChanged.connect(self.onSegmentationChanged)



        self.ui.implantlocscomboBox.currentTextChanged.connect(self.on_implantlocscomboBox_changed)          
        

        self.update_implocationlist()
        self.ui.customsliceview.currentTextChanged.connect(self.on_customsliceview_changed)
        self.ui.customlayoutButton.clicked.connect(self.createintraoplayout)
        
        self.ui.patientnamelabel.hide()
        

        self.greek()
        self.english()
        self.homeButton()
        self.widescreenButton()
        self.custom1screenButton()
        self.redcreenButton()
        self.dscreenButton()
        
        
        self.populate_locationList()
        self.findsDicomFolder()

        self.ui.registButton.connect("clicked(bool)", self.onregistButton)
        self.ui.virtprButton.connect("clicked(bool)", self.onvirtprButton)
        self.ui.genimplButton.connect("clicked(bool)", self.ongenimplButton)


        self.registButton()
        self.virtprButton()
        self.genimplButton()

        self.dataButton()
        self.ui.databutton.connect("clicked(bool)", self.ondataButton)

        
       
        # Make sure parameter node is initialized (needed for module reload)
        self.initializeParameterNode()



    def onVolumeChanged(self, volumeNode):
        if not volumeNode:
            self.ui.segmentationBox.setCurrentNode(None)
            return

        # Εμφάνισε το volume στις slice views
        slicer.util.setSliceViewerLayers(background=volumeNode)
        slicer.util.resetSliceViews()

        # Βρες segmentation nodes που έχουν reference το volume
        for segNode in slicer.util.getNodesByClass("vtkMRMLSegmentationNode"):
            refVolumeId = segNode.GetNodeReferenceID("referenceVolume")
            if refVolumeId == volumeNode.GetID():
                self.ui.segmentationBox.setCurrentNode(segNode)
                break





    def onSegmentationChanged(self, segmentationNode):
        # Καθάρισε το segmentBox
        self.ui.segmentBox.clear()

        if not segmentationNode:
            return

        segmentation = segmentationNode.GetSegmentation()
        for i in range(segmentation.GetNumberOfSegments()):
            segId = segmentation.GetNthSegmentID(i)
            segName = segmentation.GetNthSegment(i).GetName()
            # Προσθέτεις το όνομα στο combo box και κρατάς το ID σαν userData
            self.ui.segmentBox.addItem(segName, segId)







    def onGetSegmentStats(self):
        # Πάρε το επιλεγμένο segment ID από το combo box
        segId = self.ui.segmentBox.currentData
        if not segId:
            return

        # Υπολογισμός statistics
        segStatLogic = SegmentStatistics.SegmentStatisticsLogic()
        parameterNode = segStatLogic.getParameterNode()
        parameterNode.SetParameter("Segmentation", self.ui.segmentationBox.currentNode().GetID())
        segStatLogic.computeStatistics()
        stats = segStatLogic.getStatistics()

        # Καθάρισε τη λίστα πριν γεμίσεις
        self.ui.statList.clear()

        # Ασφαλής ανάγνωση με .get()
        volume_cm3 = stats.get((segId, "LabelmapSegmentStatisticsPlugin.volume_cm3"), None)
        volume_mm3 = stats.get((segId, "LabelmapSegmentStatisticsPlugin.volume_mm3"), None)
        obb_diameter = stats.get((segId, "LabelmapSegmentStatisticsPlugin.obb_diameter_mm"), None)

        # Καθαρισμός λίστας
        self.ui.statList.clear()

        if volume_mm3 is not None:
            self.ui.statList.addItem(f"Volume (mm³): {volume_mm3:.2f}")
        if volume_cm3 is not None:
            self.ui.statList.addItem(f"Volume (cm³): {volume_cm3:.3f}")
        if obb_diameter is not None:
            self.ui.statList.addItem(f"OBB diameter (mm): {obb_diameter}")
        else:
            self.ui.statList.addItem("OBB diameter not available for this segment")



    def dataButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "diOSData.png"))
        self.ui.databutton.setIcon(icon)           
    
    def ondataButton(self):
        slicer.util.selectModule("OralSurgData")
        slicer.util.reloadScriptedModule("OralSurgData")

    def onmodelcurvetreeButton(self):
        self.FilterTreeItems_6()  

    def registButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "diRegisterMod.png"))
        self.ui.registButton.setIcon(icon)

    def virtprButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "diVirtualPr.png"))
        self.ui.virtprButton.setIcon(icon)

    def genimplButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "diGenIImplCr.png"))
        self.ui.genimplButton.setIcon(icon)  

    def onregistButton(self):
        slicer.util.selectModule("RegisterModule")
        #slicer.util.reloadScriptedModule("RegisterModule")

    def onvirtprButton(self):
        slicer.util.selectModule("VirtualProsth")
        #slicer.util.reloadScriptedModule("VirtualProsth")

    def ongenimplButton(self):
        slicer.util.selectModule("GenericImplCreator")
        #slicer.util.reloadScriptedModule("GenericImplCreator")


    def widescreenButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "diws.png"))        
        self.ui.widescreenButton.setIcon(icon)


    def custom1screenButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "dics.png"))
        self.ui.custom1screenButton.setIcon(icon)


    def redcreenButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "dired.png"))
        self.ui.redcreenButton.setIcon(icon)

    def dscreenButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "di3d.png"))
        self.ui.dscreenButton.setIcon(icon)

    def homeButton(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "diOrSurgMod.png"))
        self.ui.homeButton.setIcon(icon)
        
    def onhomeButton(self):
        slicer.util.selectModule("OralSurgModuleHome")
        #slicer.util.reloadScriptedModule("OralSurgModuleHome")


    def onwidescreenButton(self):
        slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutConventionalWidescreenView)

    def onredcreenButton(self):
        slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUpRedSliceView)

    def ondscreenButton(self):
        slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUp3DView) 
    

    def greek(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "digr.png"))        
        self.ui.grbutton.setIcon(icon)


    def english(self):
        icon = qt.QIcon(os.path.join(self.resourcePath("Icons"), "dieng.png"))        
        self.ui.engbutton.setIcon(icon)


    def OnGreek(self):
    
        self.ui.CollapsibleButton_curve.setText("Επεξεργασία CBCT")
        self.ui.dicomCollapsibleButton.setText("DICOM")
        self.ui.exportCollapsibleButton.setText("Μετατροπή Dental Segmentator Segments σε Models")
        self.ui.curveCollapsibleButton.setText("Δημιουργία και Ρύθμιση Καμπυλών")
        self.ui.expimpCollapsibleButton.setText("Ρύθμιση και Εισαγωγή/Εξαγωγή Τομών")
        self.ui.selectedCollapsibleButton.setText("Προβολή/Εξαγωγή Επιλεγμένων Τομών σε png/pdf")
        self.ui.modelcurveCollapsibleButton.setText("Μοντέλα και Καμπύλες")
        self.ui.statCollapsibleButton.setText("Υπολογισμοί segments")
        self.ui.label_7.setText("Επιλογή Volume:")
        self.ui.label_5.setText("Επιλογή Κατάτμησης:")
        self.ui.label_6.setText("Επιλογή Segment:")
        self.ui.getsegmButton.setText("Υπολογισμός")
        self.ui.modelcurvetreeButton.setText("Ενημέρωση")        
        self.ui.dicomButton.setText("Δεδομένα DICOM")
        self.ui.AImodelsCreateButton.setText("Μετατροπή")
        self.ui.label_8.setText("Δημιουργία καμπύλης:")
        self.ui.label.setText("Επιλογή καμπύλης:")
        self.ui.label_10.setText("Επιλογή τομής")     
        self.ui.rotationValueLabel.setText("Περιστροφή τομής:")
        self.ui.translationValueLabel.setText("Μετατόπιση τομής:")
        self.ui.label_16.setText("Θέση Εμφυτεύματος/Βλάβης:")
        self.ui.label_4.setText("Απόσταση τομών:")
        self.ui.exportlocButton.setText("Εξαγωγή Τομής")
        self.ui.importlocButton.setText("Εισαγωγή Τομής")
        self.ui.label_2.setText("Συντεταγμένες Τομής:")
        self.ui.label_3.setText("Tομή κατά θέση:")        
        self.ui.customlayoutButton.setText("Layout με Επιλεγμένες Θέσεις")        
        self.ui.implreport.setText("Επιλεγμένες Θέσεις σε png /pdf")         
        self.ui.selectexamButton.setText("Επιλέξτε Εξέταση")



    def OnEnglish(self):

        self.ui.CollapsibleButton_curve.setText("CBCT processing")
        self.ui.dicomCollapsibleButton.setText("DICOM")
        self.ui.exportCollapsibleButton.setText("Export Dental Segmentator Segments to Models")
        self.ui.curveCollapsibleButton.setText("Create and Adjust Curves")
        self.ui.expimpCollapsibleButton.setText("Adjust and Export/Import Slices")
        self.ui.selectedCollapsibleButton.setText("Display and Export Selected Slices to png/pdf")
        self.ui.modelcurveCollapsibleButton.setText("Models and Curves")
        self.ui.statCollapsibleButton.setText("Segments Computations")        
        self.ui.dicomButton.setText("Dicom Metadata")
        self.ui.AImodelsCreateButton.setText("Export")
        self.ui.label_8.setText("Create curve:")
        self.ui.label_7.setText("Select Volume:")
        self.ui.label_5.setText("Select Segmantation:")
        self.ui.label_6.setText("Select Segment:")
        self.ui.getsegmButton.setText("Compute")
        self.ui.modelcurvetreeButton.setText("Update")        
        self.ui.label.setText("Select curve:")
        self.ui.label_10.setText("Select Slice:")
        self.ui.rotationValueLabel.setText("Rotate Slice:")
        self.ui.translationValueLabel.setText("Translate Slice:")
        self.ui.label_16.setText("Implant/Lesion Location:")
        self.ui.label_4.setText("Resample curve:")
        self.ui.exportlocButton.setText("Export Slice")
        self.ui.importlocButton.setText("Import Slice")
        self.ui.label_2.setText("Slice Coords:")
        self.ui.label_3.setText("Slice for Coords:")        
        self.ui.customlayoutButton.setText("Selected Slices Layout")
        self.ui.implreport.setText("Selected Slices png /pdf")       
        self.ui.selectexamButton.setText("Select Exam")


    def populate_locationList(self):
        
        location_list= ['None',
                        '18', '17', '16', '15', '14', '13','12','11',
                        '21', '22', '23', '24', '25','26','27','28',
                        '38', '37', '36', '35', '34', '33','32','31',
                        '41', '42', '43', '44', '45','46','47','48',
                        'L#1','L#2','L#3','L#4','L#5','L#6','L#7','L#8',
                        'L#9','L#10','L#11','L#12','L#13','L#14','L#15','L#16',
                        'L#17','L#18','L#19','L#20','L#21','L#22','L#23','L#24',
                        'L#25','L#26','L#27','L#28','L#29','L#30','L#31','L#32'
                        ]       
        #self.ui.locationcomboBox.clear() 
        for loc in location_list:
            self.ui.locationcomboBox.addItem(loc) 
        
        
    
    def findsDicomFolder(self):      

        
        path=os.path.join(os.environ['USERPROFILE'], 'Downloads')

        # Name filters
        name_filters = ["dicom", "dv"]

        self.ui.dicomcomboBox.clear()  # Clear previous entries
        

        for item in os.listdir(path):
            itemLower = item.lower()  # Case-insensitive
            # Check if name matches AND extension is allowed
            if any(tag in itemLower for tag in name_filters):
                #print("Adding:", item)
                self.ui.dicomcomboBox.addItem(item)
        self.ui.dicomcomboBox.addItem('None')
        self.ui.dicomcomboBox.setCurrentText(None)       

    def OnselectexamButton(self):
            self.findsDicomFolder()
            qt.QMessageBox.warning(
                    slicer.util.mainWindow(),
                    "Folder Selection",
                    "Παρακαλώ επιλέξτε έναν φάκελο από τη λίστα που να περιέχει στο όνομά του το'dicom' ή το 'dv'. (Please select a folder from the list that contains 'dicom' or 'dv' in its name.)"
                )
   
        
    def update_implocationlist(self):
        slicer_base = slicer.app.slicerHome
        
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
            

    def dicom_element_information(self): 

        # Ask for folder name (Qt dialog)
        folderName = self.ui.dicomcomboBox.currentText.strip()
        if not folderName or folderName == "None":
            qt.QMessageBox.warning(
                slicer.util.mainWindow(),
                "No Folder Selected",
                "Παρακαλώ επιλέξτε έναν φάκελο από τη λίστα που να περιέχει στο όνομά του το'dicom' ή το 'dv'. (Please select a folder from the list that contains 'dicom' or 'dv' in its name.)"
            )
            return

        #downloads_path = os.path.join(os.environ['USERPROFILE'], 'Downloads')
        dicom_dir = os.path.join(os.environ['USERPROFILE'], 'Downloads', folderName)
        

        img_list = os.listdir(dicom_dir)
        if not img_list:
            qt.QMessageBox.critical(slicer.util.mainWindow(), "Error", "Ο Φάκελος είναι άδειος! -Folder is empty!")
            return

        # Pick random DICOM file from folder
        img_num = random.randint(0, len(img_list) - 1)
        dicom_file_name = img_list[img_num]
        dicom_set = dcmread(os.path.join(dicom_dir, dicom_file_name))

        # --- Create popup dialog ---
        dialog = qt.QDialog(slicer.util.mainWindow())
        dialog.setWindowTitle(f"DICOM metadata ({dicom_file_name})")
        layout = qt.QVBoxLayout(dialog)

        # Create a table
        table = qt.QTableWidget(dialog)
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Tag", "Name", "Value"])
        layout.addWidget(table)

        # Populate table with DICOM elements
        elements = []
        for element in dicom_set:
            tag_str = f"({element.tag.group:04X},{element.tag.element:04X})"
            name = element.keyword if element.keyword else "Unknown"
            value = str(element.value)
            elements.append((tag_str, name, value))

        table.setRowCount(len(elements))
        for row, (tag, name, value) in enumerate(elements):
            table.setItem(row, 0, qt.QTableWidgetItem(tag))
            table.setItem(row, 1, qt.QTableWidgetItem(name))
            table.setItem(row, 2, qt.QTableWidgetItem(value))

        table.resizeColumnsToContents()
        table.resizeRowsToContents()

        def save_csv():
            slicer_base = slicer.app.slicerHome
            # Κεντρικός φάκελος
                       
            folder = os.path.join(slicer_base, "Dicoms")
            print(folder)

            if not os.path.exists(folder):
                os.makedirs(folder)
                print("Created root Dicoms folder:", folder)

            # Υποφάκελος ασθενή
            patientName = self.ui.patientnamelabel.text.strip()
            if not patientName:
                patientName = "UnknownPatient"      
                

            patient_folder = os.path.join(folder, patientName)
            if not os.path.exists(patient_folder):
                os.makedirs(patient_folder)
                print("Created patient folder:", patient_folder)
            else:
                print("Using existing patient folder:", patient_folder)

            # CSV filename (μπορείς να βάλεις και timestamp για πολλά αρχεία)
            filepath = os.path.join(patient_folder, patientName + ".csv")

            # Αν υπάρχει ήδη, ρώτα τον χρήστη
            if os.path.exists(filepath):
                reply = qt.QMessageBox.question(
                    slicer.util.mainWindow(),
                    "File Exists",
                    f"Το αρχείο (The file):\n{filepath}\nυπάρχει ήδη.\n\nΝα αντικατασταθεί (Do you want to overwrite it)?",
                    qt.QMessageBox.Yes | qt.QMessageBox.No
                )
                if reply == qt.QMessageBox.No:
                    return  # cancel if user does not want overwrite

            # Αποθήκευση σε CSV
            with open(filepath, "w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Tag", "Name", "Value"])  # header
                writer.writerows(elements)

            qt.QMessageBox.information(
                slicer.util.mainWindow(),
                "Saved",
                f"CSV saved to:\n{filepath}"
            )

        saveButton = qt.QPushButton("💾 Save to CSV")
        saveButton.clicked.connect(save_csv)
        layout.addWidget(saveButton)


        #Show dialog
        dialog.resize(800, 600)
        dialog.exec_()
        self.findsDicomFolder()
        
    




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



    def getOrCreateExportFolder(self, shNode, folderName="DentalSegmentator_Models"):
            """
            Returns the item ID of the export folder in SubjectHierarchy.
            Creates the folder only if it doesn't exist.
            """
            sceneItemID = shNode.GetSceneItemID()
            childIDs = vtk.vtkIdList()
            shNode.GetItemChildren(sceneItemID, childIDs)

            for i in range(childIDs.GetNumberOfIds()):
                childID = childIDs.GetId(i)
                if shNode.GetItemName(childID) == folderName:
                    print(f"Folder '{folderName}' already exists → reusing")
                    return childID  # reuse existing

            # If not found → create it
            folderItemId = shNode.CreateFolderItem(sceneItemID, folderName)
            #print(f"Created new folder: {folderName}")
            return folderItemId

        


    def AImodelsCreate(self):
            
            # Get the source segmentation node
            
           
            sourceSeg = slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLSegmentationNode")
            print(sourceSeg.GetName())

            sourceSeg.GetDisplayNode().SetVisibility(False)
            

            # List of segment names to copy
            segmentNames = ['Maxilla & Upper Skull', 'Mandible', 'Upper Teeth', 'Lower Teeth', 'Mandibular canal', 'Upper Mucosa', 'Lower Mucosa']

            # Create a new segmentation node to hold the selected segments
            destSeg = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLSegmentationNode', 'SelectedSegments')

            # Copy the selected segments to the new creegmentation
            for segmentName in segmentNames:
                segmentId = sourceSeg.GetSegmentation().GetSegmentIdBySegmentName(segmentName)
                if segmentId:
                    removeFromSource = False  # Set to True if you want to remove the segment from the source
                    destSeg.GetSegmentation().CopySegmentFromSegmentation(sourceSeg.GetSegmentation(), segmentId, removeFromSource)
                else:
                    print(f"Segment '{segmentName}' not found in the source segmentation.")

            # Export the selected segments to models
            shNode = slicer.mrmlScene.GetSubjectHierarchyNode()

            exportFolderItemId = self.getOrCreateExportFolder(shNode, "DentalSegmentator_Models")
            
            #exportFolderItemId = shNode.CreateFolderItem(shNode.GetSceneItemID(), "DentalSegmentator_Models")

            
            slicer.modules.segmentations.logic().ExportAllSegmentsToModels(destSeg, exportFolderItemId)

            node1=slicer.util.getNode('Maxilla & Upper Skull')
            modelDisplayNode = node1.GetDisplayNode()
            modelDisplayNode.SetColor(0.2,0.5,1)
            modelDisplayNode.SetOpacity(0.4)


            node2=slicer.util.getNode('Mandible')
            modelDisplayNode = node2.GetDisplayNode()
            modelDisplayNode.SetColor(0.2,0.5,1)
            modelDisplayNode.SetOpacity(0.4)

            node3=slicer.util.getNode('Upper Teeth')
            modelDisplayNode = node3.GetDisplayNode()
            modelDisplayNode.SetColor(0,1,0)      
            modelDisplayNode.SetOpacity(1.0)

            node4=slicer.util.getNode('Lower Teeth')
            modelDisplayNode = node4.GetDisplayNode()
            modelDisplayNode.SetColor(1,0,1)      
            modelDisplayNode.SetOpacity(1.0)

            node5=slicer.util.getNode('Mandibular canal')
            modelDisplayNode = node5.GetDisplayNode()
            modelDisplayNode.SetColor(1,1,0)
            modelDisplayNode.SetOpacity(1.0)

            node6=slicer.util.getNode('Upper Mucosa')
            modelDisplayNode = node6.GetDisplayNode()
            modelDisplayNode.SetColor(1,0.3,0)
            modelDisplayNode.SetOpacity(1.0)

            node7=slicer.util.getNode('Lower Mucosa')
            modelDisplayNode = node7.GetDisplayNode()
            modelDisplayNode.SetColor(1,0.3,0)
            modelDisplayNode.SetOpacity(1.0)

            print(f"Selected segments exported to models under folder 'DentalSegmentator_Models'!")
            self.FilterTreeItems_6()

            # Remove the temporary destination segmentation node
            slicer.mrmlScene.RemoveNode(destSeg)
            #print("Temporary segmentation node removed.")



    def FilterTreeItems_6(self):
        shNode = slicer.vtkMRMLSubjectHierarchyNode.GetSubjectHierarchyNode(slicer.mrmlScene)

        categoryName = "FilteredNodes_6"  # Unified category for both types

        # Assign category to relevant MODEL nodes
        for modelNode in slicer.util.getNodesByClass("vtkMRMLModelNode"):
            name = modelNode.GetName().lower()
            if any(keyword in name for keyword in ["maxilla", "mandible", "upper", "lower", "mandibular canal","upper mucosa", "lower mucosa"]): 
                shItemID = shNode.GetItemByDataNode(modelNode)
                if shItemID:
                    shNode.SetItemAttribute(shItemID, "Category", categoryName)

        # Assign category to relevant curve nodes
        for curveNode in slicer.util.getNodesByClass("vtkMRMLMarkupsCurveNode"):
            name = curveNode.GetName().lower()
            if any(keyword in name for keyword in ["c", "mark"]): 
                shItemID = shNode.GetItemByDataNode(curveNode)
                if shItemID:
                    shNode.SetItemAttribute(shItemID, "Category", categoryName)
                    

        # Refresh the subject hierarchy tree filter
        tree = self.ui.CurveSubjectHierarchyTreeView
        tree.setMRMLScene(None)  # Temporarily detach to clear previous filters
        tree.addItemAttributeFilter("Category", categoryName)  # Apply updated filter
        tree.setContextMenuEnabled(True)
        tree.setMRMLScene(slicer.mrmlScene)  # Re-attach scene to refresh









    def onnewcurvepoint(self):
            self.createSliceForCurveAdd()
            placeModePersistence = 1
            slicer.modules.markups.logic().StartPlaceMode(placeModePersistence) # Ensure 'Place multiple control points' is active
            

    def resamplecurve(self):
        self.curve = self.ui.addcurveComboBox.currentNode()
        spacemm = self.ui.resampleSpinBox.value  # με παρενθέσεις

        if self.curve and spacemm > 0:
            self.curve.ResampleCurveWorld(spacemm)



    def createSliceForCurveAdd(self):
            import random

            # Define custom layout XML with one Axial view
            layoutXML = """
                <layout>
                    <item>            
                        <view class="vtkMRMLSliceNode" singletontag="Axial">
                            <property name="orientation" action="default">Axial</property>
                            <property name="viewlabel" action="default">A</property>
                        </view>
                    </item>
                </layout>
            """

            # Access the layout manager
            layoutManager = slicer.app.layoutManager()

            # Generate a random custom layout ID
            customLayoutId = random.randint(7000, 8000)

            # Add the custom layout description to the layout node
            layoutManager.layoutLogic().GetLayoutNode().AddLayoutDescription(customLayoutId, layoutXML)

            # Apply the custom layout
            layoutManager.setLayout(customLayoutId)

            # Get the current volume
            currentVolume = slicer.util.getNode('vtkMRMLScalarVolumeNode*')
            if not currentVolume:
                slicer.util.errorDisplay("No volume loaded!")
                return

            # Access the Axial slice widget
            axialSliceWidget = layoutManager.sliceWidget("Axial")
            if axialSliceWidget:
                # Access the slice logic for the Axial slice
                axialSliceLogic = axialSliceWidget.sliceLogic()
                axialSliceNode = axialSliceWidget.mrmlSliceNode()

                # Set the background volume for the Axial slice
                axialSliceLogic.GetSliceCompositeNode().SetBackgroundVolumeID(currentVolume.GetID())

                # Automatically fit the slice view to 


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



    def onCurveNodeChanged(self):
        
        # Update the curve node
        self.curveNode = self.ui.selectcurvecomboBox.currentNode()

        if self.curveNode is None:
            self.ui.label_9.setText("Select curve!")
            self.ui.Slider.setEnabled(False)  # Disable slider if no curve
        else:
            self.ui.label_9.setText("Η καμπύλη ενημερώθηκε. - Curve updated.")
            self.ui.Slider.setEnabled(True)  # Enable slider for valid curve
            self.ui.Slider.setMinimum(0)
            self.ui.Slider.setMaximum(self.curveNode.GetNumberOfControlPoints() - 1)
            self.FilterTreeItems_6()

        

        if self.curveNode:
            # Disconnect previous slider signal
            try:
                self.ui.Slider.valueChanged.disconnect()
            except TypeError:
                pass  # No previous connection, safe to proceed

            # Update slider range
            self.ui.Slider.setMinimum(0)
            self.ui.Slider.setMaximum(self.curveNode.GetNumberOfControlPoints() - 1)
            numControlPoints=self.curveNode.GetNumberOfControlPoints()
            # Connect slider to update function
            self.ui.Slider.valueChanged.connect(self.onSliderValueChanged)

            # Optional: Reset the label or provide feedback
            #self.ui.label_9.setText("Η καμπύλη ενημερώθηκε:")
            self.ui.label_9.setText(f"Η καμπύλη ενημερώθηκε με(Curve updated with) {numControlPoints} σημεία(points).")
            
            
        else:
            self.ui.label_9.setText("Παρακαλώ επιλέξτε καμπύλη! -  Please, select a curve!")


    def align_slice_perpendicular_and_zoom(self, curveNode, sliceNode, pointIndex, fov=(50,50,1)):
        position = [0, 0, 0]
        curveNode.GetNthControlPointPosition(pointIndex, position)

        # Υπολογισμός εφαπτομένης
        if pointIndex == 0:
            nextPosition = [0, 0, 0]
            curveNode.GetNthControlPointPosition(pointIndex + 1, nextPosition)
            tangent = np.array(nextPosition) - np.array(position)
        elif pointIndex == curveNode.GetNumberOfControlPoints() - 1:
            prevPosition = [0, 0, 0]
            curveNode.GetNthControlPointPosition(pointIndex - 1, prevPosition)
            tangent = np.array(position) - np.array(prevPosition)
        else:
            nextPosition = [0, 0, 0]
            prevPosition = [0, 0, 0]
            curveNode.GetNthControlPointPosition(pointIndex + 1, nextPosition)
            curveNode.GetNthControlPointPosition(pointIndex - 1, prevPosition)
            tangent = np.array(nextPosition) - np.array(prevPosition)

        tangent /= np.linalg.norm(tangent)
        arbitraryVector = [0, 0, -1]
        normal = np.cross(tangent, arbitraryVector)
        normal /= np.linalg.norm(normal)
        binormal = np.cross(tangent, normal)

        rotationMatrix = np.eye(4)
        rotationMatrix[:3, 0] = normal
        rotationMatrix[:3, 1] = binormal
        rotationMatrix[:3, 2] = tangent
        rotationMatrix[:3, 3] = position

        vtkMatrix = slicer.util.vtkMatrixFromArray(rotationMatrix)
        sliceNode.GetSliceToRAS().DeepCopy(vtkMatrix)
        sliceNode.UpdateMatrices()

        # Ορισμός zoom (Field of View)
        sliceNode.SetFieldOfView(fov[0], fov[1], fov[2])

        # Κεντράρισμα στο σημείο
        sliceNode.JumpSlice(position[0], position[1], position[2])
        sliceNode.UpdateMatrices()
        

    def onSliderValueChanged(self, value):        
        self.customlayout1()
        pointIndex = int(value)
        self.align_slice_perpendicular_and_zoom(self.curveNode, self.redSliceNode, pointIndex, fov=(50,50,1))








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

  
            #path=slicer_base + 'red_slice' + '/' + self.ui.patientnamelabel.text
            path=os.path.join(slicer_base, "red_slice", self.ui.patientnamelabel.text)
            isExist = os.path.exists(path)
            if not isExist:
                os.makedirs(path)
                slicer.util.infoDisplay("Οι συντεταγμένες της τομής στο red slice αποθηκεύτηκαν(The red slice coordinates saved)!")
                #print("The new directory:", path, "is created!")
            else:
                slicer.util.infoDisplay("Οι συντεταγμένες της τομής στο red slice αποθηκεύτηκαν(The red slice coordinates saved)!")
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
        slice_dir=os.path.join(slicer_base, "red_slice", self.ui.patientnamelabel.text)
        

        coordinates_list = os.listdir(slice_dir)
       
        
        location2=self.ui.locationcomboBox.currentText

        filename=slice_dir +'/' +  location2 +'.csv'

        #'green_slice_plane_coordinates3.csv'
        with open(filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            csv_list=[]
            for line in reader:
                csv_list.append(line)
            

        position_coord= list(map(float, csv_list[1]))       
        normal_coord = list(map(float, csv_list[4]))
        

            
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

        slice_dir =os.path.join(slicer_base,"red_slice",self.ui.patientnamelabel.text)

        filename = os.path.join(slice_dir, self.ui.implantlocscomboBox.currentText)

        if not os.path.isfile(filename):            
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



    def createCustomLayout(self, number_of_slices):
        layoutManager = slicer.app.layoutManager()
        layoutLogic = layoutManager.layoutLogic()
        layoutNode = layoutLogic.GetLayoutNode()

        if not layoutNode:
            print("Error: Could not retrieve the layout node.")
            return

        customLayout = f"""
        <layout type="horizontal" split="true">
          <item>
            <view class="vtkMRMLViewNode" singletontag="1">
              <property name="viewlabel" action="default">1</property>
            </view>
          </item>
          <item>
            <layout type="grid">
              <item row="0" column="0" rowspan="1" colspan="1">
                <view class="vtkMRMLSliceNode" singletontag="Red">
                  <property name="orientation" action="default">Axial</property>
                  <property name="viewlabel" action="default">R</property>
                </view>
              </item>
        """

        total_cells = number_of_slices
        rows = int(total_cells ** 0.5)
        cols = rows if rows * rows >= total_cells else rows + 1

        for slice_idx in range(number_of_slices):
            cell_index = slice_idx + 1
            row = cell_index // cols
            col = cell_index % cols

            # Πάρε το όνομα από το comboBox (π.χ. "46.csv" → "46")
            tooth_label = os.path.splitext(self.ui.implantlocscomboBox.itemText(slice_idx))[0]

            sliceViewName = f"Custom{slice_idx+1}_{tooth_label}"
            customLayout += f"""
              <item row="{row}" column="{col}" rowspan="1" colspan="1">
                <view class="vtkMRMLSliceNode" singletontag="{sliceViewName}">
                  <property name="orientation" action="default">Axial</property>
                  <property name="viewlabel" action="default">{tooth_label}</property>
                </view>
              </item>
            """

        customLayout += """
            </layout>
          </item>
        </layout>
        """

        idnum = random.randint(502,10000)
        layoutNode.AddLayoutDescription(idnum, customLayout)
        layoutNode.SetViewArrangement(idnum)

        volumeNode = slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLScalarVolumeNode")
        if volumeNode:
            redComposite = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceCompositeNodeRed")
            if redComposite:
                redComposite.SetBackgroundVolumeID(volumeNode.GetID())
            redSlice = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeRed")
            if redSlice:
                bounds = [0]*6
                volumeNode.GetRASBounds(bounds)
                redSlice.SetSliceOffset((bounds[4]+bounds[5])/2)

            for sliceNode in slicer.util.getNodesByClass("vtkMRMLSliceNode"):
                if "Custom" in sliceNode.GetName() or sliceNode.GetName() == "Red":
                    sliceLogic = slicer.app.layoutManager().sliceWidget(sliceNode.GetName()).sliceLogic()
                    compNode = sliceLogic.GetSliceCompositeNode()
                    if compNode:
                        compNode.SetBackgroundVolumeID(volumeNode.GetID())
                    fov = (50,50,1)
                    sliceNode.SetFieldOfView(*fov)
                    sliceNode.UpdateMatrices()

            slicer.app.processEvents()




    def clearcustom(self):
        self.ui.customsliceview.clear()

        layoutManager = slicer.app.layoutManager()

        # Remove all custom slices and their composites
        nodes = slicer.util.getNodesByClass("vtkMRMLSliceNode")
        for node in nodes:
            if "Custom" in node.GetName():
                try:
                    # Get corresponding slice logic and composite node
                    sliceWidget = layoutManager.sliceWidget(node.GetName())
                    if sliceWidget:
                        compNode = sliceWidget.sliceLogic().GetSliceCompositeNode()
                        if compNode:
                            #print(f"Removing composite: {compNode.GetName()}")
                            slicer.mrmlScene.RemoveNode(compNode)

                    #print(f"Removing slice: {node.GetName()}")
                    slicer.mrmlScene.RemoveNode(node)

                except Exception as e:
                    print(f"Error while removing {node.GetName()}: {e}")

    def createintraoplayout(self):      
        self.clearcustom()

        # Number of slices = number of implant locations
        sliceno = self.ui.implantlocscomboBox.count
        #print("Implant locations in combobox:", sliceno)

        # Create the layout
        self.createCustomLayout(sliceno)

        # Debug: print what nodes exist after layout creation
        #print("After layout, slice nodes:")
        for node in slicer.util.getNodesByClass("vtkMRMLSliceNode"):
            print(" -", node.GetName())

        #print("After layout, composite nodes:")
        for node in slicer.util.getNodesByClass("vtkMRMLSliceCompositeNode"):
            print(" -", node.GetName())

        # Fill combobox with the new slice names
        nodes = slicer.util.getNodesByClass("vtkMRMLSliceNode")
        for node in nodes:
            if "Custom" in node.GetName():
                self.ui.customsliceview.addItem(node.GetName())

         
    def on_customsliceview_changed(self):
        # Access Red and Green slice nodes and logic
        red_slice_logic = slicer.app.layoutManager().sliceWidget('Red').sliceLogic()
        red_slice_node = red_slice_logic.GetSliceNode()
        custom_slice=slicer.util.getNode(self.ui.customsliceview.currentText)

        # Retrieve the Red slice's SliceToRAS matrix
        red_matrix = red_slice_node.GetSliceToRAS()

        custom_matrix = custom_slice.GetSliceToRAS()
        custom_matrix.DeepCopy(red_matrix)
        # Update the Green slice's matrix and offset
        custom_slice.UpdateMatrices()


    def smartGrid(self, total_images):
        """
        Επιστρέφει (cols, rows) ανάλογα με τον αριθμό εικόνων.
        """
        if total_images <= 1:
            return (1, 1)
        elif total_images <= 2:
            return (2, 1)
        elif total_images <= 4:
            return (2, 2)
        elif total_images <= 6:
            return (3, 2)
        elif total_images <= 9:
            return (3, 3)
        elif total_images <= 12:
            return (4, 3)
        elif total_images <= 16:
            return (4, 4)
        else:
            # Για πολλά slices, default σε 5x5
            return (5, 5)



    class CustomPDF2(FPDF):
        def __init__(self, caseName, logoPath):
            super().__init__()
            self.caseName = caseName
            self.logoPath = logoPath

        def header(self):
            # Logo
            if self.logoPath:
                self.image(self.logoPath, 10, 8, 30)
            # Title
            self.set_font("Arial", "B", 14)
            self.cell(0, 10, f"CBCT Selected Slices - {self.caseName}", ln=1, align="C")
            self.ln(5)

        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", "I", 8)
            self.cell(0, 10, f"Page {self.page_no()}", align="C")



    def createImplantReport(self):
        caseName = self.ui.patientnamelabel.text.strip()
        slicer_base = slicer.app.slicerHome

        # --- 1. Custom layout ---
        sliceno = self.ui.implantlocscomboBox.count
        self.createCustomLayout(sliceno)

        # --- 2. Field of View ---
        fov = (50, 50, 1)
        for sliceNode in slicer.util.getNodesByClass("vtkMRMLSliceNode"):
            if "Custom" in sliceNode.GetName() or sliceNode.GetName() == "Red":
                sliceNode.SetFieldOfView(*fov)
                sliceNode.UpdateMatrices()

        # --- 3. Export PNGs ---
        png_base = os.path.join(slicer_base, "pngs")
        patientFolder = os.path.join(png_base, caseName.replace(" ", "_"))
        dateFolder = datetime.date.today().isoformat()
        outputDir = os.path.join(patientFolder, dateFolder)
        os.makedirs(outputDir, exist_ok=True)

        # Καθάρισε παλιές PNGs
        for f in os.listdir(outputDir):
            if f.endswith(".png"):
                os.remove(os.path.join(outputDir, f))

        layoutManager = slicer.app.layoutManager()
        screenCaptureLogic = ScreenCapture.ScreenCaptureLogic()

        exported_images = []
        labels = []

        for i, sliceNode in enumerate(slicer.util.getNodesByClass("vtkMRMLSliceNode")):
            if "Custom" in sliceNode.GetName() or sliceNode.GetName() == "Red":
                sliceWidget = layoutManager.sliceWidget(sliceNode.GetName())
                if sliceWidget:
                    view = sliceWidget.sliceView()
                    filename = os.path.join(outputDir, f"{i:03d}_{sliceNode.GetName()}.png")
                    screenCaptureLogic.captureImageFromView(view, filename)
                    exported_images.append(filename)

                    # Label από το viewlabel (που είναι το tooth number)
                    labels.append(f"Location #{sliceNode.GetLayoutLabel()}")
                    print(f"Saved {filename} with label {labels[-1]}")

        # --- 4. PDF ---
        pdf_base = os.path.join(slicer_base, "pdfs")
        patientPDFfolder = os.path.join(pdf_base, caseName.replace(" ", "_"), dateFolder)
        os.makedirs(patientPDFfolder, exist_ok=True)
        outputPDF = os.path.join(patientPDFfolder, f"{caseName}_SelectedScans.pdf")

        logoPath = os.path.join(self.resourcePath("Icons"), "dispot.png")
        pdf = self.CustomPDF2(caseName, logoPath)
        pdf.set_auto_page_break(auto=True, margin=10)

        total_images = len(exported_images)
        if total_images == 0:
            print("No PNG images found, skipping PDF creation.")
            return

        cols, rows = self.smartGrid(total_images)

        page_width = 210
        page_height = 297
        margin_x = 15
        margin_y = 50

        cell_width = (page_width - margin_x*2) / cols
        cell_height = (page_height - margin_y*2) / rows

        for i, img in enumerate(exported_images):
            if i % (cols * rows) == 0:
                pdf.add_page()
                # Υπολογισμός range δοντιών για αυτή τη σελίδα
                start_idx = i
                end_idx = min(i + cols*rows, total_images)
                tooth_range = ", ".join(labels[start_idx:end_idx])
                pdf.set_font("Arial", "I", 8)
                pdf.set_y(-25)
                pdf.cell(0, 10, align="C")

            col = i % cols
            row = (i // cols) % rows
            x = margin_x + col * cell_width
            y = margin_y + row * cell_height
            pdf.image(img, x=x, y=y, w=cell_width-5, h=cell_height-10)

            pdf.set_font("Arial", "", 8)
            pdf.text(x, y + cell_height - 2, labels[i])

        pdf.output(outputPDF)
        print(f"PDF saved as {outputPDF}")




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

            
    def setParameterNode(self, inputParameterNode: Optional[DentImplImagingParameterNode]) -> None:
        if self._parameterNode:
            try:
                self._parameterNode.disconnectGui(self._parameterNodeGuiTag)
            except Exception:
                pass
            self._parameterNodeGuiTag = None

        self._parameterNode = inputParameterNode

        if self._parameterNode:
            guiWrapper = DentImplImagingGui(self.ui)
            self._parameterNodeGuiTag = self._parameterNode.connectGui(guiWrapper)


#
# DentImplImagingLogic
#


class DentImplImagingLogic(ScriptedLoadableModuleLogic):
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
        return DentImplImagingParameterNode(super().getParameterNode())


# DentImplImagingTest
#

class DentImplImagingTest(ScriptedLoadableModuleTest):
    pass
    
 
