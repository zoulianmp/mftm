 # -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 10:03:36 2011

@author: ZouLian
@Oncology Department
@Sichuan People's Hospital
@Chengdu,Sichuan,China
"""


"""
This is the Entry point for Invoke the Test codes


"""

from test.test_volume_image_slice_views import test_volume_image_slicer

from test.test_dicom_exporter import test_dicom_exporter

if __name__ == '__main__':
    
    test_dicom_exporter()
    test_volume_image_slicer()
