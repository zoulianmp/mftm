# -*- coding: utf-8 -*-
"""
Created on Thu Nov 03 10:58:57 2011

@author: ZouLian
@Oncology Department
@Sichuan People's Hospital
@Chengdu,Sichuan,China
"""

from traits.api import HasTraits, Instance, Str, Float, Int
from traitsui.api import View, Item,Readonly,VGroup,Spring,HGroup,Label

from tvtk.api import tvtk

#For File IO
from tvtk.api import write_data

from base_geometry import BaseGeometry
             
######################################################################
class CylinderGeometry(BaseGeometry):
    #The Added Geometry name
    geometry_typle = Str('CylinderGeometry')
    
  
    
    center_x = Float(0.0)
    center_y = Float(0.0)
    center_z = Float(0.0)
    
  
    #unit is mm
    height = Float(30.0)
    radius = Float(15.0)
    
    resolution = Int(80)
       
    source = Instance(tvtk.CylinderSource)
    
    def __init__(self,**traits):
        super(CylinderGeometry,self).__init__(**traits)
        
        self.source = tvtk.CylinderSource()
     
        self.source.center = (self.center_x, self.center_y, self.center_z)
    
        self.source.height = self.height
        self.source.radius =  self.radius
        self.source.resolution = self.resolution
       
        self.source.update()
                    
  
        self.init_poly = self.source.output
        
        mapper = tvtk.PolyDataMapper(input=self.init_poly)
        self.current_actor = tvtk.Actor(mapper=mapper)
        
  
    def _center_x_changed(self, value):
        
       # print self.source.angle
        if self.source is not None:
            self.source.center = (self.center_x,self.center_y,self.center_z)
            
            self.source.update()
            
    def _center_y_changed(self, value):
        
       # print self.source.angle
        if self.source is not None:
            self.source.center = (self.center_x,self.center_y,self.center_z)
            
            self.source.update()
            
        
    def _center_z_changed(self, value):
        
       # print self.source.angle
        if self.source is not None:
            self.source.center = (self.center_x,self.center_y,self.center_z)
            
            self.source.update()
            
    def _height_changed(self, value):
        
        if self.source is not None:
            self.source.height = value
            
            self.source.update()
            
        
        
    def _radius_changed(self, value):
        if self.source is not None:
            self.source.radius = value
            
            self.source.update()
            
     
    
    def _resolution_changed(self, value):
        if self.source is not None:
            self.source.resolution = value
            
            self.source.update()
                
            



    def get_data_for_json(self):
        '''Get a dict data for json output '''
        data = {}
        data["GeoType"] = "Cylinder"
        data["InitialParams"] = [self.center_x,self.center_y,self.center_z,
                                 self.height,self.radius,self.resolution]
       
        return data
                
           
    
    view = View( VGroup( Item(name='geometry_typle',
                              label='GeometryTyple',
                              style ='readonly'), 
                         Spring(),

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

                         Spring(),
                         Item(name='height',
                              label='Height(mm)'), 
                         Item(name='radius',
                              label='Radius (mm)'), 
                         Spring(),
                         Spring(),
                         
                         Item('_'),
                         Item(name='resolution',
                              label='Resolution'),
                         show_border = True,
                        
                     
                      )       
               )
               
               
   

if __name__ == '__main__':
    a = CylinderGeometry()
    
    a.configure_traits()

     
    from MagicalPhantom.api import ActorsViewer
    
    viewer = ActorsViewer()
    viewer.add_actors(a.current_actor)
    viewer.configure_traits()
    
    
    

