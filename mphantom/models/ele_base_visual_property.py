# -*- coding: utf-8 -*-
"""
Created on Mon Oct 07 11:26:21 2013

@author: ZouLian
@Joint Lab for Medical Physics
@Oncology Department
@Sichuan People's Hospital
@Chengdu,Sichuan,China

"""
from traits.api import HasTraits, Enum,Range,Bool, \
                       Instance,Tuple,on_trait_change,Event

from traitsui.api import View, Item,VGroup,Spring
from tvtk.api import tvtk
from vtk.util import colors

class EleBaseVisualProperty(HasTraits):
    '''A help Class for Phantom Element,this contains general properties.
    '''
     
    inner_actor = Instance( tvtk.Actor)
    
    color = Tuple(colors.black)
    
    visibility = Bool(True)

    representation = Enum( 
                          'surface',
                          'points',
                          'wireframe'
                          )
                          
    opacity = Range(low = 0.0, high = 1.0, value = 1.0, )
    
    
    vis_changed = Event
#    
#    def __color_default(self):
#        return Tuple((0.0,0.0,0.0))
                          
    def __init__(self,**traits):
        super(EleBaseVisualProperty,self).__init__(**traits)
        
        self.color = (0.0,0.0,0.0)
                          
     
    def add_actors(self, actors):
        
        pass
    
        
    def update_scene(self):
        pass
    
    def get_actor(self):
        pass 
        
    def add_actors(self, actors):
        pass
        
    def get_data_for_json(self):
        '''Get a dict data for json output '''
        pass  
        
    def remove_actors(self, actors):
        pass
                                    
                                  
    @on_trait_change( 'visibility' ) 
    def update_visibility(self):
       
        pass
    
    @on_trait_change( 'representation' ) 
    def update_representation(self):        
        pass
    
    
    @on_trait_change( 'opacity' ) 
    def update_opacity(self):
        pass
       
        
    
    view = View( VGroup( Item(name='visibility',
                              label='Visibility',
                              resizable = True), 
                         Spring(),
                         Item(name='representation',
                              label='Representation',
                              resizable = True), 
                         Spring(),
                         Item(name='opacity',
                              label='Opacity',
                              resizable = True), 
                         show_border = True,
                        ),
                  resizable = True
               )
                              
                              
                          
                          
            

if __name__ == '__main__':
    a = EleBaseVisualProperty()
    
    a.configure_traits()

    