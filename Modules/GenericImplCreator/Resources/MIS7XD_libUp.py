import qt
import vtk
import slicer


def create_generic_implant_MIS7XD(ui, helper):

            
    pointListNode = ui.pointListComboBox.currentNode() 
    preimpl=slicer.util.getNode(ui.locationcomboBox.currentText)
    preimpl.GetDisplayNode().SetVisibility(False)
    
    #ui.selectimplantcomboBox.clear()
    selected_jaw=ui.selectjawcomboBox.currentText
    selected_implant_system=ui.selectimplantsystemcomboBox.currentText
    selected_implant=ui.selectimplantcomboBox.currentText


    # Safety checks
    if 'None' in [selected_jaw, selected_implant_system, selected_implant]:
        print("Select all options before generating implant.")
        return
    
    
    elif selected_jaw == 'Upper' and selected_implant_system=='MIS_7 Implant System' and selected_implant== '3.3/10':
                    
        angle, model = helper.createCenteredSolidTaperedTube(D1=3.3, D2=2.4, length=10.0)
        ringmodel,outerBottom, outerTop,innerBottom   = helper.createHollowTaperedTube(OD1=8.4, OD2=8.4, ID1=4.7, ID2=4.7, height=4, pointListNode=pointListNode)
        radius, height, resolution, model = helper.createimplantaxis(radius=0.5, height=50.0, resolution=60)
        radius, height, resolution, model = helper.createimplantcylinder(radius=1.65, height=10.0, resolution=60, pointListNode=pointListNode)

        node=slicer.util.getNode('CenteredCappedTaperedTube')
        node.SetName('3.3/10_UpperImpl')
        node2=slicer.util.getNode('HollowTaperedTube')
        node2.SetName('3.3/10_UpperGuideRing')
        node3=slicer.util.getNode('Implant Axis')
        node3.SetName('3.3/10_UpperImplAxis')
        node4=slicer.util.getNode('Implant Cylinder')
        node4.SetName('3.3/10_UpperImplCylinder') 
        
        transformNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode= slicer.util.getNode('3.3/10_UpperImpl')
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID()) 
        transformableNode2= slicer.util.getNode('3.3/10_UpperImplAxis')
        transformableNode2.SetAndObserveTransformNodeID(transformNode.GetID())            
        transformNode2 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode3= slicer.util.getNode('3.3/10_UpperGuideRing')
        transformableNode3.SetAndObserveTransformNodeID(transformNode2.GetID())            
        transformNode3 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode4= slicer.util.getNode('3.3/10_UpperImplCylinder')
        transformableNode4.SetAndObserveTransformNodeID(transformNode3.GetID())
        transformNode4 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode2.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode3.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())
        
        sourceModel = slicer.util.getNode('3.3/10_UpperImplCylinder')
        for modelNode in slicer.util.getNodesByClass("vtkMRMLModelNode"):
            name = modelNode.GetName()
            if name == ui.locationcomboBox.currentText:
                targetModel=modelNode             
        sourceToTargetTransform = slicer.util.getNode(transformNode4.GetName())
        
        import ModelRegistration
        mrLogic = ModelRegistration.ModelRegistrationLogic()
        mrLogic.run(sourceModel, targetModel, sourceToTargetTransform)
        mrLogic.ComputeMeanDistance(sourceModel, targetModel, sourceToTargetTransform)          

      
        node=slicer.util.getNode('3.3/10_UpperImpl')
        node.SetName((ui.locationcomboBox.currentText)+':'+ '3.3/10_Implant')             
        node2=slicer.util.getNode('3.3/10_UpperGuideRing')
        node2.SetName((ui.locationcomboBox.currentText)+':'+ '3.3/10_GuideRing') 
        node3=slicer.util.getNode('3.3/10_UpperImplAxis')
        node3.SetName((ui.locationcomboBox.currentText)+':'+'3.3/10_ImplAxis')             
        node5=slicer.util.getNode(transformNode4.GetName())
        node5.SetName((ui.locationcomboBox.currentText)+':'+'3.3/10_UnitTransformInteraction')
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())            
        node6=slicer.util.getNode(transformNodeF.GetName())
        node6.SetName((ui.locationcomboBox.currentText)+':'+'3.3/10_TransformUnit')


        ringModelNode = slicer.util.getNode((ui.locationcomboBox.currentText)+':'+ '3.3/10_GuideRing')        
        transformNodeID = ringModelNode.GetTransformNodeID()        
        transformNode = slicer.mrmlScene.GetNodeByID(transformNodeID)        
        transformNode.SetName((ui.locationcomboBox.currentText)+':'+"RingTransform")        
        transformableNode = ringModelNode       
        if not transformNode or not transformableNode:
            slicer.util.errorDisplay("Transform node or transformable node not found!")
            return
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID())        
        transformMatrix = vtk.vtkMatrix4x4()
        transformNode.GetMatrixTransformToParent(transformMatrix)
        transformMatrix.SetElement(2, 3,-13)
        transformNode.SetMatrixTransformToParent(transformMatrix)


        helper.FilterTreeItems()
    
        

        
    elif selected_jaw == 'Upper' and selected_implant_system=='MIS_7 Implant System' and selected_implant== '3.3/11.5':
        angle, model = helper.createCenteredSolidTaperedTube(D1=3.3, D2=2.4, length=11.5)
        ringmodel,outerBottom, outerTop,innerBottom   = helper.createHollowTaperedTube(OD1=8.4, OD2=8.4, ID1=4.7, ID2=4.7, height=4, pointListNode=pointListNode)
        radius, height, resolution, model = helper.createimplantaxis(radius=0.5, height=50.0, resolution=60)
        radius, height, resolution, model = helper.createimplantcylinder(radius=1.65, height=11.5, resolution=60, pointListNode=pointListNode)     

        node=slicer.util.getNode('CenteredCappedTaperedTube')
        node.SetName('3.3/11.5_UpperImpl')
        node2=slicer.util.getNode('HollowTaperedTube')
        node2.SetName('3.3/11.5_UpperGuideRing')
        node3=slicer.util.getNode('Implant Axis')
        node3.SetName('3.3/11.5_UpperImplAxis')
        node4=slicer.util.getNode('Implant Cylinder')
        node4.SetName('3.3/11.5_UpperImplCylinder')  
        
        transformNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode= slicer.util.getNode('3.3/11.5_UpperImpl')
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID()) 
        transformableNode2= slicer.util.getNode('3.3/11.5_UpperImplAxis')
        transformableNode2.SetAndObserveTransformNodeID(transformNode.GetID())            
        transformNode2 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode3= slicer.util.getNode('3.3/11.5_UpperGuideRing')
        transformableNode3.SetAndObserveTransformNodeID(transformNode2.GetID())            
        transformNode3 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode4= slicer.util.getNode('3.3/11.5_UpperImplCylinder')
        transformableNode4.SetAndObserveTransformNodeID(transformNode3.GetID())
        transformNode4 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode2.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode3.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())
        
        sourceModel = slicer.util.getNode('3.3/11.5_UpperImplCylinder')
            
        for modelNode in slicer.util.getNodesByClass("vtkMRMLModelNode"):
            name = modelNode.GetName()
            if name == ui.locationcomboBox.currentText:
                targetModel=modelNode 
        sourceToTargetTransform = slicer.util.getNode(transformNode4.GetName())
        
        import ModelRegistration
        mrLogic = ModelRegistration.ModelRegistrationLogic()
        mrLogic.run(sourceModel, targetModel, sourceToTargetTransform)
        mrLogic.ComputeMeanDistance(sourceModel, targetModel, sourceToTargetTransform)          

      
        node=slicer.util.getNode('3.3/11.5_UpperImpl')
        node.SetName((ui.locationcomboBox.currentText)+':'+ '3.3/11.5_Implant')            
        node2=slicer.util.getNode('3.3/11.5_UpperGuideRing')
        node2.SetName((ui.locationcomboBox.currentText)+':'+ '3.3/11.5_GuideRing')
        node3=slicer.util.getNode('3.3/11.5_UpperImplAxis')
        node3.SetName((ui.locationcomboBox.currentText)+':'+'3.3/11.5_ImplAxis')              
        node5=slicer.util.getNode(transformNode4.GetName())
        node5.SetName((ui.locationcomboBox.currentText)+':'+'3.3/11.5_UnitTransformInteraction') 
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())            
        node6=slicer.util.getNode(transformNodeF.GetName())
        node6.SetName((ui.locationcomboBox.currentText)+':'+'3.3/11.5_TransformUnit')


        ringModelNode = slicer.util.getNode((ui.locationcomboBox.currentText)+':'+ '3.3/11.5_GuideRing')        
        transformNodeID = ringModelNode.GetTransformNodeID()        
        transformNode = slicer.mrmlScene.GetNodeByID(transformNodeID)        
        transformNode.SetName((ui.locationcomboBox.currentText)+':'+"RingTransform")        
        transformableNode = ringModelNode       
        if not transformNode or not transformableNode:
            slicer.util.errorDisplay("Transform node or transformable node not found!")
            return
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID())        
        transformMatrix = vtk.vtkMatrix4x4()
        transformNode.GetMatrixTransformToParent(transformMatrix)
        transformMatrix.SetElement(2, 3,-13.75)
        transformNode.SetMatrixTransformToParent(transformMatrix)

        
        helper.FilterTreeItems()

    elif selected_jaw == 'Upper' and selected_implant_system=='MIS_7 Implant System' and selected_implant== '3.3/13':
        angle, model = helper.createCenteredSolidTaperedTube(D1=3.3, D2=2.4, length=13.0)
        ringmodel,outerBottom, outerTop,innerBottom   = helper.createHollowTaperedTube(OD1=8.4, OD2=8.4, ID1=4.7, ID2=4.7, height=4, pointListNode=pointListNode)
        radius, height, resolution, model = helper.createimplantaxis(radius=0.5, height=50.0, resolution=60)
        radius, height, resolution, model = helper.createimplantcylinder(radius=1.65, height=13.0, resolution=60, pointListNode=pointListNode)
        
        node=slicer.util.getNode('CenteredCappedTaperedTube')
        node.SetName('3.3/13_UpperImpl')
        node2=slicer.util.getNode('HollowTaperedTube')
        node2.SetName('3.3/13_UpperGuideRing')
        node3=slicer.util.getNode('Implant Axis')
        node3.SetName('3.3/13_UpperImplAxis')
        node4=slicer.util.getNode('Implant Cylinder')
        node4.SetName('3.3/13_UpperImplCylinder') 
        
        transformNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode= slicer.util.getNode('3.3/13_UpperImpl')
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID()) 
        transformableNode2= slicer.util.getNode('3.3/13_UpperImplAxis')
        transformableNode2.SetAndObserveTransformNodeID(transformNode.GetID())            
        transformNode2 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode3= slicer.util.getNode('3.3/13_UpperGuideRing')
        transformableNode3.SetAndObserveTransformNodeID(transformNode2.GetID())            
        transformNode3 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode4= slicer.util.getNode('3.3/13_UpperImplCylinder')
        transformableNode4.SetAndObserveTransformNodeID(transformNode3.GetID())
        transformNode4 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode2.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode3.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())
        
        sourceModel = slicer.util.getNode('3.3/13_UpperImplCylinder')
        for modelNode in slicer.util.getNodesByClass("vtkMRMLModelNode"):
            name = modelNode.GetName()
            if name == ui.locationcomboBox.currentText:
                targetModel=modelNode  
        sourceToTargetTransform = slicer.util.getNode(transformNode4.GetName())
        
        import ModelRegistration
        mrLogic = ModelRegistration.ModelRegistrationLogic()
        mrLogic.run(sourceModel, targetModel, sourceToTargetTransform)
        mrLogic.ComputeMeanDistance(sourceModel, targetModel, sourceToTargetTransform)
        node=slicer.util.getNode('3.3/13_UpperImpl')
        node.SetName((ui.locationcomboBox.currentText)+':'+ '3.3/13_Implant')            
        node2=slicer.util.getNode('3.3/13_UpperGuideRing')
        node2.SetName((ui.locationcomboBox.currentText)+':'+ '3.3/13_GuideRing')            
        node3=slicer.util.getNode('3.3/13_UpperImplAxis')
        node3.SetName((ui.locationcomboBox.currentText)+':'+'3.3/13_ImplAxis')            
        node5=slicer.util.getNode(transformNode4.GetName())
        node5.SetName((ui.locationcomboBox.currentText)+':'+'3.3/13_UnitTransformInteraction')            
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())
        node6=slicer.util.getNode(transformNodeF.GetName())
        node6.SetName((ui.locationcomboBox.currentText)+':'+'3.3/13_TransformUnit')


        ringModelNode = slicer.util.getNode((ui.locationcomboBox.currentText)+':'+ '3.3/13_GuideRing')        
        transformNodeID = ringModelNode.GetTransformNodeID()        
        transformNode = slicer.mrmlScene.GetNodeByID(transformNodeID)        
        transformNode.SetName((ui.locationcomboBox.currentText)+':'+"RingTransform")        
        transformableNode = ringModelNode       
        if not transformNode or not transformableNode:
            slicer.util.errorDisplay("Transform node or transformable node not found!")
            return
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID())        
        transformMatrix = vtk.vtkMatrix4x4()
        transformNode.GetMatrixTransformToParent(transformMatrix)
        transformMatrix.SetElement(2, 3,-14.5)
        transformNode.SetMatrixTransformToParent(transformMatrix) 
         
        helper.FilterTreeItems()

    elif selected_jaw == 'Upper' and selected_implant_system=='MIS_7 Implant System' and selected_implant== '3.3/16':
        angle, model = helper.createCenteredSolidTaperedTube(D1=3.3, D2=2.4, length=16.0)
        ringmodel,outerBottom, outerTop,innerBottom   = helper.createHollowTaperedTube(OD1=8.4, OD2=8.4, ID1=4.7, ID2=4.7, height=4, pointListNode=pointListNode)
        radius, height, resolution, model = helper.createimplantaxis(radius=0.5, height=50.0, resolution=60)
        radius, height, resolution, model = helper.createimplantcylinder(radius=1.65, height=16.0, resolution=60, pointListNode=pointListNode)
        
        node=slicer.util.getNode('CenteredCappedTaperedTube')
        node.SetName('3.3/16_UpperImpl')
        node2=slicer.util.getNode('HollowTaperedTube')
        node2.SetName('3.3/16_UpperGuideRing')
        node3=slicer.util.getNode('Implant Axis')
        node3.SetName('3.3/16_UpperImplAxis')
        node4=slicer.util.getNode('Implant Cylinder')
        node4.SetName('3.3/16_UpperImplCylinder') 
        
        transformNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode= slicer.util.getNode('3.3/16_UpperImpl')
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID()) 
        transformableNode2= slicer.util.getNode('3.3/16_UpperImplAxis')
        transformableNode2.SetAndObserveTransformNodeID(transformNode.GetID())            
        transformNode2 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode3= slicer.util.getNode('3.3/16_UpperGuideRing')
        transformableNode3.SetAndObserveTransformNodeID(transformNode2.GetID())            
        transformNode3 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode4= slicer.util.getNode('3.3/16_UpperImplCylinder')
        transformableNode4.SetAndObserveTransformNodeID(transformNode3.GetID())
        transformNode4 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode2.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode3.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())
        
        sourceModel = slicer.util.getNode('3.3/16_UpperImplCylinder')
        for modelNode in slicer.util.getNodesByClass("vtkMRMLModelNode"):
            name = modelNode.GetName()
            if name == ui.locationcomboBox.currentText:
                targetModel=modelNode  
        sourceToTargetTransform = slicer.util.getNode(transformNode4.GetName())
        
        import ModelRegistration
        mrLogic = ModelRegistration.ModelRegistrationLogic()
        mrLogic.run(sourceModel, targetModel, sourceToTargetTransform)
        mrLogic.ComputeMeanDistance(sourceModel, targetModel, sourceToTargetTransform)
        node=slicer.util.getNode('3.3/16_UpperImpl')
        node.SetName((ui.locationcomboBox.currentText)+':'+ '3.3/16_Implant')            
        node2=slicer.util.getNode('3.3/16_UpperGuideRing')
        node2.SetName((ui.locationcomboBox.currentText)+':'+ '3.3/16_GuideRing')            
        node3=slicer.util.getNode('3.3/16_UpperImplAxis')
        node3.SetName((ui.locationcomboBox.currentText)+':'+'3.3/16_ImplAxis')            
        node5=slicer.util.getNode(transformNode4.GetName())
        node5.SetName((ui.locationcomboBox.currentText)+':'+'3.3/16_UnitTransformInteraction')            
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())
        node6=slicer.util.getNode(transformNodeF.GetName())
        node6.SetName((ui.locationcomboBox.currentText)+':'+'3.3/16_TransformUnit')

        ringModelNode = slicer.util.getNode((ui.locationcomboBox.currentText)+':'+ '3.3/16_GuideRing')        
        transformNodeID = ringModelNode.GetTransformNodeID()        
        transformNode = slicer.mrmlScene.GetNodeByID(transformNodeID)        
        transformNode.SetName((ui.locationcomboBox.currentText)+':'+"RingTransform")        
        transformableNode = ringModelNode       
        if not transformNode or not transformableNode:
            slicer.util.errorDisplay("Transform node or transformable node not found!")
            return
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID())        
        transformMatrix = vtk.vtkMatrix4x4()
        transformNode.GetMatrixTransformToParent(transformMatrix)
        transformMatrix.SetElement(2, 3,-16)
        transformNode.SetMatrixTransformToParent(transformMatrix)
         
        helper.FilterTreeItems()            


    elif selected_jaw == 'Upper' and selected_implant_system=='MIS_7 Implant System' and selected_implant== '3.75/8':
        angle, model = helper.createCenteredSolidTaperedTube(D1=3.75, D2=3.1, length=8.0)
        ringmodel,outerBottom, outerTop,innerBottom   = helper.createHollowTaperedTube(OD1=8.4, OD2=8.4, ID1=4.7, ID2=4.7, height=4, pointListNode=pointListNode)
        radius, height, resolution, model = helper.createimplantaxis(radius=0.5, height=50.0, resolution=60)
        radius, height, resolution, model = helper.createimplantcylinder(radius=1.875, height=8.0, resolution=60, pointListNode=pointListNode)
        
        node=slicer.util.getNode('CenteredCappedTaperedTube')
        node.SetName('3.75/8_UpperImpl')
        node2=slicer.util.getNode('HollowTaperedTube')
        node2.SetName('3.75/8_UpperGuideRing')
        node3=slicer.util.getNode('Implant Axis')
        node3.SetName('3.75/8_UpperImplAxis')
        node4=slicer.util.getNode('Implant Cylinder')
        node4.SetName('3.75/8_UpperImplCylinder') 
        
        transformNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode= slicer.util.getNode('3.75/8_UpperImpl')
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID()) 
        transformableNode2= slicer.util.getNode('3.75/8_UpperImplAxis')
        transformableNode2.SetAndObserveTransformNodeID(transformNode.GetID())            
        transformNode2 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode3= slicer.util.getNode('3.75/8_UpperGuideRing')
        transformableNode3.SetAndObserveTransformNodeID(transformNode2.GetID())            
        transformNode3 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode4= slicer.util.getNode('3.75/8_UpperImplCylinder')
        transformableNode4.SetAndObserveTransformNodeID(transformNode3.GetID())
        transformNode4 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode2.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode3.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())
        
        sourceModel = slicer.util.getNode('3.75/8_UpperImplCylinder')
        for modelNode in slicer.util.getNodesByClass("vtkMRMLModelNode"):
            name = modelNode.GetName()
            if name == ui.locationcomboBox.currentText:
                targetModel=modelNode  
        sourceToTargetTransform = slicer.util.getNode(transformNode4.GetName())
        
        import ModelRegistration
        mrLogic = ModelRegistration.ModelRegistrationLogic()
        mrLogic.run(sourceModel, targetModel, sourceToTargetTransform)
        mrLogic.ComputeMeanDistance(sourceModel, targetModel, sourceToTargetTransform)
        node=slicer.util.getNode('3.75/8_UpperImpl')
        node.SetName((ui.locationcomboBox.currentText)+':'+ '3.75/8_Implant')            
        node2=slicer.util.getNode('3.75/8_UpperGuideRing')
        node2.SetName((ui.locationcomboBox.currentText)+':'+ '3.75/8_GuideRing')            
        node3=slicer.util.getNode('3.75/8_UpperImplAxis')
        node3.SetName((ui.locationcomboBox.currentText)+':'+'3.75/8_ImplAxis')            
        node5=slicer.util.getNode(transformNode4.GetName())
        node5.SetName((ui.locationcomboBox.currentText)+':'+'3.75/8_UnitTransformInteraction')            
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())
        node6=slicer.util.getNode(transformNodeF.GetName())
        node6.SetName((ui.locationcomboBox.currentText)+':'+'3.75/8_TransformUnit')

        ringModelNode = slicer.util.getNode((ui.locationcomboBox.currentText)+':'+ '3.75/8_GuideRing')        
        transformNodeID = ringModelNode.GetTransformNodeID()        
        transformNode = slicer.mrmlScene.GetNodeByID(transformNodeID)        
        transformNode.SetName((ui.locationcomboBox.currentText)+':'+"RingTransform")        
        transformableNode = ringModelNode       
        if not transformNode or not transformableNode:
            slicer.util.errorDisplay("Transform node or transformable node not found!")
            return
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID())        
        transformMatrix = vtk.vtkMatrix4x4()
        transformNode.GetMatrixTransformToParent(transformMatrix)
        transformMatrix.SetElement(2, 3,-12)
        transformNode.SetMatrixTransformToParent(transformMatrix)
         
        helper.FilterTreeItems()

        
    elif selected_jaw == 'Upper' and selected_implant_system=='MIS_7 Implant System' and selected_implant== '3.75/10':
        angle, model = helper.createCenteredSolidTaperedTube(D1=3.75, D2=3.1, length=10.0)
        ringmodel,outerBottom, outerTop,innerBottom   = helper.createHollowTaperedTube(OD1=8.4, OD2=8.4, ID1=4.7, ID2=4.7, height=4, pointListNode=pointListNode)
        radius, height, resolution, model = helper.createimplantaxis(radius=0.5, height=50.0, resolution=60)
        radius, height, resolution, model = helper.createimplantcylinder(radius=1.875, height=10.0, resolution=60, pointListNode=pointListNode)
        
        node=slicer.util.getNode('CenteredCappedTaperedTube')
        node.SetName('3.75/10_UpperImpl')
        node2=slicer.util.getNode('HollowTaperedTube')
        node2.SetName('3.75/10_UpperGuideRing')
        node3=slicer.util.getNode('Implant Axis')
        node3.SetName('3.75/10_UpperImplAxis')
        node4=slicer.util.getNode('Implant Cylinder')
        node4.SetName('3.75/10_UpperImplCylinder') 
        
        transformNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode= slicer.util.getNode('3.75/10_UpperImpl')
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID()) 
        transformableNode2= slicer.util.getNode('3.75/10_UpperImplAxis')
        transformableNode2.SetAndObserveTransformNodeID(transformNode.GetID())            
        transformNode2 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode3= slicer.util.getNode('3.75/10_UpperGuideRing')
        transformableNode3.SetAndObserveTransformNodeID(transformNode2.GetID())            
        transformNode3 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode4= slicer.util.getNode('3.75/10_UpperImplCylinder')
        transformableNode4.SetAndObserveTransformNodeID(transformNode3.GetID())
        transformNode4 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode2.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode3.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())
        
        sourceModel = slicer.util.getNode('3.75/10_UpperImplCylinder')
        for modelNode in slicer.util.getNodesByClass("vtkMRMLModelNode"):
            name = modelNode.GetName()
            if name == ui.locationcomboBox.currentText:
                targetModel=modelNode  
        sourceToTargetTransform = slicer.util.getNode(transformNode4.GetName())
        
        import ModelRegistration
        mrLogic = ModelRegistration.ModelRegistrationLogic()
        mrLogic.run(sourceModel, targetModel, sourceToTargetTransform)
        mrLogic.ComputeMeanDistance(sourceModel, targetModel, sourceToTargetTransform)
        node=slicer.util.getNode('3.75/10_UpperImpl')
        node.SetName((ui.locationcomboBox.currentText)+':'+ '3.75/10_Implant')            
        node2=slicer.util.getNode('3.75/10_UpperGuideRing')
        node2.SetName((ui.locationcomboBox.currentText)+':'+ '3.75/10_GuideRing')            
        node3=slicer.util.getNode('3.75/10_UpperImplAxis')
        node3.SetName((ui.locationcomboBox.currentText)+':'+'3.75/10_ImplAxis')            
        node5=slicer.util.getNode(transformNode4.GetName())
        node5.SetName((ui.locationcomboBox.currentText)+':'+'3.75/10_UnitTransformInteraction')            
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())
        node6=slicer.util.getNode(transformNodeF.GetName())
        node6.SetName((ui.locationcomboBox.currentText)+':'+'3.75/10_TransformUnit')

        ringModelNode = slicer.util.getNode((ui.locationcomboBox.currentText)+':'+ '3.75/10_GuideRing')        
        transformNodeID = ringModelNode.GetTransformNodeID()        
        transformNode = slicer.mrmlScene.GetNodeByID(transformNodeID)        
        transformNode.SetName((ui.locationcomboBox.currentText)+':'+"RingTransform")        
        transformableNode = ringModelNode       
        if not transformNode or not transformableNode:
            slicer.util.errorDisplay("Transform node or transformable node not found!")
            return
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID())        
        transformMatrix = vtk.vtkMatrix4x4()
        transformNode.GetMatrixTransformToParent(transformMatrix)
        transformMatrix.SetElement(2, 3,-13)
        transformNode.SetMatrixTransformToParent(transformMatrix)
         
         
        helper.FilterTreeItems()

    elif selected_jaw == 'Upper' and selected_implant_system=='MIS_7 Implant System' and selected_implant== '3.75/11.5':
        angle, model = helper.createCenteredSolidTaperedTube(D1=3.75, D2=3.1, length=11.5)
        ringmodel,outerBottom, outerTop,innerBottom   = helper.createHollowTaperedTube(OD1=8.4, OD2=8.4, ID1=4.7, ID2=4.7, height=4, pointListNode=pointListNode)
        radius, height, resolution, model = helper.createimplantaxis(radius=0.5, height=50.0, resolution=60)
        radius, height, resolution, model = helper.createimplantcylinder(radius=1.875, height=11.5, resolution=60, pointListNode=pointListNode)
        
        node=slicer.util.getNode('CenteredCappedTaperedTube')
        node.SetName('3.75/11.5_UpperImpl')
        node2=slicer.util.getNode('HollowTaperedTube')
        node2.SetName('3.75/11.5_UpperGuideRing')
        node3=slicer.util.getNode('Implant Axis')
        node3.SetName('3.75/11.5_UpperImplAxis')
        node4=slicer.util.getNode('Implant Cylinder')
        node4.SetName('3.75/11.5_UpperImplCylinder') 
        
        transformNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode= slicer.util.getNode('3.75/11.5_UpperImpl')
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID()) 
        transformableNode2= slicer.util.getNode('3.75/11.5_UpperImplAxis')
        transformableNode2.SetAndObserveTransformNodeID(transformNode.GetID())            
        transformNode2 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode3= slicer.util.getNode('3.75/11.5_UpperGuideRing')
        transformableNode3.SetAndObserveTransformNodeID(transformNode2.GetID())            
        transformNode3 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode4= slicer.util.getNode('3.75/11.5_UpperImplCylinder')
        transformableNode4.SetAndObserveTransformNodeID(transformNode3.GetID())
        transformNode4 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode2.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode3.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())
        
        sourceModel = slicer.util.getNode('3.75/11.5_UpperImplCylinder')
        for modelNode in slicer.util.getNodesByClass("vtkMRMLModelNode"):
            name = modelNode.GetName()
            if name == ui.locationcomboBox.currentText:
                targetModel=modelNode  
        sourceToTargetTransform = slicer.util.getNode(transformNode4.GetName())
        
        import ModelRegistration
        mrLogic = ModelRegistration.ModelRegistrationLogic()
        mrLogic.run(sourceModel, targetModel, sourceToTargetTransform)
        mrLogic.ComputeMeanDistance(sourceModel, targetModel, sourceToTargetTransform)
        node=slicer.util.getNode('3.75/11.5_UpperImpl')
        node.SetName((ui.locationcomboBox.currentText)+':'+ '3.75/11.5_Implant')            
        node2=slicer.util.getNode('3.75/11.5_UpperGuideRing')
        node2.SetName((ui.locationcomboBox.currentText)+':'+ '3.75/11.5_GuideRing')            
        node3=slicer.util.getNode('3.75/11.5_UpperImplAxis')
        node3.SetName((ui.locationcomboBox.currentText)+':'+'3.75/11.5_ImplAxis')            
        node5=slicer.util.getNode(transformNode4.GetName())
        node5.SetName((ui.locationcomboBox.currentText)+':'+'3.75/11.5_UnitTransformInteraction')            
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())
        node6=slicer.util.getNode(transformNodeF.GetName())
        node6.SetName((ui.locationcomboBox.currentText)+':'+'3.75/11.5_TransformUnit')

        ringModelNode = slicer.util.getNode((ui.locationcomboBox.currentText)+':'+ '3.75/11.5_GuideRing')        
        transformNodeID = ringModelNode.GetTransformNodeID()        
        transformNode = slicer.mrmlScene.GetNodeByID(transformNodeID)        
        transformNode.SetName((ui.locationcomboBox.currentText)+':'+"RingTransform")        
        transformableNode = ringModelNode       
        if not transformNode or not transformableNode:
            slicer.util.errorDisplay("Transform node or transformable node not found!")
            return
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID())        
        transformMatrix = vtk.vtkMatrix4x4()
        transformNode.GetMatrixTransformToParent(transformMatrix)
        transformMatrix.SetElement(2, 3,-13.75)
        transformNode.SetMatrixTransformToParent(transformMatrix)
         
        helper.FilterTreeItems()

    elif selected_jaw == 'Upper' and selected_implant_system=='MIS_7 Implant System' and selected_implant== '3.75/13':
        angle, model = helper.createCenteredSolidTaperedTube(D1=3.75, D2=3.1, length=13)
        ringmodel,outerBottom, outerTop,innerBottom   = helper.createHollowTaperedTube(OD1=8.4, OD2=8.4, ID1=4.7, ID2=4.7, height=4, pointListNode=pointListNode)
        radius, height, resolution, model = helper.createimplantaxis(radius=0.5, height=50.0, resolution=60)
        radius, height, resolution, model = helper.createimplantcylinder(radius=1.875, height=13, resolution=60, pointListNode=pointListNode)
        
        node=slicer.util.getNode('CenteredCappedTaperedTube')
        node.SetName('3.75/13_UpperImpl')
        node2=slicer.util.getNode('HollowTaperedTube')
        node2.SetName('3.75/13_UpperGuideRing')
        node3=slicer.util.getNode('Implant Axis')
        node3.SetName('3.75/13_UpperImplAxis')
        node4=slicer.util.getNode('Implant Cylinder')
        node4.SetName('3.75/13_UpperImplCylinder') 
        
        transformNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode= slicer.util.getNode('3.75/13_UpperImpl')
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID()) 
        transformableNode2= slicer.util.getNode('3.75/13_UpperImplAxis')
        transformableNode2.SetAndObserveTransformNodeID(transformNode.GetID())            
        transformNode2 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode3= slicer.util.getNode('3.75/13_UpperGuideRing')
        transformableNode3.SetAndObserveTransformNodeID(transformNode2.GetID())            
        transformNode3 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode4= slicer.util.getNode('3.75/13_UpperImplCylinder')
        transformableNode4.SetAndObserveTransformNodeID(transformNode3.GetID())
        transformNode4 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode2.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode3.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())
        
        sourceModel = slicer.util.getNode('3.75/13_UpperImplCylinder')
        for modelNode in slicer.util.getNodesByClass("vtkMRMLModelNode"):
            name = modelNode.GetName()
            if name == ui.locationcomboBox.currentText:
                targetModel=modelNode  
        sourceToTargetTransform = slicer.util.getNode(transformNode4.GetName())
        
        import ModelRegistration
        mrLogic = ModelRegistration.ModelRegistrationLogic()
        mrLogic.run(sourceModel, targetModel, sourceToTargetTransform)
        mrLogic.ComputeMeanDistance(sourceModel, targetModel, sourceToTargetTransform)
        node=slicer.util.getNode('3.75/13_UpperImpl')
        node.SetName((ui.locationcomboBox.currentText)+':'+ '3.75/13_Implant')            
        node2=slicer.util.getNode('3.75/13_UpperGuideRing')
        node2.SetName((ui.locationcomboBox.currentText)+':'+ '3.75/13_GuideRing')            
        node3=slicer.util.getNode('3.75/13_UpperImplAxis')
        node3.SetName((ui.locationcomboBox.currentText)+':'+'3.75/13_ImplAxis')            
        node5=slicer.util.getNode(transformNode4.GetName())
        node5.SetName((ui.locationcomboBox.currentText)+':'+'3.75/13_UnitTransformInteraction')            
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())
        node6=slicer.util.getNode(transformNodeF.GetName())
        node6.SetName((ui.locationcomboBox.currentText)+':'+'3.75/13_TransformUnit')

        ringModelNode = slicer.util.getNode((ui.locationcomboBox.currentText)+':'+ '3.75/13_GuideRing')        
        transformNodeID = ringModelNode.GetTransformNodeID()        
        transformNode = slicer.mrmlScene.GetNodeByID(transformNodeID)        
        transformNode.SetName((ui.locationcomboBox.currentText)+':'+"RingTransform")        
        transformableNode = ringModelNode       
        if not transformNode or not transformableNode:
            slicer.util.errorDisplay("Transform node or transformable node not found!")
            return
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID())        
        transformMatrix = vtk.vtkMatrix4x4()
        transformNode.GetMatrixTransformToParent(transformMatrix)
        transformMatrix.SetElement(2, 3,-14.5)
        transformNode.SetMatrixTransformToParent(transformMatrix)
         
        helper.FilterTreeItems()


    elif selected_jaw == 'Upper' and selected_implant_system=='MIS_7 Implant System' and selected_implant== '3.75/16':
        angle, model = helper.createCenteredSolidTaperedTube(D1=3.75, D2=3.1, length=16)
        ringmodel,outerBottom, outerTop,innerBottom   = helper.createHollowTaperedTube(OD1=8.4, OD2=8.4, ID1=4.7, ID2=4.7, height=4, pointListNode=pointListNode)
        radius, height, resolution, model = helper.createimplantaxis(radius=0.5, height=50.0, resolution=60)
        radius, height, resolution, model = helper.createimplantcylinder(radius=1.875, height=16, resolution=60, pointListNode=pointListNode)
        
        node=slicer.util.getNode('CenteredCappedTaperedTube')
        node.SetName('3.75/16_UpperImpl')
        node2=slicer.util.getNode('HollowTaperedTube')
        node2.SetName('3.75/16_UpperGuideRing')
        node3=slicer.util.getNode('Implant Axis')
        node3.SetName('3.75/16_UpperImplAxis')
        node4=slicer.util.getNode('Implant Cylinder')
        node4.SetName('3.75/16_UpperImplCylinder') 
        
        transformNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode= slicer.util.getNode('3.75/16_UpperImpl')
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID()) 
        transformableNode2= slicer.util.getNode('3.75/16_UpperImplAxis')
        transformableNode2.SetAndObserveTransformNodeID(transformNode.GetID())            
        transformNode2 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode3= slicer.util.getNode('3.75/16_UpperGuideRing')
        transformableNode3.SetAndObserveTransformNodeID(transformNode2.GetID())            
        transformNode3 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode4= slicer.util.getNode('3.75/16_UpperImplCylinder')
        transformableNode4.SetAndObserveTransformNodeID(transformNode3.GetID())
        transformNode4 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode2.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode3.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())
        
        sourceModel = slicer.util.getNode('3.75/16_UpperImplCylinder')
        for modelNode in slicer.util.getNodesByClass("vtkMRMLModelNode"):
            name = modelNode.GetName()
            if name == ui.locationcomboBox.currentText:
                targetModel=modelNode  
        sourceToTargetTransform = slicer.util.getNode(transformNode4.GetName())
        
        import ModelRegistration
        mrLogic = ModelRegistration.ModelRegistrationLogic()
        mrLogic.run(sourceModel, targetModel, sourceToTargetTransform)
        mrLogic.ComputeMeanDistance(sourceModel, targetModel, sourceToTargetTransform)
        node=slicer.util.getNode('3.75/16_UpperImpl')
        node.SetName((ui.locationcomboBox.currentText)+':'+ '3.75/16_Implant')            
        node2=slicer.util.getNode('3.75/16_UpperGuideRing')
        node2.SetName((ui.locationcomboBox.currentText)+':'+ '3.75/16_GuideRing')            
        node3=slicer.util.getNode('3.75/16_UpperImplAxis')
        node3.SetName((ui.locationcomboBox.currentText)+':'+'3.75/16_ImplAxis')            
        node5=slicer.util.getNode(transformNode4.GetName())
        node5.SetName((ui.locationcomboBox.currentText)+':'+'3.75/16_UnitTransformInteraction')            
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())
        node6=slicer.util.getNode(transformNodeF.GetName())
        node6.SetName((ui.locationcomboBox.currentText)+':'+'3.75/16_TransformUnit')

        ringModelNode = slicer.util.getNode((ui.locationcomboBox.currentText)+':'+ '3.75/16_GuideRing')        
        transformNodeID = ringModelNode.GetTransformNodeID()        
        transformNode = slicer.mrmlScene.GetNodeByID(transformNodeID)        
        transformNode.SetName((ui.locationcomboBox.currentText)+':'+"RingTransform")        
        transformableNode = ringModelNode       
        if not transformNode or not transformableNode:
            slicer.util.errorDisplay("Transform node or transformable node not found!")
            return
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID())        
        transformMatrix = vtk.vtkMatrix4x4()
        transformNode.GetMatrixTransformToParent(transformMatrix)
        transformMatrix.SetElement(2, 3,-16)
        transformNode.SetMatrixTransformToParent(transformMatrix)
         
        helper.FilterTreeItems()


        
    elif selected_jaw == 'Upper' and selected_implant_system=='MIS_7 Implant System' and selected_implant== '4.2/6':
        angle, model = helper.createCenteredSolidTaperedTube(D1=4.2, D2=3.7, length=6.0)
        ringmodel,outerBottom, outerTop,innerBottom   = helper.createHollowTaperedTube(OD1=8.4, OD2=8.4, ID1=4.7, ID2=4.7, height=4, pointListNode=pointListNode)
        radius, height, resolution, model = helper.createimplantaxis(radius=0.5, height=50.0, resolution=60)
        radius, height, resolution, model = helper.createimplantcylinder(radius=2.1, height=6, resolution=60, pointListNode=pointListNode)
        
        node=slicer.util.getNode('CenteredCappedTaperedTube')
        node.SetName('4.2/6_UpperImpl')
        node2=slicer.util.getNode('HollowTaperedTube')
        node2.SetName('4.2/6_UpperGuideRing')
        node3=slicer.util.getNode('Implant Axis')
        node3.SetName('4.2/6_UpperImplAxis')
        node4=slicer.util.getNode('Implant Cylinder')
        node4.SetName('4.2/6_UpperImplCylinder') 
        
        transformNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode= slicer.util.getNode('4.2/6_UpperImpl')
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID()) 
        transformableNode2= slicer.util.getNode('4.2/6_UpperImplAxis')
        transformableNode2.SetAndObserveTransformNodeID(transformNode.GetID())            
        transformNode2 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode3= slicer.util.getNode('4.2/6_UpperGuideRing')
        transformableNode3.SetAndObserveTransformNodeID(transformNode2.GetID())            
        transformNode3 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode4= slicer.util.getNode('4.2/6_UpperImplCylinder')
        transformableNode4.SetAndObserveTransformNodeID(transformNode3.GetID())
        transformNode4 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode2.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode3.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())
        
        sourceModel = slicer.util.getNode('4.2/6_UpperImplCylinder')
        for modelNode in slicer.util.getNodesByClass("vtkMRMLModelNode"):
            name = modelNode.GetName()
            if name == ui.locationcomboBox.currentText:
                targetModel=modelNode  
        sourceToTargetTransform = slicer.util.getNode(transformNode4.GetName())
        
        import ModelRegistration
        mrLogic = ModelRegistration.ModelRegistrationLogic()
        mrLogic.run(sourceModel, targetModel, sourceToTargetTransform)
        mrLogic.ComputeMeanDistance(sourceModel, targetModel, sourceToTargetTransform)
        node=slicer.util.getNode('4.2/6_UpperImpl')
        node.SetName((ui.locationcomboBox.currentText)+':'+ '4.2/6_Implant')            
        node2=slicer.util.getNode('4.2/6_UpperGuideRing')
        node2.SetName((ui.locationcomboBox.currentText)+':'+ '4.2/6_GuideRing')            
        node3=slicer.util.getNode('4.2/6_UpperImplAxis')
        node3.SetName((ui.locationcomboBox.currentText)+':'+'4.2/6_ImplAxis')            
        node5=slicer.util.getNode(transformNode4.GetName())
        node5.SetName((ui.locationcomboBox.currentText)+':'+'4.2/6_UnitTransformInteraction')            
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())
        node6=slicer.util.getNode(transformNodeF.GetName())
        node6.SetName((ui.locationcomboBox.currentText)+':'+'4.2/6_TransformUnit')

        ringModelNode = slicer.util.getNode((ui.locationcomboBox.currentText)+':'+ '4.2/6_GuideRing')        
        transformNodeID = ringModelNode.GetTransformNodeID()        
        transformNode = slicer.mrmlScene.GetNodeByID(transformNodeID)        
        transformNode.SetName((ui.locationcomboBox.currentText)+':'+"RingTransform")        
        transformableNode = ringModelNode       
        if not transformNode or not transformableNode:
            slicer.util.errorDisplay("Transform node or transformable node not found!")
            return
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID())        
        transformMatrix = vtk.vtkMatrix4x4()
        transformNode.GetMatrixTransformToParent(transformMatrix)
        transformMatrix.SetElement(2, 3,-11)
        transformNode.SetMatrixTransformToParent(transformMatrix)
         
        helper.FilterTreeItems()




    elif selected_jaw == 'Upper' and selected_implant_system=='MIS_7 Implant System' and selected_implant== '4.2/8':
        
        angle, model = helper.createCenteredSolidTaperedTube(D1=4.2, D2=3.7, length=8.0)
        ringmodel,outerBottom, outerTop,innerBottom   = helper.createHollowTaperedTube(OD1=8.4, OD2=8.4, ID1=4.7, ID2=4.7, height=4, pointListNode=pointListNode)
        radius, height, resolution, model = helper.createimplantaxis(radius=0.5, height=50.0, resolution=60)
        radius, height, resolution, model = helper.createimplantcylinder(radius=2.1, height=8, resolution=60, pointListNode=pointListNode)
        
        node=slicer.util.getNode('CenteredCappedTaperedTube')
        node.SetName('4.2/8_UpperImpl')
        node2=slicer.util.getNode('HollowTaperedTube')
        node2.SetName('4.2/8_UpperGuideRing')
        node3=slicer.util.getNode('Implant Axis')
        node3.SetName('4.2/8_UpperImplAxis')
        node4=slicer.util.getNode('Implant Cylinder')
        node4.SetName('4.2/8_UpperImplCylinder') 
        
        transformNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode= slicer.util.getNode('4.2/8_UpperImpl')
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID()) 
        transformableNode2= slicer.util.getNode('4.2/8_UpperImplAxis')
        transformableNode2.SetAndObserveTransformNodeID(transformNode.GetID())            
        transformNode2 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode3= slicer.util.getNode('4.2/8_UpperGuideRing')
        transformableNode3.SetAndObserveTransformNodeID(transformNode2.GetID())            
        transformNode3 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode4= slicer.util.getNode('4.2/8_UpperImplCylinder')
        transformableNode4.SetAndObserveTransformNodeID(transformNode3.GetID())
        transformNode4 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode2.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode3.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())
        
        sourceModel = slicer.util.getNode('4.2/8_UpperImplCylinder')
        for modelNode in slicer.util.getNodesByClass("vtkMRMLModelNode"):
            name = modelNode.GetName()
            if name == ui.locationcomboBox.currentText:
                targetModel=modelNode  
        sourceToTargetTransform = slicer.util.getNode(transformNode4.GetName())
        
        import ModelRegistration
        mrLogic = ModelRegistration.ModelRegistrationLogic()
        mrLogic.run(sourceModel, targetModel, sourceToTargetTransform)
        mrLogic.ComputeMeanDistance(sourceModel, targetModel, sourceToTargetTransform)
        node=slicer.util.getNode('4.2/8_UpperImpl')
        node.SetName((ui.locationcomboBox.currentText)+':'+ '4.2/8_Implant')            
        node2=slicer.util.getNode('4.2/8_UpperGuideRing')
        node2.SetName((ui.locationcomboBox.currentText)+':'+ '4.2/8_GuideRing')            
        node3=slicer.util.getNode('4.2/8_UpperImplAxis')
        node3.SetName((ui.locationcomboBox.currentText)+':'+'4.2/8_ImplAxis')            
        node5=slicer.util.getNode(transformNode4.GetName())
        node5.SetName((ui.locationcomboBox.currentText)+':'+'4.2/8_UnitTransformInteraction')            
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())
        node6=slicer.util.getNode(transformNodeF.GetName())
        node6.SetName((ui.locationcomboBox.currentText)+':'+'4.2/8_TransformUnit')

        ringModelNode = slicer.util.getNode((ui.locationcomboBox.currentText)+':'+ '4.2/8_GuideRing')        
        transformNodeID = ringModelNode.GetTransformNodeID()        
        transformNode = slicer.mrmlScene.GetNodeByID(transformNodeID)        
        transformNode.SetName((ui.locationcomboBox.currentText)+':'+"RingTransform")        
        transformableNode = ringModelNode       
        if not transformNode or not transformableNode:
            slicer.util.errorDisplay("Transform node or transformable node not found!")
            return
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID())        
        transformMatrix = vtk.vtkMatrix4x4()
        transformNode.GetMatrixTransformToParent(transformMatrix)
        transformMatrix.SetElement(2, 3,-12)
        transformNode.SetMatrixTransformToParent(transformMatrix)
         
        helper.FilterTreeItems()


    elif selected_jaw == 'Upper' and selected_implant_system=='MIS_7 Implant System' and selected_implant== '4.2/10':
                     
        angle, model = helper.createCenteredSolidTaperedTube(D1=4.2, D2=3.7, length=10.0)
        ringmodel,outerBottom, outerTop,innerBottom   = helper.createHollowTaperedTube(OD1=8.4, OD2=8.4, ID1=4.7, ID2=4.7, height=4, pointListNode=pointListNode)

        radius, height, resolution, model = helper.createimplantaxis(radius=0.5, height=50.0, resolution=60)
        radius, height, resolution, model = helper.createimplantcylinder(radius=2.1, height=10, resolution=60, pointListNode=pointListNode)

        node=slicer.util.getNode('CenteredCappedTaperedTube')
        node.SetName('4.2/10_UpperImpl')
        node2=slicer.util.getNode('HollowTaperedTube')
        node2.SetName('4.2/10_UpperGuideRing')
        node3=slicer.util.getNode('Implant Axis')
        node3.SetName('4.2/10_UpperImplAxis')
        node4=slicer.util.getNode('Implant Cylinder')
        node4.SetName('4.2/10_UpperImplCylinder') 

        transformNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode= slicer.util.getNode('4.2/10_UpperImpl')
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID()) 
        transformableNode2= slicer.util.getNode('4.2/10_UpperImplAxis')
        transformableNode2.SetAndObserveTransformNodeID(transformNode.GetID())            
        transformNode2 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode3= slicer.util.getNode('4.2/10_UpperGuideRing')
        transformableNode3.SetAndObserveTransformNodeID(transformNode2.GetID())            
        transformNode3 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode4= slicer.util.getNode('4.2/10_UpperImplCylinder')
        transformableNode4.SetAndObserveTransformNodeID(transformNode3.GetID())
        transformNode4 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode2.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode3.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())

        sourceModel = slicer.util.getNode('4.2/10_UpperImplCylinder')
        for modelNode in slicer.util.getNodesByClass("vtkMRMLModelNode"):
            name = modelNode.GetName()
            if name == ui.locationcomboBox.currentText:
                targetModel=modelNode  
        sourceToTargetTransform = slicer.util.getNode(transformNode4.GetName())

        import ModelRegistration
        mrLogic = ModelRegistration.ModelRegistrationLogic()
        mrLogic.run(sourceModel, targetModel, sourceToTargetTransform)
        mrLogic.ComputeMeanDistance(sourceModel, targetModel, sourceToTargetTransform)
        node=slicer.util.getNode('4.2/10_UpperImpl')
        node.SetName((ui.locationcomboBox.currentText)+':'+ '4.2/10_Implant')            
        node2=slicer.util.getNode('4.2/10_UpperGuideRing')
        node2.SetName((ui.locationcomboBox.currentText)+':'+ '4.2/10_GuideRing')            
        node3=slicer.util.getNode('4.2/10_UpperImplAxis')
        node3.SetName((ui.locationcomboBox.currentText)+':'+'4.2/10_ImplAxis')            
        node5=slicer.util.getNode(transformNode4.GetName())
        node5.SetName((ui.locationcomboBox.currentText)+':'+'4.2/10_UnitTransformInteraction')            
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())
        node6=slicer.util.getNode(transformNodeF.GetName())
        node6.SetName((ui.locationcomboBox.currentText)+':'+'4.2/10_TransformUnit')

        ringModelNode = slicer.util.getNode((ui.locationcomboBox.currentText)+':'+ '4.2/10_GuideRing')        
        transformNodeID = ringModelNode.GetTransformNodeID()        
        transformNode = slicer.mrmlScene.GetNodeByID(transformNodeID)        
        transformNode.SetName((ui.locationcomboBox.currentText)+':'+"RingTransform")        
        transformableNode = ringModelNode       
        if not transformNode or not transformableNode:
            slicer.util.errorDisplay("Transform node or transformable node not found!")
            return
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID())        
        transformMatrix = vtk.vtkMatrix4x4()
        transformNode.GetMatrixTransformToParent(transformMatrix)
        transformMatrix.SetElement(2, 3,-13)
        transformNode.SetMatrixTransformToParent(transformMatrix)
         
        helper.FilterTreeItems()



    elif selected_jaw == 'Upper' and selected_implant_system=='MIS_7 Implant System' and selected_implant== '4.2/11.5':
                                             
        angle, model = helper.createCenteredSolidTaperedTube(D1=4.2, D2=3.7, length=11.5)
        ringmodel,outerBottom, outerTop,innerBottom   = helper.createHollowTaperedTube(OD1=8.4, OD2=8.4, ID1=4.7, ID2=4.7, height=4, pointListNode=pointListNode)

        radius, height, resolution, model = helper.createimplantaxis(radius=0.5, height=50.0, resolution=60)
        radius, height, resolution, model = helper.createimplantcylinder(radius=2.1, height=11.5, resolution=60, pointListNode=pointListNode)

        node=slicer.util.getNode('CenteredCappedTaperedTube')
        node.SetName('4.2/11.5_UpperImpl')
        node2=slicer.util.getNode('HollowTaperedTube')
        node2.SetName('4.2/11.5_UpperGuideRing')
        node3=slicer.util.getNode('Implant Axis')
        node3.SetName('4.2/11.5_UpperImplAxis')
        node4=slicer.util.getNode('Implant Cylinder')
        node4.SetName('4.2/11.5_UpperImplCylinder') 

        transformNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode= slicer.util.getNode('4.2/11.5_UpperImpl')
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID()) 
        transformableNode2= slicer.util.getNode('4.2/11.5_UpperImplAxis')
        transformableNode2.SetAndObserveTransformNodeID(transformNode.GetID())            
        transformNode2 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode3= slicer.util.getNode('4.2/11.5_UpperGuideRing')
        transformableNode3.SetAndObserveTransformNodeID(transformNode2.GetID())            
        transformNode3 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode4= slicer.util.getNode('4.2/11.5_UpperImplCylinder')
        transformableNode4.SetAndObserveTransformNodeID(transformNode3.GetID())
        transformNode4 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode2.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode3.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())

        sourceModel = slicer.util.getNode('4.2/11.5_UpperImplCylinder')
        for modelNode in slicer.util.getNodesByClass("vtkMRMLModelNode"):
            name = modelNode.GetName()
            if name == ui.locationcomboBox.currentText:
                targetModel=modelNode  
        sourceToTargetTransform = slicer.util.getNode(transformNode4.GetName())

        import ModelRegistration
        mrLogic = ModelRegistration.ModelRegistrationLogic()
        mrLogic.run(sourceModel, targetModel, sourceToTargetTransform)
        mrLogic.ComputeMeanDistance(sourceModel, targetModel, sourceToTargetTransform)
        node=slicer.util.getNode('4.2/11.5_UpperImpl')
        node.SetName((ui.locationcomboBox.currentText)+':'+ '4.2/11.5_Implant')            
        node2=slicer.util.getNode('4.2/11.5_UpperGuideRing')
        node2.SetName((ui.locationcomboBox.currentText)+':'+ '4.2/11.5_GuideRing')            
        node3=slicer.util.getNode('4.2/11.5_UpperImplAxis')
        node3.SetName((ui.locationcomboBox.currentText)+':'+'4.2/11.5_ImplAxis')            
        node5=slicer.util.getNode(transformNode4.GetName())
        node5.SetName((ui.locationcomboBox.currentText)+':'+'4.2/11.5_UnitTransformInteraction')            
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())
        node6=slicer.util.getNode(transformNodeF.GetName())
        node6.SetName((ui.locationcomboBox.currentText)+':'+'4.2/11.5_TransformUnit')

        ringModelNode = slicer.util.getNode((ui.locationcomboBox.currentText)+':'+ '4.2/11.5_GuideRing')        
        transformNodeID = ringModelNode.GetTransformNodeID()        
        transformNode = slicer.mrmlScene.GetNodeByID(transformNodeID)        
        transformNode.SetName((ui.locationcomboBox.currentText)+':'+"RingTransform")        
        transformableNode = ringModelNode       
        if not transformNode or not transformableNode:
            slicer.util.errorDisplay("Transform node or transformable node not found!")
            return
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID())        
        transformMatrix = vtk.vtkMatrix4x4()
        transformNode.GetMatrixTransformToParent(transformMatrix)
        transformMatrix.SetElement(2, 3,-13.75)
        transformNode.SetMatrixTransformToParent(transformMatrix)
         
        helper.FilterTreeItems()



        

    elif selected_jaw == 'Upper' and selected_implant_system=='MIS_7 Implant System' and selected_implant== '4.2/13':
                                 
        angle, model = helper.createCenteredSolidTaperedTube(D1=4.2, D2=3.7, length=13)
        ringmodel,outerBottom, outerTop,innerBottom   = helper.createHollowTaperedTube(OD1=8.4, OD2=8.4, ID1=4.7, ID2=4.7, height=4, pointListNode=pointListNode)

        radius, height, resolution, model = helper.createimplantaxis(radius=0.5, height=50.0, resolution=60)
        radius, height, resolution, model = helper.createimplantcylinder(radius=2.1, height=13, resolution=60, pointListNode=pointListNode)

        node=slicer.util.getNode('CenteredCappedTaperedTube')
        node.SetName('4.2/13_UpperImpl')
        node2=slicer.util.getNode('HollowTaperedTube')
        node2.SetName('4.2/13_UpperGuideRing')
        node3=slicer.util.getNode('Implant Axis')
        node3.SetName('4.2/13_UpperImplAxis')
        node4=slicer.util.getNode('Implant Cylinder')
        node4.SetName('4.2/13_UpperImplCylinder') 

        transformNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode= slicer.util.getNode('4.2/13_UpperImpl')
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID()) 
        transformableNode2= slicer.util.getNode('4.2/13_UpperImplAxis')
        transformableNode2.SetAndObserveTransformNodeID(transformNode.GetID())            
        transformNode2 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode3= slicer.util.getNode('4.2/13_UpperGuideRing')
        transformableNode3.SetAndObserveTransformNodeID(transformNode2.GetID())            
        transformNode3 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode4= slicer.util.getNode('4.2/13_UpperImplCylinder')
        transformableNode4.SetAndObserveTransformNodeID(transformNode3.GetID())
        transformNode4 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode2.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode3.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())

        sourceModel = slicer.util.getNode('4.2/13_UpperImplCylinder')
        for modelNode in slicer.util.getNodesByClass("vtkMRMLModelNode"):
            name = modelNode.GetName()
            if name == ui.locationcomboBox.currentText:
                targetModel=modelNode  
        sourceToTargetTransform = slicer.util.getNode(transformNode4.GetName())

        import ModelRegistration
        mrLogic = ModelRegistration.ModelRegistrationLogic()
        mrLogic.run(sourceModel, targetModel, sourceToTargetTransform)
        mrLogic.ComputeMeanDistance(sourceModel, targetModel, sourceToTargetTransform)
        node=slicer.util.getNode('4.2/13_UpperImpl')
        node.SetName((ui.locationcomboBox.currentText)+':'+ '4.2/13_Implant')            
        node2=slicer.util.getNode('4.2/13_UpperGuideRing')
        node2.SetName((ui.locationcomboBox.currentText)+':'+ '4.2/13_GuideRing')            
        node3=slicer.util.getNode('4.2/13_UpperImplAxis')
        node3.SetName((ui.locationcomboBox.currentText)+':'+'4.2/13_ImplAxis')            
        node5=slicer.util.getNode(transformNode4.GetName())
        node5.SetName((ui.locationcomboBox.currentText)+':'+'4.2/13_UnitTransformInteraction')            
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())
        node6=slicer.util.getNode(transformNodeF.GetName())
        node6.SetName((ui.locationcomboBox.currentText)+':'+'4.2/13_TransformUnit')

        ringModelNode = slicer.util.getNode((ui.locationcomboBox.currentText)+':'+ '4.2/13_GuideRing')        
        transformNodeID = ringModelNode.GetTransformNodeID()        
        transformNode = slicer.mrmlScene.GetNodeByID(transformNodeID)        
        transformNode.SetName((ui.locationcomboBox.currentText)+':'+"RingTransform")        
        transformableNode = ringModelNode       
        if not transformNode or not transformableNode:
            slicer.util.errorDisplay("Transform node or transformable node not found!")
            return
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID())        
        transformMatrix = vtk.vtkMatrix4x4()
        transformNode.GetMatrixTransformToParent(transformMatrix)
        transformMatrix.SetElement(2, 3,-14.5)
        transformNode.SetMatrixTransformToParent(transformMatrix)
         
        helper.FilterTreeItems()




    elif selected_jaw == 'Upper' and selected_implant_system=='MIS_7 Implant System' and selected_implant== '4.2/16':
                                 
        angle, model = helper.createCenteredSolidTaperedTube(D1=4.2, D2=3.7, length=16)
        ringmodel,outerBottom, outerTop,innerBottom   = helper.createHollowTaperedTube(OD1=8.4, OD2=8.4, ID1=4.7, ID2=4.7, height=4, pointListNode=pointListNode)

        radius, height, resolution, model = helper.createimplantaxis(radius=0.5, height=50.0, resolution=60)
        radius, height, resolution, model = helper.createimplantcylinder(radius=2.1, height=16, resolution=60, pointListNode=pointListNode)

        node=slicer.util.getNode('CenteredCappedTaperedTube')
        node.SetName('4.2/16_UpperImpl')
        node2=slicer.util.getNode('HollowTaperedTube')
        node2.SetName('4.2/16_UpperGuideRing')
        node3=slicer.util.getNode('Implant Axis')
        node3.SetName('4.2/16_UpperImplAxis')
        node4=slicer.util.getNode('Implant Cylinder')
        node4.SetName('4.2/16_UpperImplCylinder') 

        transformNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode= slicer.util.getNode('4.2/16_UpperImpl')
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID()) 
        transformableNode2= slicer.util.getNode('4.2/16_UpperImplAxis')
        transformableNode2.SetAndObserveTransformNodeID(transformNode.GetID())            
        transformNode2 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode3= slicer.util.getNode('4.2/16_UpperGuideRing')
        transformableNode3.SetAndObserveTransformNodeID(transformNode2.GetID())            
        transformNode3 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode4= slicer.util.getNode('4.2/16_UpperImplCylinder')
        transformableNode4.SetAndObserveTransformNodeID(transformNode3.GetID())
        transformNode4 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode2.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode3.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())

        sourceModel = slicer.util.getNode('4.2/16_UpperImplCylinder')
        for modelNode in slicer.util.getNodesByClass("vtkMRMLModelNode"):
            name = modelNode.GetName()
            if name == ui.locationcomboBox.currentText:
                targetModel=modelNode  
        sourceToTargetTransform = slicer.util.getNode(transformNode4.GetName())

        import ModelRegistration
        mrLogic = ModelRegistration.ModelRegistrationLogic()
        mrLogic.run(sourceModel, targetModel, sourceToTargetTransform)
        mrLogic.ComputeMeanDistance(sourceModel, targetModel, sourceToTargetTransform)
        node=slicer.util.getNode('4.2/16_UpperImpl')
        node.SetName((ui.locationcomboBox.currentText)+':'+ '4.2/16_Implant')            
        node2=slicer.util.getNode('4.2/16_UpperGuideRing')
        node2.SetName((ui.locationcomboBox.currentText)+':'+ '4.2/16_GuideRing')            
        node3=slicer.util.getNode('4.2/16_UpperImplAxis')
        node3.SetName((ui.locationcomboBox.currentText)+':'+'4.2/16_ImplAxis')            
        node5=slicer.util.getNode(transformNode4.GetName())
        node5.SetName((ui.locationcomboBox.currentText)+':'+'4.2/16_UnitTransformInteraction')            
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())
        node6=slicer.util.getNode(transformNodeF.GetName())
        node6.SetName((ui.locationcomboBox.currentText)+':'+'4.2/16_TransformUnit')

        ringModelNode = slicer.util.getNode((ui.locationcomboBox.currentText)+':'+ '4.2/16_GuideRing')        
        transformNodeID = ringModelNode.GetTransformNodeID()        
        transformNode = slicer.mrmlScene.GetNodeByID(transformNodeID)        
        transformNode.SetName((ui.locationcomboBox.currentText)+':'+"RingTransform")        
        transformableNode = ringModelNode       
        if not transformNode or not transformableNode:
            slicer.util.errorDisplay("Transform node or transformable node not found!")
            return
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID())        
        transformMatrix = vtk.vtkMatrix4x4()
        transformNode.GetMatrixTransformToParent(transformMatrix)
        transformMatrix.SetElement(2, 3,-16)
        transformNode.SetMatrixTransformToParent(transformMatrix)
         
        helper.FilterTreeItems()





    elif selected_jaw == 'Upper' and selected_implant_system=='MIS_7 Implant System' and selected_implant== '5/6':
                                 
        angle, model = helper.createCenteredSolidTaperedTube(D1=5, D2=4.5, length=6)
        ringmodel,outerBottom, outerTop,innerBottom   = helper.createHollowTaperedTube(OD1=8.4, OD2=8.4, ID1=4.7, ID2=4.7, height=4, pointListNode=pointListNode)

        radius, height, resolution, model = helper.createimplantaxis(radius=0.5, height=50.0, resolution=60)
        radius, height, resolution, model = helper.createimplantcylinder(radius=2.5, height=6, resolution=60, pointListNode=pointListNode)

        node=slicer.util.getNode('CenteredCappedTaperedTube')
        node.SetName('5/6_UpperImpl')
        node2=slicer.util.getNode('HollowTaperedTube')
        node2.SetName('5/6_UpperGuideRing')
        node3=slicer.util.getNode('Implant Axis')
        node3.SetName('5/6_UpperImplAxis')
        node4=slicer.util.getNode('Implant Cylinder')
        node4.SetName('5/6_UpperImplCylinder') 

        transformNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode= slicer.util.getNode('5/6_UpperImpl')
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID()) 
        transformableNode2= slicer.util.getNode('5/6_UpperImplAxis')
        transformableNode2.SetAndObserveTransformNodeID(transformNode.GetID())            
        transformNode2 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode3= slicer.util.getNode('5/6_UpperGuideRing')
        transformableNode3.SetAndObserveTransformNodeID(transformNode2.GetID())            
        transformNode3 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode4= slicer.util.getNode('5/6_UpperImplCylinder')
        transformableNode4.SetAndObserveTransformNodeID(transformNode3.GetID())
        transformNode4 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode2.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode3.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())

        sourceModel = slicer.util.getNode('5/6_UpperImplCylinder')
        for modelNode in slicer.util.getNodesByClass("vtkMRMLModelNode"):
            name = modelNode.GetName()
            if name == ui.locationcomboBox.currentText:
                targetModel=modelNode  
        sourceToTargetTransform = slicer.util.getNode(transformNode4.GetName())

        import ModelRegistration
        mrLogic = ModelRegistration.ModelRegistrationLogic()
        mrLogic.run(sourceModel, targetModel, sourceToTargetTransform)
        mrLogic.ComputeMeanDistance(sourceModel, targetModel, sourceToTargetTransform)
        node=slicer.util.getNode('5/6_UpperImpl')
        node.SetName((ui.locationcomboBox.currentText)+':'+ '5/6_Implant')            
        node2=slicer.util.getNode('5/6_UpperGuideRing')
        node2.SetName((ui.locationcomboBox.currentText)+':'+ '5/6_GuideRing')            
        node3=slicer.util.getNode('5/6_UpperImplAxis')
        node3.SetName((ui.locationcomboBox.currentText)+':'+'5/6_ImplAxis')            
        node5=slicer.util.getNode(transformNode4.GetName())
        node5.SetName((ui.locationcomboBox.currentText)+':'+'5/6_UnitTransformInteraction')            
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())
        node6=slicer.util.getNode(transformNodeF.GetName())
        node6.SetName((ui.locationcomboBox.currentText)+':'+'5/6_TransformUnit')

        ringModelNode = slicer.util.getNode((ui.locationcomboBox.currentText)+':'+ '5/6_GuideRing')        
        transformNodeID = ringModelNode.GetTransformNodeID()        
        transformNode = slicer.mrmlScene.GetNodeByID(transformNodeID)        
        transformNode.SetName((ui.locationcomboBox.currentText)+':'+"RingTransform")        
        transformableNode = ringModelNode       
        if not transformNode or not transformableNode:
            slicer.util.errorDisplay("Transform node or transformable node not found!")
            return
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID())        
        transformMatrix = vtk.vtkMatrix4x4()
        transformNode.GetMatrixTransformToParent(transformMatrix)
        transformMatrix.SetElement(2, 3,-11)
        transformNode.SetMatrixTransformToParent(transformMatrix)
         
        helper.FilterTreeItems()
        

    elif selected_jaw == 'Upper' and selected_implant_system=='MIS_7 Implant System' and selected_implant== '5/8':
                   
                         
        angle, model = helper.createCenteredSolidTaperedTube(D1=5, D2=4.5, length=8)
        ringmodel,outerBottom, outerTop,innerBottom   = helper.createHollowTaperedTube(OD1=8.4, OD2=8.4, ID1=4.7, ID2=4.7, height=4, pointListNode=pointListNode)

        radius, height, resolution, model = helper.createimplantaxis(radius=0.5, height=50.0, resolution=60)
        radius, height, resolution, model = helper.createimplantcylinder(radius=2.5, height=8, resolution=60, pointListNode=pointListNode)

        node=slicer.util.getNode('CenteredCappedTaperedTube')
        node.SetName('5/8_UpperImpl')
        node2=slicer.util.getNode('HollowTaperedTube')
        node2.SetName('5/8_UpperGuideRing')
        node3=slicer.util.getNode('Implant Axis')
        node3.SetName('5/8_UpperImplAxis')
        node4=slicer.util.getNode('Implant Cylinder')
        node4.SetName('5/8_UpperImplCylinder') 

        transformNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode= slicer.util.getNode('5/8_UpperImpl')
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID()) 
        transformableNode2= slicer.util.getNode('5/8_UpperImplAxis')
        transformableNode2.SetAndObserveTransformNodeID(transformNode.GetID())            
        transformNode2 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode3= slicer.util.getNode('5/8_UpperGuideRing')
        transformableNode3.SetAndObserveTransformNodeID(transformNode2.GetID())            
        transformNode3 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode4= slicer.util.getNode('5/8_UpperImplCylinder')
        transformableNode4.SetAndObserveTransformNodeID(transformNode3.GetID())
        transformNode4 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode2.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode3.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())

        sourceModel = slicer.util.getNode('5/8_UpperImplCylinder')
        for modelNode in slicer.util.getNodesByClass("vtkMRMLModelNode"):
            name = modelNode.GetName()
            if name == ui.locationcomboBox.currentText:
                targetModel=modelNode  
            sourceToTargetTransform = slicer.util.getNode(transformNode4.GetName())

        import ModelRegistration
        mrLogic = ModelRegistration.ModelRegistrationLogic()
        mrLogic.run(sourceModel, targetModel, sourceToTargetTransform)
        mrLogic.ComputeMeanDistance(sourceModel, targetModel, sourceToTargetTransform)
        node=slicer.util.getNode('5/8_UpperImpl')
        node.SetName((ui.locationcomboBox.currentText)+':'+ '5/8_Implant')            
        node2=slicer.util.getNode('5/8_UpperGuideRing')
        node2.SetName((ui.locationcomboBox.currentText)+':'+ '5/8_GuideRing')            
        node3=slicer.util.getNode('5/8_UpperImplAxis')
        node3.SetName((ui.locationcomboBox.currentText)+':'+'5/8_ImplAxis')            
        node5=slicer.util.getNode(transformNode4.GetName())
        node5.SetName((ui.locationcomboBox.currentText)+':'+'5/8_UnitTransformInteraction')            
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())
        node6=slicer.util.getNode(transformNodeF.GetName())
        node6.SetName((ui.locationcomboBox.currentText)+':'+'5/8_TransformUnit')

        ringModelNode = slicer.util.getNode((ui.locationcomboBox.currentText)+':'+ '5/8_GuideRing')        
        transformNodeID = ringModelNode.GetTransformNodeID()        
        transformNode = slicer.mrmlScene.GetNodeByID(transformNodeID)        
        transformNode.SetName((ui.locationcomboBox.currentText)+':'+"RingTransform")        
        transformableNode = ringModelNode       
        if not transformNode or not transformableNode:
            slicer.util.errorDisplay("Transform node or transformable node not found!")
            return
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID())        
        transformMatrix = vtk.vtkMatrix4x4()
        transformNode.GetMatrixTransformToParent(transformMatrix)
        transformMatrix.SetElement(2, 3,-12)
        transformNode.SetMatrixTransformToParent(transformMatrix)

        helper.FilterTreeItems()         

    elif selected_jaw == 'Upper' and selected_implant_system=='MIS_7 Implant System' and selected_implant== '5/10':
                                             
        angle, model = helper.createCenteredSolidTaperedTube(D1=5, D2=4.5, length=10)
        ringmodel,outerBottom, outerTop,innerBottom   = helper.createHollowTaperedTube(OD1=8.4, OD2=8.4, ID1=4.7, ID2=4.7, height=4, pointListNode=pointListNode)

        radius, height, resolution, model = helper.createimplantaxis(radius=0.5, height=50.0, resolution=60)
        radius, height, resolution, model = helper.createimplantcylinder(radius=2.5, height=10, resolution=60, pointListNode=pointListNode)

        node=slicer.util.getNode('CenteredCappedTaperedTube')
        node.SetName('5/10_UpperImpl')
        node2=slicer.util.getNode('HollowTaperedTube')
        node2.SetName('5/10_UpperGuideRing')
        node3=slicer.util.getNode('Implant Axis')
        node3.SetName('5/10_UpperImplAxis')
        node4=slicer.util.getNode('Implant Cylinder')
        node4.SetName('5/10_UpperImplCylinder') 

        transformNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode= slicer.util.getNode('5/10_UpperImpl')
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID()) 
        transformableNode2= slicer.util.getNode('5/10_UpperImplAxis')
        transformableNode2.SetAndObserveTransformNodeID(transformNode.GetID())            
        transformNode2 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode3= slicer.util.getNode('5/10_UpperGuideRing')
        transformableNode3.SetAndObserveTransformNodeID(transformNode2.GetID())            
        transformNode3 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode4= slicer.util.getNode('5/10_UpperImplCylinder')
        transformableNode4.SetAndObserveTransformNodeID(transformNode3.GetID())
        transformNode4 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode2.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode3.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())

        sourceModel = slicer.util.getNode('5/10_UpperImplCylinder')
        for modelNode in slicer.util.getNodesByClass("vtkMRMLModelNode"):
            name = modelNode.GetName()
            if name == ui.locationcomboBox.currentText:
                targetModel=modelNode  
        sourceToTargetTransform = slicer.util.getNode(transformNode4.GetName())

        import ModelRegistration
        mrLogic = ModelRegistration.ModelRegistrationLogic()
        mrLogic.run(sourceModel, targetModel, sourceToTargetTransform)
        mrLogic.ComputeMeanDistance(sourceModel, targetModel, sourceToTargetTransform)
        node=slicer.util.getNode('5/10_UpperImpl')
        node.SetName((ui.locationcomboBox.currentText)+':'+ '5/10_Implant')            
        node2=slicer.util.getNode('5/10_UpperGuideRing')
        node2.SetName((ui.locationcomboBox.currentText)+':'+ '5/10_GuideRing')            
        node3=slicer.util.getNode('5/10_UpperImplAxis')
        node3.SetName((ui.locationcomboBox.currentText)+':'+'5/10_ImplAxis')            
        node5=slicer.util.getNode(transformNode4.GetName())
        node5.SetName((ui.locationcomboBox.currentText)+':'+'5/10_UnitTransformInteraction')            
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())
        node6=slicer.util.getNode(transformNodeF.GetName())
        node6.SetName((ui.locationcomboBox.currentText)+':'+'5/10_TransformUnit')

        ringModelNode = slicer.util.getNode((ui.locationcomboBox.currentText)+':'+ '5/10_GuideRing')        
        transformNodeID = ringModelNode.GetTransformNodeID()        
        transformNode = slicer.mrmlScene.GetNodeByID(transformNodeID)        
        transformNode.SetName((ui.locationcomboBox.currentText)+':'+"RingTransform")        
        transformableNode = ringModelNode       
        if not transformNode or not transformableNode:
            slicer.util.errorDisplay("Transform node or transformable node not found!")
            return
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID())        
        transformMatrix = vtk.vtkMatrix4x4()
        transformNode.GetMatrixTransformToParent(transformMatrix)
        transformMatrix.SetElement(2, 3,-13)
        transformNode.SetMatrixTransformToParent(transformMatrix)
         
        helper.FilterTreeItems()

    


    elif selected_jaw == 'Upper' and selected_implant_system=='MIS_7 Implant System' and selected_implant== '5/11.5':
                                 
        angle, model = helper.createCenteredSolidTaperedTube(D1=5, D2=4.5, length=11.5)
        ringmodel,outerBottom, outerTop,innerBottom   = helper.createHollowTaperedTube(OD1=8.4, OD2=8.4, ID1=4.7, ID2=4.7, height=4, pointListNode=pointListNode)

        radius, height, resolution, model = helper.createimplantaxis(radius=0.5, height=50.0, resolution=60)
        radius, height, resolution, model = helper.createimplantcylinder(radius=2.5, height=11.5, resolution=60, pointListNode=pointListNode)

        node=slicer.util.getNode('CenteredCappedTaperedTube')
        node.SetName('5/11.5_UpperImpl')
        node2=slicer.util.getNode('HollowTaperedTube')
        node2.SetName('5/11.5_UpperGuideRing')
        node3=slicer.util.getNode('Implant Axis')
        node3.SetName('5/11.5_UpperImplAxis')
        node4=slicer.util.getNode('Implant Cylinder')
        node4.SetName('5/11.5_UpperImplCylinder') 

        transformNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode= slicer.util.getNode('5/11.5_UpperImpl')
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID()) 
        transformableNode2= slicer.util.getNode('5/11.5_UpperImplAxis')
        transformableNode2.SetAndObserveTransformNodeID(transformNode.GetID())            
        transformNode2 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode3= slicer.util.getNode('5/11.5_UpperGuideRing')
        transformableNode3.SetAndObserveTransformNodeID(transformNode2.GetID())            
        transformNode3 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode4= slicer.util.getNode('5/11.5_UpperImplCylinder')
        transformableNode4.SetAndObserveTransformNodeID(transformNode3.GetID())
        transformNode4 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode2.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode3.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())

        sourceModel = slicer.util.getNode('5/11.5_UpperImplCylinder')
        for modelNode in slicer.util.getNodesByClass("vtkMRMLModelNode"):
            name = modelNode.GetName()
            if name == ui.locationcomboBox.currentText:
                targetModel=modelNode  
        sourceToTargetTransform = slicer.util.getNode(transformNode4.GetName())

        import ModelRegistration
        mrLogic = ModelRegistration.ModelRegistrationLogic()
        mrLogic.run(sourceModel, targetModel, sourceToTargetTransform)
        mrLogic.ComputeMeanDistance(sourceModel, targetModel, sourceToTargetTransform)
        node=slicer.util.getNode('5/11.5_UpperImpl')
        node.SetName((ui.locationcomboBox.currentText)+':'+ '5/11.5_Implant')            
        node2=slicer.util.getNode('5/11.5_UpperGuideRing')
        node2.SetName((ui.locationcomboBox.currentText)+':'+ '5/11.5_GuideRing')            
        node3=slicer.util.getNode('5/11.5_UpperImplAxis')
        node3.SetName((ui.locationcomboBox.currentText)+':'+'5/11.5_ImplAxis')            
        node5=slicer.util.getNode(transformNode4.GetName())
        node5.SetName((ui.locationcomboBox.currentText)+':'+'5/11.5_UnitTransformInteraction')            
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())
        node6=slicer.util.getNode(transformNodeF.GetName())
        node6.SetName((ui.locationcomboBox.currentText)+':'+'5/11.5_TransformUnit')

        ringModelNode = slicer.util.getNode((ui.locationcomboBox.currentText)+':'+ '5/11.5_GuideRing')        
        transformNodeID = ringModelNode.GetTransformNodeID()        
        transformNode = slicer.mrmlScene.GetNodeByID(transformNodeID)        
        transformNode.SetName((ui.locationcomboBox.currentText)+':'+"RingTransform")        
        transformableNode = ringModelNode       
        if not transformNode or not transformableNode:
            slicer.util.errorDisplay("Transform node or transformable node not found!")
            return
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID())        
        transformMatrix = vtk.vtkMatrix4x4()
        transformNode.GetMatrixTransformToParent(transformMatrix)
        transformMatrix.SetElement(2, 3,-13.75)
        transformNode.SetMatrixTransformToParent(transformMatrix)
         
        helper.FilterTreeItems()


    elif selected_jaw == 'Upper' and selected_implant_system=='MIS_7 Implant System' and selected_implant== '5/13':
                                 
        angle, model = helper.createCenteredSolidTaperedTube(D1=5, D2=4.5, length=13)
        ringmodel,outerBottom, outerTop,innerBottom   = helper.createHollowTaperedTube(OD1=8.4, OD2=8.4, ID1=4.7, ID2=4.7, height=4, pointListNode=pointListNode)

        radius, height, resolution, model = helper.createimplantaxis(radius=0.5, height=50.0, resolution=60)
        radius, height, resolution, model = helper.createimplantcylinder(radius=2.5, height=13, resolution=60, pointListNode=pointListNode)

        node=slicer.util.getNode('CenteredCappedTaperedTube')
        node.SetName('5/13_UpperImpl')
        node2=slicer.util.getNode('HollowTaperedTube')
        node2.SetName('5/13_UpperGuideRing')
        node3=slicer.util.getNode('Implant Axis')
        node3.SetName('5/13_UpperImplAxis')
        node4=slicer.util.getNode('Implant Cylinder')
        node4.SetName('5/13_UpperImplCylinder') 

        transformNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode= slicer.util.getNode('5/13_UpperImpl')
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID()) 
        transformableNode2= slicer.util.getNode('5/13_UpperImplAxis')
        transformableNode2.SetAndObserveTransformNodeID(transformNode.GetID())            
        transformNode2 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode3= slicer.util.getNode('5/13_UpperGuideRing')
        transformableNode3.SetAndObserveTransformNodeID(transformNode2.GetID())            
        transformNode3 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode4= slicer.util.getNode('5/13_UpperImplCylinder')
        transformableNode4.SetAndObserveTransformNodeID(transformNode3.GetID())
        transformNode4 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode2.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode3.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())

        sourceModel = slicer.util.getNode('5/13_UpperImplCylinder')
        for modelNode in slicer.util.getNodesByClass("vtkMRMLModelNode"):
            name = modelNode.GetName()
            if name == ui.locationcomboBox.currentText:
                targetModel=modelNode  
        sourceToTargetTransform = slicer.util.getNode(transformNode4.GetName())

        import ModelRegistration
        mrLogic = ModelRegistration.ModelRegistrationLogic()
        mrLogic.run(sourceModel, targetModel, sourceToTargetTransform)
        mrLogic.ComputeMeanDistance(sourceModel, targetModel, sourceToTargetTransform)
        node=slicer.util.getNode('5/13_UpperImpl')
        node.SetName((ui.locationcomboBox.currentText)+':'+ '5/13_Implant')            
        node2=slicer.util.getNode('5/13_UpperGuideRing')
        node2.SetName((ui.locationcomboBox.currentText)+':'+ '5/13_GuideRing')            
        node3=slicer.util.getNode('5/13_UpperImplAxis')
        node3.SetName((ui.locationcomboBox.currentText)+':'+'5/13_ImplAxis')            
        node5=slicer.util.getNode(transformNode4.GetName())
        node5.SetName((ui.locationcomboBox.currentText)+':'+'5/13_UnitTransformInteraction')            
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())
        node6=slicer.util.getNode(transformNodeF.GetName())
        node6.SetName((ui.locationcomboBox.currentText)+':'+'5/13_TransformUnit')

        ringModelNode = slicer.util.getNode((ui.locationcomboBox.currentText)+':'+ '5/13_GuideRing')        
        transformNodeID = ringModelNode.GetTransformNodeID()        
        transformNode = slicer.mrmlScene.GetNodeByID(transformNodeID)        
        transformNode.SetName((ui.locationcomboBox.currentText)+':'+"RingTransform")        
        transformableNode = ringModelNode       
        if not transformNode or not transformableNode:
            slicer.util.errorDisplay("Transform node or transformable node not found!")
            return
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID())        
        transformMatrix = vtk.vtkMatrix4x4()
        transformNode.GetMatrixTransformToParent(transformMatrix)
        transformMatrix.SetElement(2, 3,-14.5)
        transformNode.SetMatrixTransformToParent(transformMatrix)
         
        helper.FilterTreeItems()


    elif selected_jaw == 'Upper' and selected_implant_system=='MIS_7 Implant System' and selected_implant== '5/16':
                                 
        angle, model = helper.createCenteredSolidTaperedTube(D1=5, D2=4.5, length=16)
        ringmodel,outerBottom, outerTop,innerBottom   = helper.createHollowTaperedTube(OD1=8.4, OD2=8.4, ID1=4.7, ID2=4.7, height=4, pointListNode=pointListNode)

        radius, height, resolution, model = helper.createimplantaxis(radius=0.5, height=50.0, resolution=60)
        radius, height, resolution, model = helper.createimplantcylinder(radius=2.5, height=16, resolution=60, pointListNode=pointListNode)

        node=slicer.util.getNode('CenteredCappedTaperedTube')
        node.SetName('5/16_UpperImpl')
        node2=slicer.util.getNode('HollowTaperedTube')
        node2.SetName('5/16_UpperGuideRing')
        node3=slicer.util.getNode('Implant Axis')
        node3.SetName('5/16_UpperImplAxis')
        node4=slicer.util.getNode('Implant Cylinder')
        node4.SetName('5/16_UpperImplCylinder') 

        transformNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode= slicer.util.getNode('5/16_UpperImpl')
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID()) 
        transformableNode2= slicer.util.getNode('5/16_UpperImplAxis')
        transformableNode2.SetAndObserveTransformNodeID(transformNode.GetID())            
        transformNode2 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode3= slicer.util.getNode('5/16_UpperGuideRing')
        transformableNode3.SetAndObserveTransformNodeID(transformNode2.GetID())            
        transformNode3 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode4= slicer.util.getNode('5/16_UpperImplCylinder')
        transformableNode4.SetAndObserveTransformNodeID(transformNode3.GetID())
        transformNode4 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode2.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode3.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())

        sourceModel = slicer.util.getNode('5/16_UpperImplCylinder')
        for modelNode in slicer.util.getNodesByClass("vtkMRMLModelNode"):
            name = modelNode.GetName()
            if name == ui.locationcomboBox.currentText:
                targetModel=modelNode  
        sourceToTargetTransform = slicer.util.getNode(transformNode4.GetName())

        import ModelRegistration
        mrLogic = ModelRegistration.ModelRegistrationLogic()
        mrLogic.run(sourceModel, targetModel, sourceToTargetTransform)
        mrLogic.ComputeMeanDistance(sourceModel, targetModel, sourceToTargetTransform)
        node=slicer.util.getNode('5/16_UpperImpl')
        node.SetName((ui.locationcomboBox.currentText)+':'+ '5/16_Implant')            
        node2=slicer.util.getNode('5/16_UpperGuideRing')
        node2.SetName((ui.locationcomboBox.currentText)+':'+ '5/16_GuideRing')            
        node3=slicer.util.getNode('5/16_UpperImplAxis')
        node3.SetName((ui.locationcomboBox.currentText)+':'+'5/16_ImplAxis')            
        node5=slicer.util.getNode(transformNode4.GetName())
        node5.SetName((ui.locationcomboBox.currentText)+':'+'5/16_UnitTransformInteraction')            
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())
        node6=slicer.util.getNode(transformNodeF.GetName())
        node6.SetName((ui.locationcomboBox.currentText)+':'+'5/16_TransformUnit')

        ringModelNode = slicer.util.getNode((ui.locationcomboBox.currentText)+':'+ '5/16_GuideRing')        
        transformNodeID = ringModelNode.GetTransformNodeID()        
        transformNode = slicer.mrmlScene.GetNodeByID(transformNodeID)        
        transformNode.SetName((ui.locationcomboBox.currentText)+':'+"RingTransform")        
        transformableNode = ringModelNode       
        if not transformNode or not transformableNode:
            slicer.util.errorDisplay("Transform node or transformable node not found!")
            return
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID())        
        transformMatrix = vtk.vtkMatrix4x4()
        transformNode.GetMatrixTransformToParent(transformMatrix)
        transformMatrix.SetElement(2, 3,-16)
        transformNode.SetMatrixTransformToParent(transformMatrix)
         
        helper.FilterTreeItems()


    elif selected_jaw == 'Upper' and selected_implant_system=='MIS_7 Implant System' and selected_implant== '6/6':
                                             
        angle, model = helper.createCenteredSolidTaperedTube(D1=6, D2=5.5, length=6)
        ringmodel,outerBottom, outerTop,innerBottom   = helper.createHollowTaperedTube(OD1=8.4, OD2=8.4, ID1=4.7, ID2=4.7, height=4, pointListNode=pointListNode)

        radius, height, resolution, model = helper.createimplantaxis(radius=0.5, height=50.0, resolution=60)
        radius, height, resolution, model = helper.createimplantcylinder(radius=3, height=6, resolution=60, pointListNode=pointListNode)

        node=slicer.util.getNode('CenteredCappedTaperedTube')
        node.SetName('6/6_UpperImpl')
        node2=slicer.util.getNode('HollowTaperedTube')
        node2.SetName('6/6_UpperGuideRing')
        node3=slicer.util.getNode('Implant Axis')
        node3.SetName('6/6_UpperImplAxis')
        node4=slicer.util.getNode('Implant Cylinder')
        node4.SetName('6/6_UpperImplCylinder') 

        transformNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode= slicer.util.getNode('6/6_UpperImpl')
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID()) 
        transformableNode2= slicer.util.getNode('6/6_UpperImplAxis')
        transformableNode2.SetAndObserveTransformNodeID(transformNode.GetID())            
        transformNode2 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode3= slicer.util.getNode('6/6_UpperGuideRing')
        transformableNode3.SetAndObserveTransformNodeID(transformNode2.GetID())            
        transformNode3 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode4= slicer.util.getNode('6/6_UpperImplCylinder')
        transformableNode4.SetAndObserveTransformNodeID(transformNode3.GetID())
        transformNode4 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode2.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode3.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())

        sourceModel = slicer.util.getNode('6/6_UpperImplCylinder')
        for modelNode in slicer.util.getNodesByClass("vtkMRMLModelNode"):
            name = modelNode.GetName()
            if name == ui.locationcomboBox.currentText:
                targetModel=modelNode  
        sourceToTargetTransform = slicer.util.getNode(transformNode4.GetName())

        import ModelRegistration
        mrLogic = ModelRegistration.ModelRegistrationLogic()
        mrLogic.run(sourceModel, targetModel, sourceToTargetTransform)
        mrLogic.ComputeMeanDistance(sourceModel, targetModel, sourceToTargetTransform)
        node=slicer.util.getNode('6/6_UpperImpl')
        node.SetName((ui.locationcomboBox.currentText)+':'+ '6/6_Implant')            
        node2=slicer.util.getNode('6/6_UpperGuideRing')
        node2.SetName((ui.locationcomboBox.currentText)+':'+ '6/6_GuideRing')            
        node3=slicer.util.getNode('6/6_UpperImplAxis')
        node3.SetName((ui.locationcomboBox.currentText)+':'+'6/6_ImplAxis')            
        node5=slicer.util.getNode(transformNode4.GetName())
        node5.SetName((ui.locationcomboBox.currentText)+':'+'6/6_UnitTransformInteraction')            
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())
        node6=slicer.util.getNode(transformNodeF.GetName())
        node6.SetName((ui.locationcomboBox.currentText)+':'+'6/6_TransformUnit')

        ringModelNode = slicer.util.getNode((ui.locationcomboBox.currentText)+':'+ '6/6_GuideRing')        
        transformNodeID = ringModelNode.GetTransformNodeID()        
        transformNode = slicer.mrmlScene.GetNodeByID(transformNodeID)        
        transformNode.SetName((ui.locationcomboBox.currentText)+':'+"RingTransform")        
        transformableNode = ringModelNode       
        if not transformNode or not transformableNode:
            slicer.util.errorDisplay("Transform node or transformable node not found!")
            return
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID())        
        transformMatrix = vtk.vtkMatrix4x4()
        transformNode.GetMatrixTransformToParent(transformMatrix)
        transformMatrix.SetElement(2, 3,-11)
        transformNode.SetMatrixTransformToParent(transformMatrix)
         
        helper.FilterTreeItems()



    elif selected_jaw == 'Upper' and selected_implant_system=='MIS_7 Implant System' and selected_implant== '6/8':
                                 
        angle, model = helper.createCenteredSolidTaperedTube(D1=6, D2=5.5, length=8)
        ringmodel,outerBottom, outerTop,innerBottom   = helper.createHollowTaperedTube(OD1=8.4, OD2=8.4, ID1=4.7, ID2=4.7, height=4, pointListNode=pointListNode)

        radius, height, resolution, model = helper.createimplantaxis(radius=0.5, height=50.0, resolution=60)
        radius, height, resolution, model = helper.createimplantcylinder(radius=3, height=8, resolution=60, pointListNode=pointListNode)

        node=slicer.util.getNode('CenteredCappedTaperedTube')
        node.SetName('6/8_UpperImpl')
        node2=slicer.util.getNode('HollowTaperedTube')
        node2.SetName('6/8_UpperGuideRing')
        node3=slicer.util.getNode('Implant Axis')
        node3.SetName('6/8_UpperImplAxis')
        node4=slicer.util.getNode('Implant Cylinder')
        node4.SetName('6/8_UpperImplCylinder') 

        transformNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode= slicer.util.getNode('6/8_UpperImpl')
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID()) 
        transformableNode2= slicer.util.getNode('6/8_UpperImplAxis')
        transformableNode2.SetAndObserveTransformNodeID(transformNode.GetID())            
        transformNode2 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode3= slicer.util.getNode('6/8_UpperGuideRing')
        transformableNode3.SetAndObserveTransformNodeID(transformNode2.GetID())            
        transformNode3 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode4= slicer.util.getNode('6/8_UpperImplCylinder')
        transformableNode4.SetAndObserveTransformNodeID(transformNode3.GetID())
        transformNode4 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode2.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode3.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())

        sourceModel = slicer.util.getNode('6/8_UpperImplCylinder')
        for modelNode in slicer.util.getNodesByClass("vtkMRMLModelNode"):
            name = modelNode.GetName()
            if name == ui.locationcomboBox.currentText:
                targetModel=modelNode  
        sourceToTargetTransform = slicer.util.getNode(transformNode4.GetName())

        import ModelRegistration
        mrLogic = ModelRegistration.ModelRegistrationLogic()
        mrLogic.run(sourceModel, targetModel, sourceToTargetTransform)
        mrLogic.ComputeMeanDistance(sourceModel, targetModel, sourceToTargetTransform)
        node=slicer.util.getNode('6/8_UpperImpl')
        node.SetName((ui.locationcomboBox.currentText)+':'+ '6/8_Implant')            
        node2=slicer.util.getNode('6/8_UpperGuideRing')
        node2.SetName((ui.locationcomboBox.currentText)+':'+ '6/8_GuideRing')            
        node3=slicer.util.getNode('6/8_UpperImplAxis')
        node3.SetName((ui.locationcomboBox.currentText)+':'+'6/8_ImplAxis')            
        node5=slicer.util.getNode(transformNode4.GetName())
        node5.SetName((ui.locationcomboBox.currentText)+':'+'6/8_UnitTransformInteraction')            
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())
        node6=slicer.util.getNode(transformNodeF.GetName())
        node6.SetName((ui.locationcomboBox.currentText)+':'+'6/8_TransformUnit')

        ringModelNode = slicer.util.getNode((ui.locationcomboBox.currentText)+':'+ '6/8_GuideRing')        
        transformNodeID = ringModelNode.GetTransformNodeID()        
        transformNode = slicer.mrmlScene.GetNodeByID(transformNodeID)        
        transformNode.SetName((ui.locationcomboBox.currentText)+':'+"RingTransform")        
        transformableNode = ringModelNode       
        if not transformNode or not transformableNode:
            slicer.util.errorDisplay("Transform node or transformable node not found!")
            return
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID())        
        transformMatrix = vtk.vtkMatrix4x4()
        transformNode.GetMatrixTransformToParent(transformMatrix)
        transformMatrix.SetElement(2, 3,-12)
        transformNode.SetMatrixTransformToParent(transformMatrix)
         
        helper.FilterTreeItems()


    elif selected_jaw == 'Upper' and selected_implant_system=='MIS_7 Implant System' and selected_implant== '6/10':
                                 
        angle, model = helper.createCenteredSolidTaperedTube(D1=6, D2=5.5, length=10)
        ringmodel,outerBottom, outerTop,innerBottom   = helper.createHollowTaperedTube(OD1=8.4, OD2=8.4, ID1=4.7, ID2=4.7, height=4, pointListNode=pointListNode)

        radius, height, resolution, model = helper.createimplantaxis(radius=0.5, height=50.0, resolution=60)
        radius, height, resolution, model = helper.createimplantcylinder(radius=3, height=10, resolution=60, pointListNode=pointListNode)

        node=slicer.util.getNode('CenteredCappedTaperedTube')
        node.SetName('6/10_UpperImpl')
        node2=slicer.util.getNode('HollowTaperedTube')
        node2.SetName('6/10_UpperGuideRing')
        node3=slicer.util.getNode('Implant Axis')
        node3.SetName('6/10_UpperImplAxis')
        node4=slicer.util.getNode('Implant Cylinder')
        node4.SetName('6/10_UpperImplCylinder') 

        transformNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode= slicer.util.getNode('6/10_UpperImpl')
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID()) 
        transformableNode2= slicer.util.getNode('6/10_UpperImplAxis')
        transformableNode2.SetAndObserveTransformNodeID(transformNode.GetID())            
        transformNode2 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode3= slicer.util.getNode('6/10_UpperGuideRing')
        transformableNode3.SetAndObserveTransformNodeID(transformNode2.GetID())            
        transformNode3 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode4= slicer.util.getNode('6/10_UpperImplCylinder')
        transformableNode4.SetAndObserveTransformNodeID(transformNode3.GetID())
        transformNode4 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode2.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode3.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())

        sourceModel = slicer.util.getNode('6/10_UpperImplCylinder')
        for modelNode in slicer.util.getNodesByClass("vtkMRMLModelNode"):
            name = modelNode.GetName()
            if name == ui.locationcomboBox.currentText:
                targetModel=modelNode  
        sourceToTargetTransform = slicer.util.getNode(transformNode4.GetName())

        import ModelRegistration
        mrLogic = ModelRegistration.ModelRegistrationLogic()
        mrLogic.run(sourceModel, targetModel, sourceToTargetTransform)
        mrLogic.ComputeMeanDistance(sourceModel, targetModel, sourceToTargetTransform)
        node=slicer.util.getNode('6/10_UpperImpl')
        node.SetName((ui.locationcomboBox.currentText)+':'+ '6/10_Implant')            
        node2=slicer.util.getNode('6/10_UpperGuideRing')
        node2.SetName((ui.locationcomboBox.currentText)+':'+ '6/10_GuideRing')            
        node3=slicer.util.getNode('6/10_UpperImplAxis')
        node3.SetName((ui.locationcomboBox.currentText)+':'+'6/10_ImplAxis')            
        node5=slicer.util.getNode(transformNode4.GetName())
        node5.SetName((ui.locationcomboBox.currentText)+':'+'6/10_UnitTransformInteraction')            
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())
        node6=slicer.util.getNode(transformNodeF.GetName())
        node6.SetName((ui.locationcomboBox.currentText)+':'+'6/10_TransformUnit')

        ringModelNode = slicer.util.getNode((ui.locationcomboBox.currentText)+':'+ '6/10_GuideRing')        
        transformNodeID = ringModelNode.GetTransformNodeID()        
        transformNode = slicer.mrmlScene.GetNodeByID(transformNodeID)        
        transformNode.SetName((ui.locationcomboBox.currentText)+':'+"RingTransform")        
        transformableNode = ringModelNode       
        if not transformNode or not transformableNode:
            slicer.util.errorDisplay("Transform node or transformable node not found!")
            return
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID())        
        transformMatrix = vtk.vtkMatrix4x4()
        transformNode.GetMatrixTransformToParent(transformMatrix)
        transformMatrix.SetElement(2, 3,-13)
        transformNode.SetMatrixTransformToParent(transformMatrix)
         
        helper.FilterTreeItems()

    elif selected_jaw == 'Upper' and selected_implant_system=='MIS_7 Implant System' and selected_implant== '6/11.5':
                                             
        angle, model = helper.createCenteredSolidTaperedTube(D1=6, D2=5.5, length=11.5)
        ringmodel,outerBottom, outerTop,innerBottom   = helper.createHollowTaperedTube(OD1=8.4, OD2=8.4, ID1=4.7, ID2=4.7, height=4, pointListNode=pointListNode)

        radius, height, resolution, model = helper.createimplantaxis(radius=0.5, height=50.0, resolution=60)
        radius, height, resolution, model = helper.createimplantcylinder(radius=3, height=11.5, resolution=60, pointListNode=pointListNode)

        node=slicer.util.getNode('CenteredCappedTaperedTube')
        node.SetName('6/11.5_UpperImpl')
        node2=slicer.util.getNode('HollowTaperedTube')
        node2.SetName('6/11.5_UpperGuideRing')
        node3=slicer.util.getNode('Implant Axis')
        node3.SetName('6/11.5_UpperImplAxis')
        node4=slicer.util.getNode('Implant Cylinder')
        node4.SetName('6/11.5_UpperImplCylinder') 

        transformNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode= slicer.util.getNode('6/11.5_UpperImpl')
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID()) 
        transformableNode2= slicer.util.getNode('6/11.5_UpperImplAxis')
        transformableNode2.SetAndObserveTransformNodeID(transformNode.GetID())            
        transformNode2 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode3= slicer.util.getNode('6/11.5_UpperGuideRing')
        transformableNode3.SetAndObserveTransformNodeID(transformNode2.GetID())            
        transformNode3 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode4= slicer.util.getNode('6/11.5_UpperImplCylinder')
        transformableNode4.SetAndObserveTransformNodeID(transformNode3.GetID())
        transformNode4 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode2.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode3.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())

        sourceModel = slicer.util.getNode('6/11.5_UpperImplCylinder')
        for modelNode in slicer.util.getNodesByClass("vtkMRMLModelNode"):
            name = modelNode.GetName()
            if name == ui.locationcomboBox.currentText:
                targetModel=modelNode  
        sourceToTargetTransform = slicer.util.getNode(transformNode4.GetName())

        import ModelRegistration
        mrLogic = ModelRegistration.ModelRegistrationLogic()
        mrLogic.run(sourceModel, targetModel, sourceToTargetTransform)
        mrLogic.ComputeMeanDistance(sourceModel, targetModel, sourceToTargetTransform)
        node=slicer.util.getNode('6/11.5_UpperImpl')
        node.SetName((ui.locationcomboBox.currentText)+':'+ '6/11.5_Implant')            
        node2=slicer.util.getNode('6/11.5_UpperGuideRing')
        node2.SetName((ui.locationcomboBox.currentText)+':'+ '6/11.5_GuideRing')            
        node3=slicer.util.getNode('6/11.5_UpperImplAxis')
        node3.SetName((ui.locationcomboBox.currentText)+':'+'6/11.5_ImplAxis')            
        node5=slicer.util.getNode(transformNode4.GetName())
        node5.SetName((ui.locationcomboBox.currentText)+':'+'6/11.5_UnitTransformInteraction')            
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())
        node6=slicer.util.getNode(transformNodeF.GetName())
        node6.SetName((ui.locationcomboBox.currentText)+':'+'6/11.5_TransformUnit')

        ringModelNode = slicer.util.getNode((ui.locationcomboBox.currentText)+':'+ '6/11.5_GuideRing')        
        transformNodeID = ringModelNode.GetTransformNodeID()        
        transformNode = slicer.mrmlScene.GetNodeByID(transformNodeID)        
        transformNode.SetName((ui.locationcomboBox.currentText)+':'+"RingTransform")        
        transformableNode = ringModelNode       
        if not transformNode or not transformableNode:
            slicer.util.errorDisplay("Transform node or transformable node not found!")
            return
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID())        
        transformMatrix = vtk.vtkMatrix4x4()
        transformNode.GetMatrixTransformToParent(transformMatrix)
        transformMatrix.SetElement(2, 3,-13.75)
        transformNode.SetMatrixTransformToParent(transformMatrix)
         
        helper.FilterTreeItems()
    


    elif selected_jaw == 'Upper' and selected_implant_system=='MIS_7 Implant System' and selected_implant== '6/13':
                                 
        angle, model = helper.createCenteredSolidTaperedTube(D1=6, D2=5.5, length=13)
        ringmodel,outerBottom, outerTop,innerBottom   = helper.createHollowTaperedTube(OD1=8.4, OD2=8.4, ID1=4.7, ID2=4.7, height=4, pointListNode=pointListNode)

        radius, height, resolution, model = helper.createimplantaxis(radius=0.5, height=50.0, resolution=60)
        radius, height, resolution, model = helper.createimplantcylinder(radius=3, height=13, resolution=60, pointListNode=pointListNode)

        node=slicer.util.getNode('CenteredCappedTaperedTube')
        node.SetName('6/13_UpperImpl')
        node2=slicer.util.getNode('HollowTaperedTube')
        node2.SetName('6/13_UpperGuideRing')
        node3=slicer.util.getNode('Implant Axis')
        node3.SetName('6/13_UpperImplAxis')
        node4=slicer.util.getNode('Implant Cylinder')
        node4.SetName('6/13_UpperImplCylinder') 

        transformNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode= slicer.util.getNode('6/13_UpperImpl')
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID()) 
        transformableNode2= slicer.util.getNode('6/13_UpperImplAxis')
        transformableNode2.SetAndObserveTransformNodeID(transformNode.GetID())            
        transformNode2 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode3= slicer.util.getNode('6/13_UpperGuideRing')
        transformableNode3.SetAndObserveTransformNodeID(transformNode2.GetID())            
        transformNode3 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformableNode4= slicer.util.getNode('6/13_UpperImplCylinder')
        transformableNode4.SetAndObserveTransformNodeID(transformNode3.GetID())
        transformNode4 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode2.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNode3.SetAndObserveTransformNodeID(transformNode4.GetID())
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())

        sourceModel = slicer.util.getNode('6/13_UpperImplCylinder')
        for modelNode in slicer.util.getNodesByClass("vtkMRMLModelNode"):
            name = modelNode.GetName()
            if name == ui.locationcomboBox.currentText:
                targetModel=modelNode  
        sourceToTargetTransform = slicer.util.getNode(transformNode4.GetName())

        import ModelRegistration
        mrLogic = ModelRegistration.ModelRegistrationLogic()
        mrLogic.run(sourceModel, targetModel, sourceToTargetTransform)
        mrLogic.ComputeMeanDistance(sourceModel, targetModel, sourceToTargetTransform)
        node=slicer.util.getNode('6/13_UpperImpl')
        node.SetName((ui.locationcomboBox.currentText)+':'+ '6/13_Implant')            
        node2=slicer.util.getNode('6/13_UpperGuideRing')
        node2.SetName((ui.locationcomboBox.currentText)+':'+ '6/13_GuideRing')            
        node3=slicer.util.getNode('6/13_UpperImplAxis')
        node3.SetName((ui.locationcomboBox.currentText)+':'+'6/13_ImplAxis')            
        node5=slicer.util.getNode(transformNode4.GetName())
        node5.SetName((ui.locationcomboBox.currentText)+':'+'6/13_UnitTransformInteraction')            
        transformNodeF = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode")
        transformNode4.SetAndObserveTransformNodeID(transformNodeF.GetID())
        node6=slicer.util.getNode(transformNodeF.GetName())
        node6.SetName((ui.locationcomboBox.currentText)+':'+'6/13_TransformUnit')

        ringModelNode = slicer.util.getNode((ui.locationcomboBox.currentText)+':'+ '6/13_GuideRing')        
        transformNodeID = ringModelNode.GetTransformNodeID()        
        transformNode = slicer.mrmlScene.GetNodeByID(transformNodeID)        
        transformNode.SetName((ui.locationcomboBox.currentText)+':'+"RingTransform")        
        transformableNode = ringModelNode       
        if not transformNode or not transformableNode:
            slicer.util.errorDisplay("Transform node or transformable node not found!")
            return
        transformableNode.SetAndObserveTransformNodeID(transformNode.GetID())        
        transformMatrix = vtk.vtkMatrix4x4()
        transformNode.GetMatrixTransformToParent(transformMatrix)
        transformMatrix.SetElement(2, 3,-14.5)
        transformNode.SetMatrixTransformToParent(transformMatrix)
         
        helper.FilterTreeItems()



     
        
    else:
        slicer.util.infoDisplay(f"No matching implant defined for: {selected_jaw}, {selected_implant_system}, {selected_implant}") 




