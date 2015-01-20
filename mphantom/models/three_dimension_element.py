# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 14:37:11 2011

@author: ZouLian
@Oncology Department
@Sichuan People's Hospital
@Chengdu,Sichuan,China
"""

from traits.api import on_trait_change
from traitsui.api import View, Item,Tabbed


from mphantom.api import  Ele3DVisualProperty,Ele3DGeometryTuner,BaseElement



######################################################################
'''
A Based Class for Phantom Construction Element
'''

class ThreeDimensionElement(BaseElement):
    
      
    def __init__(self):
        super(ThreeDimensionElement, self).__init__()
      
        
        self.visual =  Ele3DVisualProperty()
        
        self.visual.add_actors( self.geometry.current_actor )
        
        self.geometry_tuner = Ele3DGeometryTuner()
        
        self.geometry_tuner.on_trait_change(self.render_transformed_actor,'geo_tuner_changed')
        self.visual.on_trait_event(self.turn_on_vis_changed,'vis_changed')
        self.general.on_trait_change(self.update_name,'name')
      
    def update_name(self):
        if self.helper is not None:
           self.helper.elements_name_modified =True
        
        
      
    def get_data_for_json(self):
        '''Get a dict data for json output '''
        data = {}
        
        data["EleName"] = self.name
        data["GeneralParams"] = self.general.get_data_for_json()
        data["GeoTunerParams"] = self.geometry_tuner.get_data_for_json()
        data["GeometryParams"] = self.geometry.get_data_for_json()
        data["VisParams"] = self.visual.get_data_for_json()
        
        return data
         
        
    
    def render_transformed_actor(self):
        tf = self.geometry_tuner.current_transform
        
        geo = self.geometry
        
        geo.current_transform = tf
        
        geo.current_actor.property.color = self.visual.color

        geo.current_actor.visibility = self.visual.visibility

        geo.current_actor.property.representation = self.visual.representation 
                          
        geo.current_actor.property.opacity = self.visual.opacity 
         
        self.visual.inner_actor = geo.current_actor
        
        if self.helper is not None:
            self.helper.phantom_modified =True
        
      
   
    def turn_on_vis_changed(self):
        if self.helper is not None:
            self.helper.phantom_modified =True
        
    
   
         
      
        
         ######################
    
    tab1 =  Item(name='general',
                 style='custom',
                 show_label = False,
                 resizable = True) 
                     
    tab2=  Item(name='visual',
                style='custom',
                show_label = False,
                resizable = True) 
                
    tab3=  Item(name='geometry_tuner',
                style='custom',
                show_label = False,
                resizable = True)
                
  
    
    view = View(Tabbed( tab1,
                        tab2,
                        tab3
                        ),
                resizable = True,
              #  width= 400
               )
    
    

if __name__ == '__main__':
    
    from mphantom.api import CubeGeometry,ConeGeometry,STLFileGeometry
    geo = CubeGeometry()
    cone = ConeGeometry()
    
    stl = STLFileGeometry()
    stl.configure_traits()    
    
    a = ThreeDimensionElement()
    a.geometry = geo    
    
    a.configure_traits()
