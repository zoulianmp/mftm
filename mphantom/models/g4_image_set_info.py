# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 15:08:10 2011

@author: ZouLian
@Oncology Department
@Sichuan People's Hospital
@Chengdu,Sichuan,China
"""


import datetime



# Enthought library imports.

from traits.api import HasTraits,Str,Instance, Int, Enum, Float,List, \
                       Directory, on_trait_change,String, Date, Time
 
from traitsui.api import Item, View, Spring, VGroup,VGrid,HGroup,Label,Readonly,HFlow

import string

from util import ensure_dir
# dicom library imports.__debug__

#import sys 
#import os.path
#import time
#import dicom
import numpy as np
           
from dicom.dataset import Dataset, FileDataset
from dicom.UID import  pydicom_root_UID
from tvtk.api import tvtk
from traitsui.menu import OKButton,  CancelButton

from vtk.util import vtkConstants

    
class G4ImageSetInfo(HasTraits):
   
   nvoxels_x = Int(4)
   nvoxels_y = Int(4)
   nvoxels_z = Int(4)
   
   step_x = Float(2.0)
   step_y = Float(2.0)
   step_z = Float(2.0)
   
   offset_x = Float(0.0)
   offset_y = Float(0.0)
   offset_z = Float(0.0)


#Image i-j-k index
   bound_x_min = Float()
   bound_x_max = Float()
   
   bound_y_min = Float()
   bound_y_max = Float()
   
   bound_z_min = Float()
   bound_z_max = Float()
   
   bounds = (bound_x_min,bound_x_max,
             bound_y_min,bound_y_max,
             bound_z_min,bound_z_max)

   def __init__(self,**traits):
        super(G4ImageSetInfo, self).__init__(**traits)
        self.update_bounds()
        
        
        
        
        
   def _nvoxels_x_changed(self, old,new):
       if new < 2 :
           self.nvoxels_x = 2
       
       self.update_bounds()
        
   def _nvoxels_y_changed(self, old,new):
       if new < 2 :
           self.nvoxels_y = 2
       
       self.update_bounds()
             
   def _nvoxels_z_changed(self, old,new):
        if new < 2 :
           self.nvoxels_z = 2
       
        self.update_bounds()
        
        
        
        
        
   def _step_x_changed(self, old,new):
        self.update_bounds() 
        
   def _step_y_changed(self, old,new):          
        self.update_bounds()
   
   def _step_z_changed(self, old,new):             
        self.update_bounds()
  
   def _offset_x_changed(self, old,new):             
        self.update_bounds()
   
   def _offset_y_changed(self, old,new):             
        self.update_bounds()
   
   def _offset_z_changed(self, old,new):             
        self.update_bounds()
    
  
   def update_bounds(self):
        self.bound_x_min = -0.5* (self.nvoxels_x-1) * self.step_x +self.offset_x
        self.bound_x_max = 0.5* (self.nvoxels_x-1) * self.step_x +self.offset_x
        
        self.bound_y_min = -0.5* (self.nvoxels_y-1) * self.step_y +self.offset_y
        self.bound_y_max = 0.5* (self.nvoxels_y-1) * self.step_y +self.offset_y
        
          
        self.bound_z_min = -0.5* (self.nvoxels_z-1) * self.step_z +self.offset_z
        self.bound_z_max = 0.5* (self.nvoxels_z-1) * self.step_z +self.offset_z
        
        
        self.bounds = (self.bound_x_min,self.bound_x_max,
                       self.bound_y_min,self.bound_y_max,
                       self.bound_z_min,self.bound_z_max)

        
   
   space = VGroup(
                   Spring(),
                   Spring(),
                   Spring(),
                   Spring()
                  )

 
 
   view = View( 
                  VGroup(
                        
                        HGroup(Item('nvoxels_x', 
                                    label='NvoxelsX',
                                   
                                    resizable = False),
                               Item('nvoxels_y', 
                                    label='NvoxelsY',
                                   
                                    resizable = False),
                               Item('nvoxels_z', 
                                    label='NvoxelsZ',
                                 
                                    resizable = False),
                              label = "The Voxels' number: ",
                              show_border = True
                     
                              ),
                         space,
                         HGroup(Item('step_x', 
                                    label='Step X',
                                   
                                    resizable = False),
                               Item('step_y', 
                                    label='Step Y',
                                   
                                    resizable = False),
                              Item('step_z', 
                                    label='Step Z',
                                   
                                    resizable = False),
                              label = "The Voxel Parameters (mm):",
                              show_border = True
                               
                                ),
                         space,
                         HGroup(Item('offset_x', 
                                    label='Offset X',
                                   
                                    resizable = False),
                               Item('offset_y', 
                                    label='Offset Y',
                                   
                                    resizable = False),
                              Item('offset_z', 
                                    label='Offset Z',
                                   
                                    resizable = False),
                              label = "The VOI Offset (mm):",
                              show_border = True
                               
                                ),
                        space,

                        VGroup(
                        
                            HGroup(
                                Readonly('bound_x_min', 
                                            label='Xmin',              
                                            resizable = False),  
                                
                                Readonly('bound_y_min', 
                                            label='Ymin',
                                            resizable = False),
                                            
                                Readonly('bound_z_min', 
                                            label='Zmin',
                                            resizable = False), 
                                ),            
                             HGroup(     
                               Readonly('bound_x_max', 
                                    label='Xmax', 
                                    resizable = False),
                                    
                               Readonly('bound_y_max', 
                                    label='Ymax',
                                    resizable = False),
            
                               Readonly('bound_z_max', 
                                    label='Zmax',        
                                    resizable = False)
                                    ) ,
                            label = "The Extracted Boundary (mm)",
                            show_border = True ),
                            
                            
                            
                        label = "The Extracted G4Geometry Parameters",
                        show_border = True,
                        ),
               
               )
                              
 
 
 
 
 
 
 
 
 
 
 
 
 
####################################

if __name__ == '__main__':
    
   
   imageinfo = G4ImageSetInfo()
   
   imageinfo.configure_traits()