# -*- coding: utf-8 -*-
"""
Created on Tue Nov 01 17:09:16 2011

@author: ZouLian
@Oncology Department
@Sichuan People's Hospital
@Chengdu,Sichuan,China
"""

# Enthought library imports.

from traits.api import HasTraits, Instance, DelegatesTo
from traitsui.api import Item, View,InstanceEditor,VGroup,HGroup,HSplit,Spring,Label,UItem

# Local imports.
from mphantom.api import MPhantom,PhantomEditorView, MPhantomVisualView
    
    
    
class PhantomFactoryGUI(HasTraits):
    """ A GUI For making a phantom.
    """

    name = 'PhantomFactoryGUI'

    #The Phantom to be Visualization
    phantom = Instance(MPhantom)

    current_element = DelegatesTo('phantom')

 
    lef_panel  = Instance(PhantomEditorView)
    
    right_panel = Instance(MPhantomVisualView)

 
   
    def __init__(self,**traits): 
        super(PhantomFactoryGUI, self).__init__(**traits)
        
        if self.lef_panel is None:
            self.lef_panel = PhantomEditorView()
        
        if self.right_panel is None:
            self.right_panel = MPhantomVisualView()
        
        if self.phantom is None:
            self.phantom = MPhantom()
        
        self.lef_panel.phantom = self.phantom
        self.right_panel.phantom = self.phantom
        
        
        
        self.phantom.on_trait_event(self.update_gui,'updated')
        self.phantom.on_trait_event(self.update_gui,'vis_props_changed')
       
 
    def _phantom_changed(self,new):
        
        
        if self.lef_panel is None:
            self.lef_panel = PhantomEditorView()
        
        if self.right_panel is None:
            self.right_panel = MPhantomVisualView()
        
       
        self.lef_panel.phantom = self.phantom
        self.right_panel.phantom = self.phantom
        
 
 
    def update_gui(self):
        
        
        self.lef_panel.update_editor_view()
        self.right_panel.update_visualization()
        
 
 

    view = View(  HGroup(        
                
                        Item(name='lef_panel',
                             editor = InstanceEditor(),
                             style ='custom',   
                             show_label = False,
                             width =0.27,
                             resizable = True),
                        
                             
                  
                       Item(name='right_panel',
                           editor = InstanceEditor(),
                           style ='custom',
                           show_label = False,
                           width =0.73,
                           resizable = True )
                  
                         )
                )
    
    
    
    
   
        
        
        

   
   
 ####################################

if __name__ == '__main__':
    
    from mphantom.api import CubeGeometry,ConeGeometry,STLFileGeometry, \
                                   ThreeDimensionElement
    cube = CubeGeometry()
   # cube.configure_traits()
    
    cone = ConeGeometry()
   # cone.configure_traits()
    
    cube_element = ThreeDimensionElement()
    cube_element.geometry = cube
   # cube_element.name = "Cube"
    #cube_element.configure_traits()
    
    
    cone_element = ThreeDimensionElement()
    cone_element.geometry = cone
    cone_element.name = "Cone"
    
    phantom = MPhantom()
    
    
    phantom.add_3d_element(cube_element)
    phantom.add_3d_element(cone_element)
    
   
    GUI =  PhantomFactoryGUI(phantom = phantom)
    print GUI.current_element
   
    GUI.configure_traits()
    
    phantom.name = "alktjlk"
    
    GUI.configure_traits()
    
 
