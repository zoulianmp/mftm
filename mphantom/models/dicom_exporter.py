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
           
from dicom.dataset import Dataset, FileDataset
from dicom.UID import  pydicom_root_UID
from tvtk.api import tvtk
from traitsui.menu import OKButton,  CancelButton

from vtk.util import vtkConstants

from image_export_property import ImageExportProperty

from image_set_info import ImageSetInfo



    
class DicomExporter(HasTraits):
    
    image_sets = List(tvtk.ImageData) 
   
    image_3d = Instance(tvtk.ImageData) 
   
 
             
    image_set_info = Instance(ImageSetInfo)
  
    
    export_property = Instance(ImageExportProperty)
    
    
    file_meta_data = Instance(Dataset)

    slice_template = Instance(Dataset)
    
    dicom_minimum = Instance(Dataset)
    
    
    
    slice_dataset = Instance(Dataset)
    image_pixel_array = Instance(np.ndarray)    
    
    
    
    
    
    
    image_style = Enum('minimum','template')
    
    #*******Define the Dicom root uid for other places use**************************
    uid_root = Str()    
      
    sop_instance_uid_start_value = 39 
    
    sop_instance_uid = Int(0)
    
    test = Str()
    
    def _test_default(self):
        pass
        
    
         
    #********************************************************************
    #Initial member variable
    def _slice_template_default(self):
           
        #This Postion can read a template dicom file,then return the Dataset.
        #This is very usefull
        
        
        import os
        dev_root = 'F:/PythonDir/DicomSolution/mphantom/'
        run_root =  os.getcwd() + '/mphantom/models/'
 
        dev_path = os.path.join(dev_root,'images/DicomCTTemplate.dcm') 
        run_path = os.path.join(run_root,'./images/DicomCTTemplate.dcm') 

        import dicom
        
        if os.path.isfile(dev_path):       
            dataset = dicom.read_file(dev_path,force=True)
             
        elif os.path.isfile(run_path):
            dataset = dicom.read_file(run_path,force=True)
        
        
        return  dataset
        
        
    def _dicom_minimum_default(self):
        
        data = Dataset()
        
        self.gen_init_dicom_dataset(data)
        
        return data
        
          
    def _file_meta_data_default(self):
        return  self.get_file_meta()
        
    def _image_pixel_array_default(self):
        array = np.ones((512,512),dtype = np.int16) * -1000
        array[100:412,100:412] = 200
        array[200:312,200:312] = 800
        return  array
        
     
    
  
        
    #********************************************************************
    #Value changed callbacks
         
    @on_trait_change('image_set_info')
    def update_uid_root(self):
        self.uid_root =  pydicom_root_UID + self.image_set_info.time_stamp_str 
        
        
    

#*******************************************************
#  Export  related properties
#*******************************************************  
    @on_trait_change('export_style')
    def _export_style_callback(self):
        if self.export_style == 'GeneralUse':
            self.file_name_prefix = Str('Vscan.CT.')
            self.file_name_suffix = Str('phantom.dcm')
            
        elif self.export_style == 'Xio 4.3.1' or self.export_style =='Xio 4.6.4':
           
            Tname =string.join(string.split(self.patient_name),sep="_") 
            self.file_name_suffix = Tname
              
             
            full_study_id = '0108' + self.date + '000'+ self.short_study_id
            self.file_name_prefix = "CTI."+ self.patient_id +'.' + full_study_id +"."
    
    
    
    #********************************************************************
    #functions for gen useful datas
    def get_file_meta(self):
        """generate the dicom file meta data.
        """
        file_meta = Dataset()
        file_meta.FileMetaInformationVersion = '\x00\x01'
        file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.2' # CT Image Storage
        file_meta.MediaStorageSOPInstanceUID = self.uid_root +'.' + '1'  # !! Need valid UID here for real work
        file_meta.TransferSyntaxUID = '1.2.840.10008.1.2'
 
        file_meta.ImplementationClassUID = pydicom_root_UID + "1" # !!! Need valid UIDs here
    
        return  file_meta
        
   
    
    def gen_patient_module(self,dataset):
        """Generate the CT Image Storage Patient Module Attributes
        """
        dataset.PatientsName = 'TestPhantom'
        dataset.PatientID ='0001'
        dataset.PatientsBirthDate = '0'
        dataset.PatientsSex = 'Other'

     
    def gen_general_study_module(self,dataset):
        """Generate the CT Image Storage General Study Module Attributes
        """
        dataset.StudyInstanceUID = self.uid_root +'.' + '5'
        
        from datetime import datetime
    
        tim = datetime.now()
        
        date = tim.strftime("%Y%m%d")
        time = tim.strftime("%H%M%S")
     
        
        
        dataset.StudyDate = date
        #dataset.StudyTime = self.time + '.00'
        dataset.StudyTime = time 
        dataset.AccessionNumber = '01'+date+time
        
        
        
        
        full_study_id = '0108' + date + '000'+ '001'
        dataset.StudyID =  full_study_id
        
        dataset.ReferringPhysiciansName = 'MagicalPhantomSoftware'
        dataset.StudyDescription = "StudyGeneratedbyMagicalPhantom"
        
    def gen_general_series_module(self,dataset):
        """Generate the CT Image Storage General Series Module Attributes
        """
        dataset.Modality = 'CT'
        dataset.SeriesInstanceUID =  self.uid_root +'.' + '8'
        dataset.PatientPosition = 'HFS'
        dataset.SeriesDescription = 'VitualScanSeries'       
        dataset.SeriesNumber = "2"
        dataset.OperatorsName = "MPhantom"
    def gen_frame_of_reference_uid_module(self,dataset):
        """Generate the CT Image Storage frame_of_reference_uid Module Attributes
        """
        dataset.FrameofReferenceUID = self.uid_root +'.' + '15'
        dataset.PositionReferenceIndicator = ' '
    
    def gen_general_equipment_module(self,dataset):
        """Generate the CT Image Storage General Equipment Module Attributes
        """    
        dataset.Manufacturer ='Zoulian@SichuanProvincialPeople\'sHospital'
        dataset.ManufacturersModelName = 'MagicalPhantom'
        dataset.PixelPaddingValue = '-1000'
        dataset.StationName = 'MPLabDicom'
    def gen_general_image_module(self,dataset):
        """Generate the CT Image Storage General Image Module Attributes
        """  
        dataset.InstanceNumber = 1
        dataset.AcquisitionNumber = ''
        
    def gen_image_plane_module(self,dataset):
        """Generate the CT Image Storage Image Plane Module Attributes
        """  
        
        
        dataset.PixelSpacing= ['0.85','0.85']
                                             
        dataset.SliceThickness = '3.0'
        
        
                                       
        dataset.ImagePositionPatient = [-256.0,-256.0,0.0]
        dataset.ImageOrientationPatient = ['1.0','0','0','0','1.0','0']
        dataset.SliceLocation = str(-256.0)
        
        
    def gen_image_pixel_module(self,dataset):
        """Generate the CT Image Storage Image Pixel Module Attributes
        """  
        dataset.SamplesperPixel = 1
        dataset.PhotometricInterpretation = 'MONOCHROME2'
        dataset.Rows = 512
        dataset.Columns =  512
        dataset.BitsAllocated = 16
        dataset.BitsStored = 16
        dataset.PixelRepresentation = 1
  
      
        
        # dataset.PixelAspectRatio = '1:1'
        #the PixelData property will be assigned another place
   
    def gen_ct_image_module(self,dataset):
        """Generate the CT Image Storage CT Image Module Attributes
        """  
        dataset.ImageType = ['ORIGINAL','PRIMARY','AXIAL']
        dataset.RescaleIntercept = '0'
        dataset.RescaleSlope = '1'
        
        dataset.GantryDetectorTilt = '0'
        dataset.TableHeight = 129
        dataset.HighBit = 15
        
        dataset.KVP = ''
        dataset.BitsAllocated = 16
    
    def gen_sop_common_module(self,dataset):
        """Generate the CT Image Storage SOP Common Module Attributes
        """  
        dataset.SOPClassUID = '1.2.840.10008.5.1.4.1.1.2'
        dataset.SOPInstanceUID = self.uid_root+'.' + str(self.sop_instance_uid_start_value) # start value is 39
        
        dataset.SoftwareVersions = "1.0.0"
        
        dataset.SpecificCharacterSet = "ISO_IR 100"
        
        dataset.InstanceCreatorUID = self.uid_root
        
    def gen_init_dicom_dataset(self,dataset):
        """Generate the init Dicom DataSet,in the dataset,have some fixed uid suffix value:
            1,  StudyInstanceUID is 5;
            2,  SeriesInstanceUID is 8;
            3,  FrameofReferenceUID is 15;
            4,  SOPInstanceUID is starting as 39;
    
            the Dicom CT Image PixelValue range: -1000 -> 1000 (HU)
            the demension unit is mm.
            
            image fixed values:
            1, PixelSpacing is (1.0,1.0)            
        """
        self.gen_patient_module(dataset)
        self.gen_general_study_module(dataset)
        self.gen_general_series_module(dataset)
        self.gen_frame_of_reference_uid_module(dataset)
        self.gen_general_equipment_module(dataset)
        self.gen_general_image_module(dataset)        
        self.gen_image_plane_module(dataset)
        self.gen_image_pixel_module(dataset)
        self.gen_ct_image_module(dataset)
        self.gen_sop_common_module(dataset)
        
        
        
       
 
        
    

    def gen_dicom_files(self,outdir,image_3d,imageinfo,slice_dataset):
        
       
        
        if(image_3d is None):
            #from pyface.api import MessageDialog
            #dialog = MessageDialog(message="The 3D Image  is not Set,Please Solve the Problem befor Export the DICOM Files!",
            #                       title="Failure of  3D Image  Check", severity='information')
            #dialog.open()  
            print "check"
            return 
            
        else:
            dim3 = image_3d.dimensions
            origin = image_3d.origin
            spacing = image_3d.spacing
              
            center_x =  origin[0] + dim3[0]/2.0 * spacing[0]
            center_y =  origin[1] + dim3[1]/2.0 * spacing[1]
                
            #Matrix for get 2d from 3d image array
            axial = tvtk.Matrix4x4()      
            axial.deep_copy((-1, 0, 0, 0,
                         0, -1, 0, 0,
                         0, 0, 1, 0,
                         0, 0, 0, 1))         
                         
              
            for n in range(dim3[2]):
                #Set the 2D Image Values             
                current_x =  origin[0]
                current_y =  origin[1]
                current_z =  origin[2] + n*spacing[2]
                
              
                
                #****************************************************
                #Modify the Image properties
                
                imageinfo.image_number = n
                
                
                slice_dataset.SOPInstanceUID = self.uid_root+'.'+ str(self.sop_instance_uid_start_value + n)
              
                 
               
                imageinfo.slice_thickness = spacing[2]
                
                imageinfo.image_spacing_x = spacing[0]
                imageinfo.image_spacing_y = spacing[1]
                
                
                
                
                imageinfo.image_rows = dim3[1]    
                imageinfo.image_colums = dim3[0]                
    
                imageinfo.image_position = [current_x,current_y,current_z]
    
               
                #***************************************************
                #Update the reslice matrix
                 
                axial.set_element(0, 3, center_x)
                axial.set_element(1, 3, center_y)
                axial.set_element(2, 3, current_z) 
           
                image_2d =  get_slice_from_3d_image(image_3d,axial)
               
               
               
               
                #get the image pixel array
                array_1d = image_2d.point_data.scalars.to_array()
                
               
                
                pixel_array = np.reshape(array_1d,(dim3[0],dim3[1]))
                
                 
          
          
                slice_dataset.PixelData = pixel_array.tostring()
            
                
                #****************************************************
                #Write out dicom image file
                fn_prefix = self.export_property.file_name_prefix
                fn_sufix =  self.export_property.file_name_suffix
                
                out_file_name =outdir + '/'  + fn_prefix \
                                    + str(n) + '.' +  fn_sufix 
                                    
                                    
                                    
                out_version = self.export_property.export_style                   
                                    
            
                slice_dataset.is_little_endian = True
                slice_dataset.is_implicit_VR = True  
                
                    
                imageinfo.update_dataset(slice_dataset)
   
       
               
                if out_version == 'DicomCT-Xio 4.3.1':
                    
                    fds = FileDataset(out_file_name, slice_dataset) 
                    fds.save_as(out_file_name)
                    
                elif out_version == 'DicomCT-GeneralUse':
               
                     # Create the FileDataset instance (initially no data elements, but file_meta supplied)
                   
                    fds = FileDataset(out_file_name, slice_dataset,file_meta=self.file_meta_data, preamble="\0"*128) 
                    fds.save_as(out_file_name)
                    
                elif out_version == 'DicomCT-Xio 4.6.4':
                  
                    fds = FileDataset(out_file_name,slice_dataset, file_meta=self.file_meta_data)  
                    fds.save_as(out_file_name)
           
       
    
       
    def do_job(self):
        
            
        dicoms_out_dir = self.export_property.output_dir+ '/' + self.export_property.export_style
        
        ensure_dir(dicoms_out_dir)
    
        if self.image_style == 'template':
            self.slice_dataset = self.slice_template
                
        elif self.image_style == 'minimum':
            self.slice_dataset = self.dicom_minimum
        
       
        if len(self.image_sets) == 1:
            
            self.image_3d = self.image_sets[0]
            self.gen_dicom_files(dicoms_out_dir,self.image_3d,self.image_set_info,self.slice_dataset)
        
       
 
        elif len(self.image_sets) > 1:
            #Do multiple image sets export
            print "in the multiple image sets export"
            pass
            

    




    #***************************************************************************
    #
     
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
                           
                           Item(name ='patient_age',
                                label = 'Patient Age'),
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
                           
    io_group = VGroup(
                     HGroup(Item(name = 'export_style',
                            label = 'Export Styles'),
                            Spring()),
                     
                     Item(name = 'dicoms_out_dir',
                          label = 'Output Directory'),
                    

                     label = 'Dicom Image IO Properties', 
                     show_border = True,    
    
                    )
 
    view = View(
               VGroup(
                      space,
                      patient_group,
                      space,
                      image_set_group,
                      space,
                      io_group
                     ),
                     
               
                title = 'Dicom CT Image Exporter',
                height= 500,
                width = 400,
                kind = 'livemodal',
                buttons = [OKButton,CancelButton]
                )
 
####################################

if __name__ == '__main__':
    
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
    
    
