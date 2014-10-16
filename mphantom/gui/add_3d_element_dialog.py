# -*- coding: utf-8 -*-
"""
Created on Thu Nov 03 10:58:57 2011

@author: ZouLian
@Oncology Department
@Sichuan People's Hospital
@Chengdu,Sichuan,China
"""

from traits.api import HasTraits, Instance, Enum, Dict,List,Str, DelegatesTo
from traitsui.api import View,Item,Spring,Group, UItem
from tvtk.pyface import actors
from tvtk.api import tvtk

from traitsui.menu import OKCancelButtons, ModalButtons 

#local import 
from mphantom.api import  BaseGeometry, ConeGeometry, CubeGeometry, CylinderGeometry, \
                          SphereGeometry, STLFileGeometry, VTKFileGeometry

from mphantom.api import ThreeDimensionElement           



             
######################################################################
class Add3DElementDialog(HasTraits):
    
     
      
      # Flag to set the poly data type.
      geo_type = Enum('Cone','Cube','Cylinder','Sphere',
                    'VTKExternalFile','STLExternalFile',
                     desc='which poly data source to be used')
      
      ele = Instance(ThreeDimensionElement)
      
      
      name = DelegatesTo('ele')
        
      current_geometry = Instance(BaseGeometry)
      
      # A dictionary that maps the source names to instances of the
      # Buildin Geometry
      _geometry_dict = Dict(Str,
                          Instance(HasTraits,
                                   allow_none=False))
         
      
     
      def __init__(self,**traits):
          super(Add3DElementDialog,self).__init__(**traits)
          
                  
          self.ele = ThreeDimensionElement()
     
          
          self.current_geometry = self._geometry_dict['Cone']
          self.current_geometry.current_actor.property.color = (0.00,0.00,0.00)          
          
          self.ele.geometry = self.current_geometry
        
     
                            
      ######################################################################
      # Non-public methods.
      ######################################################################
        
      def _geo_type_changed(self, value):
           """This method is invoked (automatically) when the `source`
           trait is changed.
           """
           self.current_geometry = self._geometry_dict[self.geo_type]
           self.current_geometry.current_actor.property.color = (0.00,0.00,0.00)
         
      def _current_geometry_changed(self, value):
           """This method is invoked (automatically) when the `source`
           trait is changed.
           """
           
           self.ele.geometry = self.current_geometry
        
   
        
        
      def __geometry_dict_default(self):
           """Default value for source dict."""
           sd = {'Cone':ConeGeometry(),
                 'Cube':CubeGeometry(),
                 'Cylinder':CylinderGeometry(),
                 'Sphere':SphereGeometry(),
                 'VTKExternalFile':VTKFileGeometry(),
                 'STLExternalFile':STLFileGeometry(),
                }
           return sd

        

      
      space =Group( Spring (),
                    Spring (),
                    Spring (),
                    Spring ())
      
      ######################
      view = View(Item(name='name',
                       label='Element Name'),
                  space,      
                  Item(name='geo_type',
                       label='Geometry Type:'
                             ),
                  space,
                  Group(
                        
                        UItem(name = 'current_geometry',
                              style = 'custom',
                              label = 'False',
                              resizable = False,),
                            #  height = 350,
                            #  width = 400,),
                        show_border = True,
                        label='Geometry Parameters',
                      
                       ),
                  
                  # buttons =ModalButtons,
                  buttons = OKCancelButtons,
                  close_result  = False,
                  title = 'Adding 3D Element',
                  height= 650,
                  width = 550,
                  resizable = True,
                  kind = 'livemodal'
                )



if __name__ == '__main__':
    a = Add3DElementDialog()
  
    a.configure_traits()
    
      
   