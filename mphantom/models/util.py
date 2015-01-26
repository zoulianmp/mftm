#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-
# util.py
"""Several utility functions that don't really belong anywhere."""
#


import os

from tvtk.api import tvtk

from vtk.util import vtkConstants




ELEMENT_LIB_PATH = ""
CFG_PATH = ""



def set_system_path(mainpath):
    
    
    
    global ELEMENT_LIB_PATH 
    global CFG_PATH
    
    import os
   
    ELEMENT_LIB_PATH= os.path.join(os.path.dirname(mainpath), 'elements_lib')
    CFG_PATH =  os.path.join(os.path.dirname(mainpath), 'mphantom\config')
    
    
    

def makesure_element_in_lib(rootpath, elementname):
    import os 
    
    fname = rootpath + elementname
    exist = os.path.exists(fname)
    
    if not exist:
        
        tips = "The element: " + elementname + " is not in your elements libs,pelease makesure your element lib is right for your use!"
        topinfo="Element not In Libs"

        message_box(message=tips, title=topinfo, severity='error')


def get_main_dir():
          
    mainpath = os.getcwd()
    return mainpath

def get_residual_filename(prepath, fullpath):
           
    fullsize = len(fullpath)
    prenum =  len(prepath) 
    
    residual = fullpath[prenum:fullsize]
    
    return residual


#**********************************************
#Ensure the directory is here
#**********************************************
def ensure_dir(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)
        



def message_box(message,title,severity):
    from pyface.api import MessageDialog
    dialog = MessageDialog(message= message, title= title, severity=severity)
    dialog.open()

          
def get_slice_from_3d_image(image3d,matrix,bgvalue=-1000):      
    """ Extract a slice in the desired orientation of the image3d.
        get the vtkImage 2D        
        Matrix for 2d Image extract from 3D is instance of tvtk.Matrix4x4   
        
        matrix_axial = Instance(tvtk.Matrix4x4)         
    """        
    reslice = tvtk.ImageReslice()
    
    reslice.auto_crop_output = True      
    reslice.background_level = bgvalue      
    reslice.input = image3d
    
    reslice.output_dimensionality = 2
    reslice.reslice_axes =  matrix
      
#        reslice.output_spacing =[self.dicom_export_spacing_x,
#                                 self.dicom_export_spacing_y,
#                                 self.slice_thickness ]       
#        

      
    reslice.interpolation_mode = vtkConstants.VTK_NEAREST_INTERPOLATION

    reslice.update()
    return reslice.output

   


    

