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


from pyface.api import  ImageResource

class StartupUIActionSet(WorkbenchActionSet):
   
    #####################################################
    #Groups
    #####################################################
    
    id = 'mphantom.ui.startup'    
    

    #####################################################
    # Menus
    tasks_menu = Menu(
        id = "Tasks",
        name = "&Tasks",
        path = 'MenuBar',
        before = "View"   )
          

    
           
 
      
           
        
    ######################################################
    # Actions
     
    ID = 'mphantom.api'   #used for construct actions class name 
    
    

    
    
    
    startup_task = Action(
       id = "startuptask",
       class_name = ID +".StartupTaskAction",
       name = "Startup",
       path = "MenuBar/Tasks")
       
       
      
    tb_startup_task = Action(
       id = "startuptask",
       class_name = ID +".StartupTaskAction",
       name = "Startup",
       path = "ToolBar/TasksBar")
   

    phantom_task = Action(
       id = "phantomconfig",
       class_name = ID +".ModelingTaskAction",
       name = "PhantomConfig",
       path = "MenuBar/Tasks")  
       
    tb_phantom_task = Action(
       id = "phantomconfig",
       class_name = ID +".ModelingTaskAction",
       name = "PhantomConfig",
       path = "ToolBar/TasksBar")  
       
       
    scanning_task = Action(
       id = "NewPhantom",
       class_name = ID +".ScannerTaskAction",
       name = "CTScanner",
       path = "MenuBar/Tasks")
       
    tb_scanning_task = Action(
       id = "scanning",
       class_name = ID +".ScannerTaskAction",
       name = "CTScanner",
       path = "ToolBar/TasksBar")
       
       
 

  
  
            
    actions = [startup_task,
               phantom_task,            
               scanning_task,
               tb_startup_task,
               tb_phantom_task,
               tb_scanning_task
              ]
 
        
    tool_bars = [ 
          
                ToolBar(name='TasksBar'),
   
                ToolBar(name='phantom'),
                ToolBar(name='Elements'),
                ToolBar(name='Vscan'),
               
               ]

    #### 'WorkbenchActionSet' interface #######################################

    # The Ids of the perspectives that the action set is enabled in.
    enabled_for_perspectives = ['Startup','PhantomConfig','VirtualScan']
#    visible_for_perspectives =  ['Startup'] 
# 
       