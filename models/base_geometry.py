# -*- coding: utf-8 -*-
"""
Created on Thu Nov 03 10:58:57 2011

@author: ZouLian
@Oncology Department
@Sichuan People's Hospital
@Chengdu,Sichuan,China
"""

from traits.api import HasTraits, Instance, Str, on_trait_change

from tvtk.api import tvtk

#For File IO
from tvtk.api import write_data

             
######################################################################
class BaseGeometry(HasTraits):
       
    #The Added Geometry name
    geometry_typle = Str('BaseGeometry')
    
    init_poly = Instance(tvtk.PolyData)
      
    transformed_poly = Instance(tvtk.PolyData)
 
    current_transform = Instance(tvtk.LinearTransform)
    #The actor presente the representation in visualization window
    current_actor = Instance(tvtk.Actor)
      
   
    def _current_transform_default(self):
        
        return tvtk.IdentityTransform()
   
   
   
   
    
    def __init__(self,**traits):
        super(BaseGeometry,self).__init__(**traits)
        
      
        poly = tvtk.SphereSource().output
        self.init_poly = poly        
        
        self.current_transform = tvtk.IdentityTransform()
     
      
   
                    
            
    @on_trait_change('current_transform,init_poly')
    def update_geometry(self):
        self.update_poly_data()
        self.update_actor()
        
                    
     
        
    def update_poly_data(self):
        
        polydatafilter = tvtk.TransformPolyDataFilter(input = self.init_poly, 
                                                      transform =self.current_transform)
        polydatafilter.update()
        
        self.transformed_poly = polydatafilter.output
    
    def update_actor(self):
           
        mapper = tvtk.PolyDataMapper(input=self.transformed_poly)
        self.current_actor = tvtk.Actor(mapper=mapper)
        
        

    
    #Save the geometry to file in disk        
    def save_current_geometry_as(self,fname):
       
        write_data(self.transformed_poly,fname)
    
    def get_data_for_json(self):
        '''Get a dict data for json output '''
        pass  
         
    #Get the Element's geometry bounds                      
    def get_bounds(self):
    
        return  self.current_actor.bounds
            
  

if __name__ == '__main__':
    a = BaseGeometry()
    
    print a.actor
    


