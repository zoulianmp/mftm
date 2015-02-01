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
from traits.api import Delegate

from image_export_property import ImageExportProperty

from dicom_image_set_info import DicomImageSetInfo

from g4_image_set_info import G4ImageSetInfo

from dicom_exporter import DicomExporter

from g4_geometry_exporter import G4GeometryExporter


    
class ImageSetExporter(HasTraits):
        
    
   
    image_sets = List(tvtk.ImageData) #CT images set
    
    index_sets =  List(tvtk.ImageData) # Phantom's index set
    density_sets = List(tvtk.ImageData) # phantom's density set
    
    
    dicom_image_set_info = Instance(DicomImageSetInfo) #Input parameters for DICOM output
    g4_image_set_info = Instance(G4ImageSetInfo)#Input parameters for Geant4 Geometry output
    
    
    export_property = Instance(ImageExportProperty)
   
    style_flag  = Delegate( 'export_property' )
    
    dicom_worker = Instance( DicomExporter)
    geant4_worker = Instance( G4GeometryExporter)
    
   
        
    def __init__(self,**traits):
        super(ImageSetExporter, self).__init__(**traits)
        
        self.dicom_image_set_info = DicomImageSetInfo()
        self.g4_image_set_info = G4ImageSetInfo()
        
        self.g4_materials = []
        
        self.export_property = ImageExportProperty()
        
        self.dicom_worker =DicomExporter()
        self.geant4_worker = G4GeometryExporter()
                       
        
    def do_dicom_export(self):
       
            
        self.dicom_worker.dicom_image_set_info  = self.dicom_image_set_info
        self.dicom_worker.export_property = self.export_property
        self.dicom_worker.image_sets = self.image_sets
            
        self.dicom_worker.do_job()
            
    def do_g4_export(self):
       
        
        self.geant4_worker.index_sets = self.index_sets 
        self.geant4_worker.density_sets = self.density_sets
      
    
        print "in the do_g4_export: ", self.geant4_worker.g4_materials 
     
        self.geant4_worker.g4_image_set_info = self.g4_image_set_info  
        self.geant4_worker.export_property = self.export_property
    
        self.geant4_worker.do_job()
        
        

        #G4GeometryExporter
        
   
    #********************************************************************
    #Do Export Job 
    def do_export_job(self):
        style =  self.export_property.export_style
        
        print "Image Export Style:", style
        
        if style == 'Dicom CTImage' or style == 'EcliseTPS-CTImage' :
          
            self.do_dicom_export()
        elif style == 'GEANT4 Geometry' :
            self.do_g4_export()
            
            
          
#        elif self.export_property.export_style == 'DicomCT-Xio 4.3.1' :
#            self.do_dicom_export()
#        
#        elif self.export_property.export_style ==  'DicomCT-Xio 4.6.4' :
#            self.do_dicom_export()
#        



    space = VGroup(
                   Spring(),
                   Spring(),
                   Spring(),
                   Spring()
                  )


 
    view = View( 
                 Item(name='dicom_image_set_info',
                      style='custom',
                      visible_when = 'style_flag == 0',
                      show_label = False),
                      
                 Item(name='g4_image_set_info',
                      style='custom',
                      visible_when = 'style_flag == 1',
                      show_label = False),
                        
                 space,
                 Item(name='export_property',
                      style='custom',
                      show_label = False),
               
                title = 'Image Set Exporter',
                height= 500,
                width =600,
                kind = 'livemodal',
                buttons = [OKButton,CancelButton]
                )
 
####################################

if __name__ == '__main__':
    
   
   exporter =  ImageSetExporter()
   exporter.configure_traits()
   
   