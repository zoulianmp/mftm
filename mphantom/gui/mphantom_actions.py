# -*- coding: utf-8 -*-
"""
Created on Tue Nov 08 08:48:11 2011

@author: IMRTQA
"""
from traits.api import Str, HasTraits
from pyface.action.api import Action

from traitsui.api import View, Item, Spring, Group
from traitsui.menu import OKCancelButtons

from os.path import isfile
from mayavi.core.common import error


from pyface.api import  ImageResource


from pyface.api import FileDialog, OK
#from envisage.ui.action.api import Action, ActionSet,Group,Menu

from mphantom.api import MPhantom

from mphantom.api import RunManager, Add3DElementDialog,ThreeDimensionElement, \
                         ImageSetExporter, TestDialog

#from models.compound_element import CompoundElement


#####################################################
# Utility funcitons
#####################################################

#####################################################
# New Phantom Actions
#####################################################

class PhantomName ( HasTraits ):
    name  = Str("NewPhantom")
    
     # ct_scanner = BaseElement
    
     
    space =Group( Spring (),
                  Spring (),
                  Spring (),
                  Spring ())
      
      ######################
    view = View(  
                  Spring (),
                  Item(name ='name',
                       label='Enter the New Name',),
                  Item('_'),
               
                  Spring (),
                  Spring (),
                  
                
                  
                  space,
                  buttons = OKCancelButtons,
                  title = ' New Phantom ....',
                  height= 400,
                  width = 250,
                  kind = 'livemodal'
                  
                )










               
#####################################################
# Task Switch Actions
#####################################################        

 
class StartupTaskAction(Action):
    """ An Action that Switch the perspective to the 3D Modeling perspective
    """
    tooltip = "Switch to startup page"
    description = "Switch to startup page"
    
    # The action's image (displayed on tool bar tools etc).
    image = ImageResource('startup.ico')
        
    #####################################################
    # 'Action ' Interface
    #####################################################
    def perform(self,event):
        
        self.window.active_perspective = self.window.perspectives[0]
      
        
 
 
 
 
class ModelingTaskAction(Action):
    """ An Action that Switch the perspective to the 3D Modeling perspective
    """
    tooltip = "Switch to 3D Modeling Task"
    description = "Switch to 3D Modeling Task,by switch to the phantom configuration"
    
    # The action's image (displayed on tool bar tools etc).
    image = ImageResource('modeling.ico')
        
    #####################################################
    # 'Action ' Interface
    #####################################################
    def perform(self,event):
        
        self.window.active_perspective = self.window.perspectives[1]
      
        
         
        
       
class ScannerTaskAction(Action):
    """ An Action that Switch the perspective to the 3D Modeling perspective
    """
    tooltip = "Switch to Scanner Task"
    description = "Switch to Virtual CT Scanner Task,by switch to the virtual ct scanner perspective"
    
    # The action's image (displayed on tool bar tools etc).
    image = ImageResource('scanner.ico')
        
    #####################################################
    # 'Action ' Interface
    #####################################################
    def perform(self,event):
        self.window.active_perspective = self.window.perspectives[2]
      
        

















  
class NewPhantomAction(Action):
    
    name = '&NewPhantom'

    tooltip = "Create a new phantom"
    description =  "Create a new phantom,enter the modeling gui"
        
    # The action's image (displayed on tool bar tools etc).
    image = ImageResource('newphantom.ico')
    
    
    #####################################################
    # 'Action ' Interface
    #####################################################
    def perform(self,event):
        
        """Perform the New Phantom Action """        
         
        p = PhantomName()      
        ui = p.edit_traits()
         
        if ui.result:
              
          run_manager = self.window.application.get_service('mphantom.api.RunManager')
          phantom = run_manager.model
          phantom.name = p.name
          self.window.active_perspective = self.window.perspectives[1]
                       
        else:
             pass    
        
       
      
       

  
 
class LoadPhantomAction(Action):
    """ An Action that Load a phantom from file"""
    tooltip = "Load saved phantom"
    
    description = "Load saved phantom from a MagicalPhantom (*.mp) file"
    
    image = ImageResource('loadphantom.ico')
        
    #####################################################
    # 'Action ' Interface
    #####################################################
    def perform(self,event):
        """Perform the Save Phantom  Action """
        wildcard = 'MagicalPhantom files (*.mp)|*.mp|' + FileDialog.WILDCARD_ALL
        parent = self.window.control
        dialog = FileDialog(parent=parent,
                            title = 'Open MagicalPhantom file',
                            action = 'open',wildcard = wildcard)
        if dialog.open()==OK:
            if not isfile(dialog.path):
                error("File '%s' does not exist"%dialog.path,parent)
                return
       
        run_manager = self.window.application.get_service('mphantom.api.RunManager')
        
        phantom = run_manager.model
        
       
        
        print dialog.path
                
        phantom.clear_phantom()
        phantom.load_phantom(dialog.path)
        
       
        
        self.window.active_perspective = self.window.perspectives[1]
        
  
         
  

class SavePhantomAction(Action):
    """ An Action that saves the current phantom"""
    tooltip = "Save current phantom"
    
    description = "Save current phantom to a MagicalPhantom (*.mp) file"
    
      
    image = ImageResource('savephantom.ico')
    #####################################################
    # 'Action ' Interface
    #####################################################
    def perform(self,event):
        """Perform the Save Phantom  Action """
        wildcard = 'MagicalPhantom files (*.mp)|*.mp|' + FileDialog.WILDCARD_ALL
        dialog = FileDialog(parent=self.window.control,
                            title = 'Save MagicalPhantom file',
                            action = 'save as',wildcard = wildcard)
        if dialog.open()==OK:
             
            run_manager = self.window.application.get_service('mphantom.api.RunManager')
            currentphantom= run_manager.model
 
            currentphantom.save_phantom(dialog.path)
        
        
          
  
  

class RenamePhantomAction(Action):
    """ An Action that Creat a new phantom for configure"""
    
    name = '&Rename'
#    accelerator = 'Ctrl+r'

    tooltip = "Change current phantom's name"
    description =  "Change the name of  phantom which is in configuration"
    image = ImageResource('renamephantom.ico')  
        
    #####################################################
    # 'Action ' Interface
    #####################################################
    def perform(self,event):
        
        """Perform the New Phantom Action """
        
        p = PhantomName()
         
        ui = p.edit_traits()
         
        if ui.result:
          run_manager = self.window.application.get_service('mphantom.api.RunManager')
          phantom = run_manager.model
          
          phantom.name = p.name
          
              
        else:
             pass
              
           

#####################################################
# Add Buildin Single Element Actions
#####################################################

class Add3DElementAction(Action):
    """ Add a Single Element to Crruent phantom for configure"""
  
    
    name = '&Add3DElement'
 #   accelerator = 'Ctrl+s'    
    
     # The action's image (displayed on tool bar tools etc).
    image = ImageResource('add.ico')


    tooltip = "Add a 3D Element to Crruent phantom"
    description =  "Add a 3D Element to Crruent phantom"
   
     
        
    #####################################################
    # 'Action ' Interface
    #####################################################
    def perform(self,event):
        """Perform the Add a Single Element  Action """
        run_manager = self.window.application.get_service('mphantom.api.RunManager')
        
        currentphantom= run_manager.model
        
        dialog =  Add3DElementDialog()
        ui= dialog.edit_traits()
   
        if ui.result:
            
             currentphantom.add_3d_element(dialog.ele)
             
           
           
        else:
             return
        
               
        
        
         
#####################################################
# Delet Current Actions
#####################################################        
 
class DeletCurrentElementAction(Action):
    """ Add a Buildin Compound Element to Crruent phantom for configure"""
    
    name = '&DeletCurrentElement'
#    accelerator = 'Ctrl+d'        
    
    tooltip = " Delet the Current Element of Crruent phantom"
    description =  " Delet the Current Element of Crruent phantom"
   
    # The action's image (displayed on tool bar tools etc).
    image = ImageResource('remove.ico')
   
 
    
    #####################################################
    # 'Action ' Interface
    #####################################################
    def perform(self,event):
        """Perform the Add a Single Element  Action """
        run_manager = self.window.application.get_service('mphantom.api.RunManager')
        currentphantom= run_manager.model
   
      
        celement = currentphantom.current_element
       
        if isinstance(celement,ThreeDimensionElement):
            currentphantom.remove_3d_element(celement)
         
                   
            return
        
      
        
        
        


#####################################################
# Save  Current Phantom Actions
#####################################################        
 
  
#####################################################
# Save  Current Phantom Actions
#####################################################        

        
       
        