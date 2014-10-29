



# Enthought library imports.

from traits.api import HasTraits,Str,Instance, Int, Enum, Float,List, \
                       Directory, on_trait_change,String
 
from traitsui.api import Item, View, Spring, VGroup,VGrid,HGroup

import string

from mphantom.api import ensure_dir, get_slice_from_3d_image,ImageExportProperty,ImageSetInfo
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



# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 13:56:49 2014

@author: ZouLian
@Joint Lab for Medical Physics
@Oncology Department
@Sichuan People's Hospital
@Chengdu,Sichuan,China

"""

def test_dicom_exporter():
    
    imginfo = ImageSetInfo()
    imginfo.configure_traits()
    
   
    from  debug_helpers import gen_image_data_by_numpy         
    image = gen_image_data_by_numpy(220)
   
    print image
    
    
#    
#    
#       export_style = Enum('DicomCT-GeneralUse','DicomCT-Xio 4.3.1',
#                        'DicomCT-Xio 4.6.4','GEANT4 Geometry',
#                        'EGSnrc Geometry','FoxChase-MCTP Geometry')
#    output_dir = Directory('./image_output')
#    
    
    exprop = ImageExportProperty()
 #   exprop.export_style= 'DicomCT-Xio 4.3.1'
    
    exprop.export_style= 'DicomCT-Xio 4.6.4'
    
    exprop.output_dir = 'F:/DICOMOUT'
    
    
    dicom_exporter = DicomExporter()
    dicom_exporter.export_property = exprop
    
    dicom_exporter.image_style ='template'
    
    dicom_exporter.image_set_info = imginfo 
    
    dicom_exporter.image_sets = [image]
    
    dicom_exporter.do_job()
    


  
#*******************************************
# Test for file_meta
  
    print "**********Test Run Successfully*****************************/n"
 
  #  print "New file meta:", meta
    #dicom_exporter.gen_init_dicom_dataset()
   # print dicom_exporter.data_set.InstanceNumber    
    
 #   print dicom_exporter.data_set
#********************************************
    
    