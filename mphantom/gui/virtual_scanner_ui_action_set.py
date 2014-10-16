# -*- coding: utf-8 -*-
"""
Created on Tue Nov 01 17:09:16 2011

@author: ZouLian
@Oncology Department
@Sichuan People's Hospital
@Chengdu,Sichuan,China
"""
# Enthought library imports.
from envisage.ui.action.api import Action, Group, Menu, ToolBar
from envisage.ui.workbench.api import WorkbenchActionSet



class VirtualScannerUIActionSet(WorkbenchActionSet):
    
    id = 'mphantom.ui.virtualscanner'
    
    #####################################################
    #Groups
    #####################################################
    
    
         
    #####################################################
    # Menus
    
    
     
        
    ###################################################
    # Tool Bars
    
        
        
        
        
    ######################################################
    # Actions
    ID = 'mphantom.api'
    
    tb_modeling_task = Action(
       id = "modelingtask",
       class_name = ID +".ModelingTaskAction",
       path = "ToolBar/Modeling")
    
   
       
#       
#    start_scan  = Action(
#       id = "StartScan",
#       class_name = ID +".magical_phantom_actions.VirtualScanAction",
#       name = "Start Scan",
#       group = "VirtualScanGroup",
#       path = "MenuBar/VirtualScan")
#       
#       
#    export_dicom  = Action(
#       id = "ExportDicom",
#       class_name = ID +".magical_phantom_actions.ExportDicomAction",
#       name = "Export Dicom",
#       group = "VirtualScanGroup",
#       path = "MenuBar/VirtualScan")
#       

    
            
    actions = [
               tb_modeling_task,
#               start_scan,
#               export_dicom,
              ]
             
    tool_bars = [ 
                 ToolBar(name='Modeling')
               ]
   
    
    #### 'WorkbenchActionSet' interface #######################################

    # The Ids of the perspectives that the action set is enabled in.
    enabled_for_perspectives = ['VirtualScan']

    # The Ids of the perspectives that the action set is visible in.
    visible_for_perspectives = ['PhantomConfig','VirtualScan']

       
       