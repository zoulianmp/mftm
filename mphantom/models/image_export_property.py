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

    
class ImageExportProperty(HasTraits):
   
    
    #dicom output presets
    file_name_prefix = Str('Vscan.CT.')
    file_name_suffix = Str('phantom.dcm')
    
    export_style = Enum('Dicom CTImage','GEANT4 Geometry',
                        'EGSnrc Geometry','FoxChase-MCTP Geometry')
    output_dir = Directory('./image_output')
    
  

    #***************************************************************************
    #
     
    space = VGroup(
                   Spring(),
                   Spring(),
                   Spring(),
                   Spring()
                  )
                  
  
                           
    io_group = VGroup(
                     HGroup(Item(name = 'export_style',
                            label = 'Export Styles'),
                            Spring()),
                     
                     Item(name = 'output_dir',
                          label = 'Output Directory'),
                    

                     label = 'Image Export Properties', 
                     show_border = True,    
    
                    )
 
    view = View(io_group )
 
####################################

if __name__ == '__main__':
    
  prop =  ImageExportProperty()
  prop.configure_traits()