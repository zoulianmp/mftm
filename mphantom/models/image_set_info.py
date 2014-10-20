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
 
from traitsui.api import Item, View, Spring, VGroup,VGrid,HGroup

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

    
class ImageSetInfo(HasTraits):
   
   
    
    #patient valuesimage_spacing_x
    patient_id = Str('123456')
    patient_name = Str('Magical Phantom')
    
    
    patient_birth_date = Date(datetime.datetime.today() )
    patient_birth_time = Time(datetime.datetime.now() )
       
    
    
    patient_sex =  Enum('Male','Female','Other')    
    patient_sex_map = {'Male':'M','Female':'F','Other':'O'}
    
    
    
    
    
    #image set related values
    short_study_id = String('001',minlen=3,maxlen=3)    
    
    study_comment = Str('Phantom virtual scan')
    
  
    
    image_number = Int(0)  #as image slice number    
    slice_thickness = Float(3.0)
    
    
    image_position = List([-256.0,-256.0,0.0])
    
    image_rows = Int(512)    
    image_colums = Int(512)
    
    image_spacing_x =  Float(0.85)
    image_spacing_y =  Float(0.85)
    
    
    
    #*****Date and Time variables********
    year = Int()
    date = Str()
    time = Str()
    
    time_stamp_str = Str()
         
    def __init__(self,**traits):
        super(ImageSetInfo, self).__init__(**traits)
        
        self.init_time_related_variables()
     
    
    def update_dataset(self,data_set):
        data_set.PatientID = self.patient_id 
        data_set.PatientsName = self.patient_name
        
        data_set.PatientsBirthDate = self.patient_birth_date.strftime("%Y%m%d") 
        data_set.PatientBirthTime = self.patient_birth_time.strftime("%H%M%S.%f")
        
        
        
        data_set.PatientsSex = self.patient_sex_map[self.patient_sex]
     
        
        data_set.InstanceNumber = self.image_number
        data_set.InstanceCreationTime = str(int(self.time) + self.image_number)
        
        data_set.SliceThickness = self.slice_thickness
        
        
        data_set.PixelSpacing= [self.image_spacing_x,
                                      self.image_spacing_y]
                                      
               
                       
        data_set.ImagePosition = [str(self.image_position[0]),
                                  str(self.image_position[1]),
                                  str(self.image_position[2])]
                                  
        data_set.ImagePositionPatient = [str(self.image_position[0]),
                                         str(self.image_position[1]),
                                         str(self.image_position[2])]
        
        data_set.SliceLocation = str(self.image_position[2])        
        
        
        data_set.Rows = self.image_rows   
        data_set.Columns =  self.image_colums
        
        data_set.InstanceCreationDate = self.date
        data_set.InstanceCreationTime = self.time

        
           
        full_study_id = '0108' + self.date + '000'+ self.short_study_id
        data_set.StudyID =  full_study_id

        
    def init_time_related_variables(self):
        """initial the date and time related variables for further application.
        """
        
    
        tim = datetime.datetime.now()
        
        self.date = tim.strftime("%Y%m%d")
        self.time = tim.strftime("%H%M%S")
        self.year = tim.year
        self.time_stamp_str =  tim.strftime("%Y%m%d.%H%M%S")
    
    
    def print_image_set_info(self):
        print "This is the image set info:"
        print "patient_id = ", self.patient_id
        print "patient_name = ", self.patient_name
    

     
    space = VGroup(
                   Spring(),
                   Spring(),
                   Spring(),
                   Spring()
                  )
                  
    patient_group = VGrid(
                           Item(name ='patient_id',
                                label = 'Patient ID'),
                           Spring(),
                           Item(name ='patient_name',
                                label = 'Patient Name'),
                           Spring(),
                           
                           Item(name ='patient_birth_date',
                                label = 'Patient BirthDate'),
                           Spring(),           
                           Item(name ='patient_birth_time',
                                label = 'Patient BirthTime'),
                                
                           Spring(),

                           Item(name ='patient_sex',
                                label = 'Patient Sex'),
                           Spring(),
                           
                           label = 'Patient Properties', 
                           show_border = True,    
                          )
    image_set_group = VGrid(
                          
                           Item(name = 'short_study_id',
                                label = 'Study ID'),
                           Spring(),
                           Item(name='study_comment',
                                label = 'Study Comment'),
                           Spring(),
                               
                           label = 'Image Set Properties', 
                           show_border = True,    
                           )
  
    view = View(
               VGroup(
                      space,
                      patient_group,
                      space,
                      image_set_group,
                  
                     ),
                     
        
                )
 
####################################

if __name__ == '__main__':
    
   
   imageinfo = ImageSetInfo()
   print  imageinfo.patient_birth_time
   print  imageinfo.patient_birth_time.strftime("%H%M%S.%f")
   imageinfo.configure_traits()