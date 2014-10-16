# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 15:08:10 2011

@author: ZouLian
@Oncology Department
@Sichuan People's Hospital
@Chengdu,Sichuan,China
"""


def test_volume_image_slicer():
    from mphantom.api import gen_image_data_by_numpy, VolumeImageSliceViews         
    image = gen_image_data_by_numpy(220)
   
    viewers = VolumeImageSliceViews()
    viewers.volume = image
    
    viewers.configure_traits()
  
    
    
