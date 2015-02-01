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

from util import ensure_dir, get_slice_from_3d_image
# dicom library imports.__debug__

#import sys
#import os.path
#import time
#import dicom
import numpy as np
      
from util import message_box      
      
from tvtk.api import tvtk
from traitsui.menu import OKButton,  CancelButton

from vtk.util import vtkConstants

from image_export_property import ImageExportProperty

from g4_image_set_info import G4ImageSetInfo

from image_export_property import ImageExportProperty

    
class G4GeometryExporter(HasTraits):
    
    index_sets = List(tvtk.ImageData) 
    density_sets = List(tvtk.ImageData)
    
        
    extracted_index_sets = List(tvtk.ImageData) 
    extracted_density_sets = List(tvtk.ImageData)
    
    g4_materials = List()
    
   

     
    g4_image_set_info = Instance(G4ImageSetInfo)   
    export_property = Instance(ImageExportProperty)
    
    
    
     
    def __init__(self,**traits):
        super(G4GeometryExporter, self).__init__(**traits)          
       
    
    def read_g4_material_list(self, fname):
        
        self.g4_materials = [] 
        index = 0
        
         
        import csv   
        with open(fname, 'rb') as csvfile:
            material_set = csv.DictReader(csvfile) 
              
            for row in material_set:
                name = row["MaterialName"]
                
                material_pair = (index,name)
                self.g4_materials.append(material_pair)
                index = index + 1  
        csvfile.close() 
        
    
    def prepare_extracted_images(self):
        
        from util import MATE_LIST_FILE
        self.read_g4_material_list(MATE_LIST_FILE)
        
        
            
        image_info = self.g4_image_set_info
        
        extracted_bounds = image_info.bounds
        extracted_steps = (image_info.step_x,image_info.step_y,image_info.step_z)
        
        extracted_index_sets = []
        extracted_density_sets = []
        
        for index in self.index_sets:
            origin = index.origin
            spacing = index.spacing
            
            x_factor = spacing[0]/extracted_steps[0]
            y_factor = spacing[1]/extracted_steps[1]
            z_factor = spacing[2]/extracted_steps[2]
            
            resampled_image = self.resample_image(index,x_factor,y_factor,z_factor)
            
            resampled_spacing = resampled_image.spacing
             
            from debug_helpers import print_image_info
            
            print "Resampled Index:x"
            print_image_info(resampled_image)
            
            extracted_voi = ((extracted_bounds[0] - origin[0])/resampled_spacing[0],
                             (extracted_bounds[1] - origin[0])/resampled_spacing[0],
                             (extracted_bounds[2] - origin[1])/resampled_spacing[1],
                             (extracted_bounds[3] - origin[1])/resampled_spacing[1],
                             (extracted_bounds[4] - origin[2])/resampled_spacing[2],
                             (extracted_bounds[5] - origin[2])/resampled_spacing[2]           
                            )
            extracted_image = self.extract_image_voi(resampled_image,extracted_voi)
           
            self.extracted_index_sets.append(extracted_image)
           
           
        for density in self.density_sets:
            origin = density.origin
            spacing = density.spacing
            
            x_factor = spacing[0]/extracted_steps[0]
            y_factor = spacing[0]/extracted_steps[1]
            z_factor = spacing[0]/extracted_steps[2]
            
            resampled_image = self.resample_image(density,x_factor,y_factor,z_factor)
            
            resampled_spacing = resampled_image.spacing
             
            from debug_helpers import print_image_info
            
            print "Resampled Index:x"
            print_image_info(resampled_image)
            
            extracted_voi = ((extracted_bounds[0] - origin[0])/resampled_spacing[0],
                             (extracted_bounds[1] - origin[0])/resampled_spacing[0],
                             (extracted_bounds[2] - origin[1])/resampled_spacing[1],
                             (extracted_bounds[3] - origin[1])/resampled_spacing[1],
                             (extracted_bounds[4] - origin[2])/resampled_spacing[2],
                             (extracted_bounds[5] - origin[2])/resampled_spacing[2]           
                            )
            extracted_image = self.extract_image_voi(resampled_image,extracted_voi)
           
            self.extracted_density_sets.append(extracted_image)
           
               
       

        
        
        

    
    def resample_image(self,image,x_factor=1.0,y_factor=1.0,z_factor=1.0):
        
        resampler = tvtk.ImageResample()
        
        resampler.input = image
        
        #interpolation modes : cubic,linear, nearest neigbor    
        resampler.interpolation_mode = 'cubic' 
        resampler.set_axis_magnification_factor(0, x_factor)
        
        resampler.set_axis_magnification_factor(1, y_factor)
        resampler.set_axis_magnification_factor(2, z_factor)
        
        resampler.update()
     
        return resampler.output

        
        
        
        
    #voi is (xmin,xmax,ymin,ymax,zmin,zmax)    
    def extract_image_voi(self,image,voi):
        
        extractor =tvtk.ExtractVOI()
        
        extractor.input = image
        
        extractor.voi = voi
         
         
        extractor.update ()
        return extractor.output
         
        
    def write_g4geometry_header(self,fhandle):
        
        import csv
         
        material_num = len(self.g4_materials)
        
        writer = csv.writer(fhandle,delimiter = ' ', lineterminator='\n')
                
        writer.writerow([material_num])
        
        for n in range(0,material_num):
             writer.writerow(self.g4_materials[n])
            
 
       
    def do_job(self):
        
        self.prepare_extracted_images()       
   
        out_dir = self.export_property.output_dir+ '/' + self.export_property.export_style
        
        ensure_dir(out_dir)
        
        if (len(self.extracted_density_sets) != len(self.extracted_index_sets) ):
            message_box(message= "The number of index is not equal to number of density!",
                                   title="Index not match Density"  , severity='error')
            return 
            
        
        #****************************************************
        #Write out Geant4 geometr files
        
        sets_number = len(self.extracted_density_sets)
        
                
        fn_prefix = self.export_property.file_name_prefix
        fn_sufix =  self.export_property.file_name_suffix
        
        import csv
        for n in range(0,sets_number):
            out_file_name = out_dir + '/'  + fn_prefix \
                            + str(n) + '.' +  fn_sufix 
                            
            #  write out the Data set
            
            index  = self.extracted_index_sets[n]
                
            density = self.extracted_density_sets[n]
            
            image_info = self.g4_image_set_info
            
            out_nvoxels = [image_info.nvoxels_x, image_info.nvoxels_y, image_info.nvoxels_z]
             
       
            out_bound_x = [image_info.bound_x_min, image_info.bound_x_max]
            out_bound_y = [image_info.bound_y_min, image_info.bound_y_max]
            out_bound_z = [image_info.bound_z_min, image_info.bound_z_max]
            
                    
            with open(out_file_name, 'w') as csvfile:
         
                self.write_g4geometry_header(csvfile)

                writer = csv.writer(csvfile,delimiter = ' ', lineterminator='\n')
                
                writer.writerow(out_nvoxels)
                writer.writerow(out_bound_x)  
                writer.writerow(out_bound_y) 
                writer.writerow(out_bound_z)
                
                import numpy as np        
                np_index = np.frombuffer(index.point_data.scalars.to_array(), dtype=np.int16)          
                
                np_density = np.frombuffer(density.point_data.scalars.to_array(), dtype=np.float32) 
                
                np_index.tofile(csvfile, sep=" ", format="%i") 
                writer.writerow([])
                
                np_density.tofile(csvfile, sep=" ", format="%f") 
              
            csvfile.close()


             
            print "**********Geant4 Geometry Exported Successfully*****************************/n"
            
            
            content = self.export_property.export_style + "  Exported Successfully"
            
            message_box(message= content,
                                   title="Exported Successfully", severity='information')

             
 

        
####################################

if  __name__ == '__main__':
    
    imginfo = ImageSetInfo()
    imginfo.configure_traits()
    
   
    from  debug_helpers import gen_image_data_by_numpy         
    image = gen_g4geometry_by_numpy(220)
   
    print image
    
    
#    
#    
#       export_style = Enum('DicomCT-GeneralUse','DicomCT-Xio 4.3.1',
#                        'DicomCT-Xio 4.6.4','GEANT4 Geometry',
#                        'EGSnrc Geometry','FoxChase-MCTP Geometry')
#    output_dir = Directory('./image_output')
#    
    
    exprop = G4GeometryExporter()
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
    
    
