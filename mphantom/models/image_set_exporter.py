# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 15:08:10 2011

@author: ZouLian
@Oncology Department
@Sichuan People's Hospital
@Chengdu,Sichuan,China
"""



# Enthought library imports.

from traits.api import HasTraits,Str,Instance, Int, Enum, Float,List, \
                       Directory, on_trait_change,String
 
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


from image_export_property import ImageExportProperty

from image_set_info import ImageSetInfo

from dicom_exporter import DicomExporter
    
class ImageSetExporter(HasTraits):
   
    image_sets = List(tvtk.ImageData) 
    
    
    image_set_info = Instance(ImageSetInfo)
   
    export_property = Instance(ImageExportProperty)
   

    dicom_worker = Instance(DicomExporter)
#    geant4_worker = Instance()
    
   
        
    def __init__(self,**traits):
        super(ImageSetExporter, self).__init__(**traits)
        
        self.image_set_info = ImageSetInfo()
   
        self.export_property = ImageExportProperty()
        
                       
        
    def do_dicom_export(self):
        dicom_worker =DicomExporter()
            
        dicom_worker.image_set_info  = self.image_set_info
        dicom_worker.export_property = self.export_property
        dicom_worker.image_sets = self.image_sets
            
        dicom_worker.do_job()
            
        
   
    #********************************************************************
    #Do Export Job 
    def do_export_job(self):
        if self.export_property.export_style == 'Dicom CTImage' or 'EcliseTPS-CTImage' :
            print "Image Export Style:",  self.export_property.export_style
            self.do_dicom_export()
            
#        elif self.export_property.export_style == 'DicomCT-Xio 4.3.1' :
#            self.do_dicom_export()
#        
#        elif self.export_property.export_style ==  'DicomCT-Xio 4.6.4' :
#            self.do_dicom_export()
#        
#        elif  self.export_property.export_style == 'GEANT4 Geometry' :
#            pass
          


    space = VGroup(
                   Spring(),
                   Spring(),
                   Spring(),
                   Spring()
                  )


 
    view = View( 
                 Item(name='image_set_info',
                      style='custom',
                      show_label = False),
                 space,
                 Item(name='export_property',
                      style='custom',
                      show_label = False),
               
                title = 'Image Set Exporter',
                height= 500,
                width = 400,
                kind = 'livemodal',
                buttons = [OKButton,CancelButton]
                )
 
####################################

if __name__ == '__main__':
    
   
   exporter =  ImageSetExporter()
   exporter.configure_traits()
   
   