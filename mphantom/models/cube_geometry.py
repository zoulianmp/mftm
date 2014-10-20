# -*- coding: utf-8 -*-
"""
Created on Thu Nov 03 10:58:57 2011

@author: ZouLian
@Oncology Department
@Sichuan People's Hospital
@Chengdu,Sichuan,China
"""

from traits.api import HasTraits, Instance, Str, Float,Tuple
from traitsui.api import View, Item,Readonly,VGroup,Spring,HGroup,Label

from tvtk.api import tvtk

#For File IO
from tvtk.api import write_data

from base_geometry import BaseGeometry
             
######################################################################
class CubeGeometry(BaseGeometry):
    #The Added Geometry name
    geometry_typle = Str('CubeGeometry')
    
    
    center_x = Float(0.0)
    center_y = Float(0.0)
    center_z = Float(0.0)
    
    length_x = Float(30.0)
    length_y = Float(30.0)
    length_z = Float(30.0)
    
    source = Instance(tvtk.CubeSource)
    
    def __init__(self,**traits):
        super(CubeGeometry,self).__init__(**traits)
        
      
        self.source =  tvtk.CubeSource()        
          
        self.source.center = (self.center_x, self.center_y, self.center_z)
    
        self.source.x_length = self.length_x
        self.source.y_length = self.length_y
        self.source.z_length = self.length_z
            
        
        self.source.update()
    
        self.init_poly =  self.source.output
        
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
            
        
        
    def _length_x_changed(self, value):
        
        if self.source is not None:
            self.source.x_length = self.length_x 
            
          
            self.source.update()
        
    def _length_y_changed(self, value):
        
       # print self.source.angle
        if self.source is not None:
        
            self.source.y_length = self.length_y
            
            print "length y:" ,self.source.y_length
             
            self.source.update()
        
    def _length_z_changed(self, value):   
    
        if self.source is not None:
            self.source.z_length = self.length_z
            self.source.update()
        
    def get_data_for_json(self):
        '''Get a dict data for json output '''
        data = {}
        data["GeoType"] = "Cube" 
        data["InitialParams"] = [self.center_x,self.center_y,self.center_z,
                                 self.length_x,self.length_y,self.length_z]
        
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

                         HGroup(Item('length_x', 
                                    label='X',
                                    width = 30),
                               Item('length_y', 
                                    label='Y',
                                    width = 30),
                              Item('length_z', 
                                    label='Z',
                                    width = 30),
                             label = "Length(mm)   " ),

                      
                         show_border = True,
                        
                     
                      )       
               )
               
               
   

if __name__ == '__main__':
    
    
    init =  Tuple(0.0,0.0,0.0,40,20,10)
    
    a = CubeGeometry(init_paras = init)
    
    
    
    a.configure_traits()
    
    from mphantom.api import ActorsViewer
    
    viewer = ActorsViewer()
    viewer.add_actors(a.current_actor)
    viewer.configure_traits()
    
    
 

    