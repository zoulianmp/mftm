# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 17:19:19 2014

@author: ZouLian
@Joint Lab for Medical Physics
@Oncology Department
@Sichuan People's Hospital
@Chengdu,Sichuan,China

"""
from tvtk.api import tvtk
from vtk.util import vtkConstants
import numpy as np


image = tvtk.ImageData()
           
dim= (1024,1024,150)
           
print "The VTK Image Dims:", dim

   
scalars = np.ones(dim,dtype = np.int16) 
   
image.scalar_type = vtkConstants.VTK_SHORT
image.point_data.scalars = scalars.ravel()

print size(image)

print "***********************The end image test***********************"
