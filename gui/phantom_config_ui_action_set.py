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

class PhantomConfigUIActionSet(WorkbenchActionSet):
   
    #####################################################
    #Groups
    #####################################################
    
    id = 'mphantom.ui.phantomconfig'    
   
     
     
             
    
    #####################################################
    # Menus
    
            
    phantom_menu = Menu(
        id = "Phantom",
        name = "&Phantom",
        path = 'MenuBar',
        before = 'View'
        )
        
        
        
        
    element_menu = Menu(
        id = "Elements",
        name = "&Elements",
        path = 'MenuBar',
        before = 'View'
       )
        
        

        
    ######################################################
    # Actions
     
    ID = 'mphantom.api'   #used for construct actions class name 
    
    
    
    
#
#  
#    new_phantom = Action(
#       id = "NewPhantom",
#       class_name = ID +".NewPhantomAction",
#       name = "NewPhantom",
#       path = "MenuBar/Phantom")
#   
#    
#    tb_new_phantom = Action(
#       id = "NewPhantom",
#       class_name = ID +".NewPhantomAction",
#       path = "ToolBar/Phantom")
#   
    
    load_phantom = Action(
       id = "LoadPhantom",
       class_name = ID +".LoadPhantomAction",
       name = "LoadPhantom",
       path = "MenuBar/Phantom")
       
       
    tb_load_phantom = Action(
       id = "LoadPhantom",
       class_name = ID +".LoadPhantomAction",
       path = "ToolBar/Phantom")
    
    
    
   
        
    rename_phantom = Action(
       id = "RenamePhantom",
       class_name = ID +".RenamePhantomAction",
       name = "Rename Phantom",
       path = "MenuBar/Phantom")
       
    tb_rename_phantom = Action(
       id = "RenamePhantom",
       class_name = ID +".RenamePhantomAction",    
       path = "ToolBar/Phantom")
       
          
    save_phantom = Action(
       id = "SavePhantom",
       class_name = ID +".SavePhantomAction",
       name = "Save Phantom",
       path = "MenuBar/Phantom")
    
    tb_save_phantom = Action(
       id = "SavePhantom",
       class_name = ID +".SavePhantomAction",
       path = "ToolBar/Phantom")
    
    
    
    
    
    
    add_3delement = Action(
       id = "Add3DElement",
       class_name = ID +".Add3DElementAction",
       name = "Add3DElement",
   
       path = "MenuBar/Elements")
       
    tb_add_3dselement = Action(
       path = "ToolBar/Elements",
       id = "Add3DElement",
       class_name = ID +".Add3DElementAction",
       name = "AddSingleElement",
       )
  
       
       
       
    delet_current_element = Action(
       id = "DeletCurrentElement",
       class_name = ID +".DeletCurrentElementAction",
       name = "Delet CurrentElement",     
       path = "MenuBar/Elements")
       
        
    tb_delet_current_element = Action(
       id = "DeletCurrentElement",
       class_name = ID +".DeletCurrentElementAction",
       name = "Delet CurrentElement",   
       path = "ToolBar/Elements")
       
     
  
#  
#    tb_scanner_task = Action(
#       id = "scannertask",
#       class_name = ID +".ScannerTaskAction",
#       path = "ToolBar/Vscan")
#    
#
#
#

#    
#    groups = [phantom_group,
#              element_group            
#             ]
             
    menus = [
             phantom_menu,
             element_menu
      
            ]   
            
            
    actions = [
              # new_phantom,
               rename_phantom,
               load_phantom,
             
               save_phantom,
  
               add_3delement, 
               delet_current_element,
               
            #   tb_new_phantom,
               tb_rename_phantom,
               tb_load_phantom,
               
               tb_save_phantom, 
              
               tb_add_3dselement,
               tb_delet_current_element,
#                        
#               tb_scanner_task,
              ]
             
    

        
    tool_bars = [
                ToolBar(id='TasksBar'),
                ToolBar(id='Phantom'),
                ToolBar(id='Elements'),
                ToolBar(id='Vscan'),
                
               ]

    #### 'WorkbenchActionSet' interface #######################################

    # The Ids of the perspectives that the action set is enabled in.
    enabled_for_perspectives = ['PhantomConfig']

    # The Ids of the perspectives that the action set is visible in.
    visible_for_perspectives = ['Startup','PhantomConfig','VirtualScan']
       
       
       