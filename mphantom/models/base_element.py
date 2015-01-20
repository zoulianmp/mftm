# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 14:37:11 2011

@author: ZouLian
@Oncology Department
@Sichuan People's Hospital
@Chengdu,Sichuan,China
"""

from traits.api import on_trait_change

from traits.api import HasTraits, Str, Dict, Enum, Float,Range,Instance, \
                       Bool,DelegatesTo, Event

from traitsui.api import View, Item,Readonly,VGroup,Tabbed

from tvtk.api import tvtk
from vtk.util import colors


from tvtk.pyface import actors




from mphantom.api import PhantomUpdateHelper

from mphantom.api import EleBaseVisualProperty,EleBaseGeometryTuner,EleGeneralProperty


#local import 
from base_geometry import BaseGeometry


######################################################################
'''
A Based Class for Phantom Construction Element
'''
class BaseElement(HasTraits):
    
    helper  = Instance(PhantomUpdateHelper)
    
    general = Instance(EleGeneralProperty)
    
    name = DelegatesTo('general')
    
    
    visual = Instance(EleBaseVisualProperty)
    geometry_tuner = Instance(EleBaseGeometryTuner)
    
    geom_modified = Event
    
    geometry = Instance(BaseGeometry)
    
    
    ele_vis_modified = Event
    
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
                        tab3)          
               )
    
    
    def __init__(self):
        super(BaseElement, self).__init__()
        
        self.general = EleGeneralProperty()    
        self.visual =  EleBaseVisualProperty()
        self.geometry_tuner = EleBaseGeometryTuner()
        self.geometry = BaseGeometry()
          
        self.on_trait_event(self.update_geometry,'geom_modified')
        
        self.visual.inner_actor = self.geometry.current_actor
     
        self.general.on_trait_change(self.update_color, 'color')
   
        self.name = self.general.name
  

    def update_color(self):
        self.visual.color = self.general.color

    ########################################################
    #Set up the Real Geometry Chain 
    def setup_geometry(self):
        pass
       
       
    #Show the default splash Element
    def _show_splash(self):
        pass
    
    #Get the Element's geometry bounds                      
    def get_bounds(self):
   
        if self.geometry is not None:
            bounds = self.geometry.get_bounds()
            return bounds
    
    def get_data_for_json(self):
        '''Get a dict data for json output '''
        pass
    
    
    #mask the inimage by the element's geometry ,and fill the 
    #inimage by bgvalue on the voxels in the element's geometry
    #range
    def mask_image_by_geometry(self,inimage,bgvalue):
        pass
        
    @on_trait_change('geometry' )    
    def update_geometry(self):
        
        self.visual.inner_actor = self.geometry.current_actor
       
        self.visual.update_scene()
        
        if self.helper is not None:
            self.helper.phantom_modified =True
        
        
  
    

if __name__ == '__main__':
    a = BaseElement()
    
    a.configure_traits()
