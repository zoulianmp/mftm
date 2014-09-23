# -*- coding: utf-8 -*-
"""
Created on Thu Nov 03 10:58:57 2011

@author: ZouLian
@Oncology Department
@Sichuan People's Hospital
@Chengdu,Sichuan,China
"""

from traits.api import HasTraits, Instance, Str, Float
from traitsui.api import View, Item,Readonly,VGroup,Spring,HGroup,Label

from tvtk.api import tvtk

#For File IO
from tvtk.api import write_data

from base_geometry import BaseGeometry
             
######################################################################
class SphereGeometry(BaseGeometry):
    #The Added Geometry name
    geometry_typle = Str('SphereGeometry')
    
    
    radius = Float(30.0)    
    
    center_x = Float(0.0)
    center_y = Float(0.0)
    center_z = Float(0.0)
    
    source =  Instance(tvtk.SphereSource)
     
    def __init__(self,**traits):
        super(BaseGeometry,self).__init__(**traits)
        
        self.source = tvtk.SphereSource()
           
        self.source.center = (self.center_x, self.center_y, self.center_z)
       
        self.source.radius =  self.radius
        
        self.source.theta_resolution = 80
        self.source.phi_resolution = 80
        
        self.source.update()
        
        self.init_poly =self.source.output
        
            
 #      self.source.resolution = self.resolution
        
        mapper = tvtk.PolyDataMapper(input=self.init_poly)
        self.current_actor = tvtk.Actor(mapper=mapper)
        
    

    def get_data_for_json(self):
        '''Get a dict data for json output '''
        data = {}
        data["GeoType"] = "Sphere"
        data["InitialParams"] = [self.radius,
                                 self.center_x,self.center_y,self.center_z]
       
        return data       
    
          
   
    
    
    
    view = View( VGroup( Item(name='geometry_typle',
                              label='GeometryTyple',
                              style ='readonly'), 
                         Spring(),

                         Item('radius', 
                              label='Radius(mm)',
                              width = 30),
                         HGroup(Item('center_x', 
                                    label='X',
                                    width = 30),
                               Item('center_y', 
                                    label='Y',
                                    width = 30),
                              Item('center_z', 
                                    label='Z',
                                    width = 30),
                             label = "Center(mm)   " ),
                
                         show_border = True,                     
                      )       
               )
               


if __name__ == '__main__':
    a = SphereGeometry()
    
    a.configure_traits()
   
    from mphantom.api import ActorsViewer
    
    viewer = ActorsViewer()
    viewer.add_actors(a.current_actor)
    viewer.configure_traits()
    
    
    