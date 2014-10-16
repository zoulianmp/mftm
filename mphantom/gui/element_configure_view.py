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
from traitsui.api import Item, View,InstanceEditor

# Local imports.
from mphantom.api import MPhantom

    
    
class ElementConfigureView(HasTraits):
    """ A simple dock pane for editing an attractor model's configuration
        options.
    """

    #### 'ITaskPane' interface ################################################

    id = 'magicphantom.element_config_pane'
    name = 'Element Parameters Configuration'

    #The Phantom to be Visualization
    phantom = Instance(MPhantom)

    current_element = DelegatesTo('phantom')



    traits_ui_view = View(Item(name='current_element',
                               editor = InstanceEditor(),
                          style ='custom',
                          show_label = False),
                          resizable = True,
                         # width = 350,
                          #height = 500
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
  #  cube_element.configure_traits()
    
    
    cone_element = ThreeDimensionElement()
    cone_element.geometry = cone
    cone_element.name = "Cone"
    
    phantom = MPhantom()
    
    
    phantom.add_3d_element(cube_element)
    phantom.add_3d_element(cone_element)
    
   
    GUI =  ElementConfigureView(phantom = phantom)
    print GUI.current_element
   
    GUI.configure_traits()
    
 
