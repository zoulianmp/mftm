# -*- coding: utf-8 -*-
"""
Created on Thu Nov 03 10:58:57 2011

@author: ZouLian
@Oncology Department
@Sichuan People's Hospital
@Chengdu,Sichuan,China
"""

from traits.api import HasTraits, Instance, Enum, Dict,List,Str
from traitsui.api import View,Item,Spring,Group, UItem
from tvtk.pyface import actors
from tvtk.api import tvtk

from traitsui.menu import OKCancelButtons

#local import 

from base_geometry import BaseGeometry
            
             
######################################################################
class BuildinSGeometry(BaseGeometry):
    
      geometry_name = Str('SingleGeometry')
      
      #This method is invoked (automatically) when the `source`
      #trait is changed.
      
      def _source_changed(self, value):
       
           super(BuildinSGeometry,self)._source_changed(value)
           self.geometry = [self._current_actor]
          
            


      
      space =Group( Spring (),
                    Spring (),
                    Spring (),
                    Spring ())
      
      ######################
      view = View(Item(name='geometry_name',
                       label='Geometry Name'),
                  space,      
                  Item(name='source',
                       label='Geometry Type:'
                             ),
                  
                  Group(
                        Item('_'),
                        UItem(name = 'current_source',
                              style = 'custom',
                              label = 'False',
                              resizable = False,),
                            #  height = 350,
                            #  width = 400,),
                        show_border = True,
                        label='Geometry Parameters',
                      
                       ),
                  
               
                  buttons = OKCancelButtons,
                  title = 'Adding SingleElement Geometry',
                  height= 650,
                  width = 550,
                  resizable = True
                  
                )



if __name__ == '__main__':
    a = BuildinSGeometry()
  
    a.configure_traits()
