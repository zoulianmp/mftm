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
from mphantom.api import MPhantom, MPhantomTreeView, MPhantomVisualView
    
    
    
class PhantomEditorView(HasTraits):
    """ A GUI For making a phantom.
    """

    name = 'PhantomEditorView'

    #The Phantom to be Visualization
    phantom = Instance(MPhantom)

    current_element = DelegatesTo('phantom')

 
    tree_panel  = Instance(MPhantomTreeView)
    
 
   
    def __init__(self,**traits): 
        super(PhantomEditorView, self).__init__(**traits)
        
        if self.tree_panel is None:
            self.tree_panel = MPhantomTreeView()
   
        if self.phantom is None:
            self.phantom = MPhantom()
        
    
        self.tree_panel.phantom = self.phantom
        
     
        
       
 
    def _phantom_changed(self,new):
       
        
        if self.tree_panel is None:
            self.tree_panel = MPhantomTreeView()
        
     
       
        self.tree_panel.phantom = self.phantom
        
 
    def update_editor_view(self):
      
        self.tree_panel.selected = self.phantom.current_element
        
 
 
 
 
 
 
 

    view = View(        
                 VGroup(
                        Item(name='tree_panel',
                             editor = InstanceEditor(),
                             style ='custom',
                             show_label = False,
                             height=0.2,
                         #    width =400,                                        
                             resizable = True),
                        Item(name='current_element',
                             editor = InstanceEditor(),
                             style ='custom',   
                             show_label = False,
                             height=0.6,
                          #   width =400,
                             resizable = True),
                        
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
    
   
    GUI =  PhantomEditorView(phantom = phantom)
    print GUI.current_element
   
    GUI.configure_traits()
    
    phantom.name = "alktjlk"
    
    GUI.configure_traits()
    
 
