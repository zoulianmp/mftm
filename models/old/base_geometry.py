# -*- coding: utf-8 -*-
"""
Created on Thu Nov 03 10:58:57 2011

@author: ZouLian
@Oncology Department
@Sichuan People's Hospital
@Chengdu,Sichuan,China
"""

from traits.api import HasTraits, Instance, Enum, Dict,List,Str
from traitsui.api import View,Item,Spring,Group
from tvtk.pyface import actors
from tvtk.api import tvtk

from vtk_external_file import VTKExternalFileReader
from traitsui.menu import OKCancelButtons

            


#For File IO
from tvtk.api import write_data

             
######################################################################
class BaseGeometry(HasTraits):
       
    #The Added Geometry name
    geometry_name = Str('BaseGeometry')
      
    current_source = Instance(HasTraits)
      
    #The Geometry Container 
    geometry = List(tvtk.Actor)
      
     
    # Flag to set the poly data type.
    source = Enum('Cone','Cube','Cylinder',
                    'Sphere','Superquadric',
                    'VTKExternalFile','STLExternalFile',
                     desc='which poly data source to be used')
     
     
    
    def __init__(self,**traits):
        super(BaseGeometry,self).__init__(**traits)
        self._source_changed('Cone')
   
    ########################################
    # Private traits.
    
    _current_actor = Instance(tvtk.Actor)  

    # A dictionary that maps the source names to instances of the
    # poly data sources.
    _source_dict = Dict(Str,
                          Instance(HasTraits,
                                   allow_none=False))
         
                          
                                  
    ######################################################################
    # Non-public methods.
    ######################################################################
    def _source_changed(self, value):
        """This method is invoked (automatically) when the `source`
        trait is changed.
        """
        self.current_source = self._source_dict[self.source]
        self._current_actor = self._generat_actor(self.current_source)      
        




    def __source_dict_default(self):
        """Default value for source dict."""
        sd = {'Cone':tvtk.ConeSource(),
              'Cube':tvtk.CubeSource(),
              'Cylinder':tvtk.CylinderSource(),
              'Sphere':tvtk.SphereSource(),
              'Superquadric':tvtk.SuperquadricSource(),
              'VTKExternalFile':VTKExternalFileReader(),
              'STLExternalFile':tvtk.STLReader(),
              }
        return sd
        
        
        
     #Generate the actor from selected source
     
    def _generat_actor(self,source):
         mapper = tvtk.PolyDataMapper(input=source.output)
         actor = tvtk.Actor(mapper=mapper)
         return actor


    def __set_pure_state__(self,state):
        
        #current number single elements
        n_g = len(self.geometry)
        
        #number of single elements in saved state
        n_saved_g = len(state.geometry)        
                
        
        #remove extra ones
        for i in range(n_g - n_saved_g):
            self.geometry.pop(-1)
        
        #add New ones 
        for i in range(n_saved_g - n_g):
            se = tvtk.Actor()
            
            self.geometry.append(se)
            
            
            
    #Save the geometry to file in disk        
    def save_geometry(self,fname):
        polydata = self.get_polydata()
        write_data(polydata,fname)
    
         
         
    #Get the Element's geometry bounds                      
    def get_bounds(self):
        
        xmin = 0
        xmax = 0
        
        ymin = 0
        ymax = 0

        zmin = 0
        zmax = 0
        
        if len(self.geometry) >0:
            bounds = self.geometry[0].bounds
            xmin = bounds[0]
            xmax = bounds[1]
        
            ymin = bounds[2]
            ymax = bounds[3]

            zmin = bounds[4]
            zmax = bounds[5]
        else:
            return              
        
        #Iterating the single elements
        for actor in self.geometry:
            tbounds = actor.bounds
            
            if tbounds[0] < xmin :
                xmin = tbounds[0]
            
            if tbounds[1] > xmax :
                xmax = tbounds[1]
                
            if tbounds[2] < ymin :
                ymin = tbounds[2]
                
            if tbounds[3] > ymax :
                ymax = tbounds[3]
                
            if tbounds[4] < zmin :
                zmin = tbounds[4]
                
            if tbounds[5] > zmax :
                zmax = tbounds[5]      
               
        bounds = (xmin,xmax,ymin,ymax,zmin,zmax)
        
        return bounds
            
         
    #Get the geometry data as a polydata         
    def get_polydata(self):
        nactor = len(self.geometry)          
        
        if nactor > 0:
            if nactor > 1 :
                polyappender = tvtk.AppendPolyData()
                for actor in self.geometry:
                
                    
                    polydata = self._get_polydata_from_actor(actor)
                    
                    polyappender.add_input(polydata)                 
                    polyappender.update()
                    
                    return polyappender.output            
            else:
                actor = self.geometry[0]
                
                polydata = self._get_polydata_from_actor(actor)
                
                polydata.update()                             
                return polydata
        
                
                
    # The useful function for get polydata from an actor            
    def _get_polydata_from_actor(self, actor):
        #Get the polydata pre actor         
        prepolydata =  actor.mapper.input
        
        #Creat the Transform correspond to the actor's internal Varians
           
        #Get the actor's internal Varians
        origin = actor.origin
        orientation = actor.orientation
        scale = actor.scale
        position = actor.position
        
        #Set the Transform
        transform = tvtk.Transform()
        

     
        transform.post_multiply()
        
        #Shif back to actor's origin
        transform.translate(origin)
        
        #scale
        transform.scale(scale)
        
        #Rotate
        transform.rotate_y(orientation[1])
        transform.rotate_x(orientation[0])
        transform.rotate_z(orientation[2])
        
        #move back from origin and translate
        transform.translate(origin [0] + position[0],
                            origin [1] + position[1],
                            origin [2] + position[2])
                            
    
        #Transform the polydata to the final state
        
        polydatafilter = tvtk.TransformPolyDataFilter(input = prepolydata, 
                                                      transform = transform )
        
        return polydatafilter.output        
            

if __name__ == '__main__':
    a = BaseGeometry()
    
    a.configure_traits()

