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

    
class DicomExporter(HasTraits):
   
    image_3d = Instance(tvtk.ImageData) 
   
    #Define the root uid for other places use
    uid_root = Str()    
    
    #patient values
    patient_id = Str('123456')
    patient_name = Str('Magical Phantom')
    patient_age = Int()
    patient_sex =  Enum('Male','Female','Other')
     
    
    #image set related values
    short_study_id = String('001',minlen=3,maxlen=3)    
    
    study_comment = Str('Phantom virtual scan')
    
    sop_instance_uid_start_value = 39 
    
    sop_instance_uid = Int(0)
    
    image_number = Int(0)  #as image slice number    
    slice_thickness = Float(3.0)
    
    
    image_position = List([-256.0,-256.0,0.0])
    
    image_rows = Int(512)    
    image_colums = Int(512)
    
    image_pixel_array = Instance(np.ndarray)    
    
    #Axial Matrix for 2d Image extract from 3D              
    matrix_axial = Instance(tvtk.Matrix4x4)
         
                             
                             
                             
    #dicom data sets
    file_meta_data = Instance(Dataset)
    data_set = Instance(Dataset)
    
    dicom_export_spacing_x = Float(0.85)
    dicom_export_spacing_y = Float(0.85)
#    
    
    #dicom output presets
    file_name_prefix = Str('Vscan.CT.')
    file_name_suffix = Str('phantom.dcm')
    
    export_style = Enum('GeneralUse','Xio 4.3.1','Xio 4.6.4')
    dicoms_out_dir = Directory('./dicom_output')
    
    out_file_name = "E:/TestDataBase/testout.dcm"
    
    #*****Date and Time variables********
    year = Int()
    date = Str()
    time = Str()
    
    time_stamp_str = Str()
    
    #********************************************************************
    #Initial member variable
    def _data_set_default(self):
        
        #This Postion can read a template dicom file,then return the Dataset.
        #This is very usefull
        
        
        import os
        dev_root = 'F:/PythonDir/DicomSolution/mphantom/'
        run_root =  os.getcwd()
 
        dev_path = os.path.join(dev_root,'images/DicomCTTemplate.dcm') 
        run_path = os.path.join(run_root,'./images/DicomCTTemplate.dcm') 

        import dicom
        
        if os.path.isfile(dev_path):       
            dataset = dicom.read_file(dev_path,force=True)
             
        elif os.path.isfile(run_path):
            dataset = dicom.read_file(run_path,force=True)
        
        
        return  dataset
          
    def _file_meta_data_default(self):
        return  self.get_file_meta()
        
    def _image_pixel_array_default(self):
        array = np.ones((512,512),dtype = np.int16) * -1000
        array[100:412,100:412] = 200
        array[200:312,200:312] = 800
        return  array
        
    def _matrix_axial_default(self):
        axial = tvtk.Matrix4x4()      
        axial.deep_copy((-1, 0, 0, 0,
                         0, -1, 0, 0,
                         0, 0, 1, 0,
                         0, 0, 0, 1))
        return axial
        
    def __init__(self,**traits):
        super(DicomExporter, self).__init__(**traits)
        
        self.init_time_related_variables()
        self.uid_root =  pydicom_root_UID + self.time_stamp_str + '.'
       
        self.gen_init_dicom_dataset()
        
    #********************************************************************
    #Value changed callbacks
    
    

#*******************************************************
#  Patient  related properties
#*******************************************************    
    @on_trait_change( 'patient_id' )
    def _patient_id_callback(self):
         self.data_set.PatientID = self.patient_id
          
    @on_trait_change( 'patient_name' )
    def _patient_name_callback(self):
         self.data_set.PatientsName = self.patient_name
          
    @on_trait_change( 'patient_age' )
    def _patient_age_callback(self):
         self.data_set.PatientsBirthDate =str(self.year - self.patient_age)
          
          
    @on_trait_change( 'patient_sex' )
    def _patient_sex_callback(self):
         self.data_set.PatientsSex = self.patient_sex
        

#*******************************************************
#  Image  related properties
#*******************************************************

    @on_trait_change('sop_instance_uid')
    def _sop_instance_uid_callback(self):
        self.data_set.SOPInstanceUID  =  self.uid_root + str(self.sop_instance_uid)
    

    
    @on_trait_change( 'image_number' )
    def _image_number_callback(self):
        self.data_set.InstanceNumber = self.image_number
        self.data_set.InstanceCreationTime = str(int(self.time) + self.image_number)
         
    @on_trait_change( 'slice_thickness' )
    def _slice_thickness_callback(self):
        self.data_set.SliceThickness = self.slice_thickness
    
    @on_trait_change( 'dicom_export_spacing_x' )
    def _dicom_export_spacing_x_callback(self):
        self.data_set.PixelSpacing= [self.dicom_export_spacing_x,
                                      self.dicom_export_spacing_y]
           
        
    @on_trait_change( 'dicom_export_spacing_y' )
    def _dicom_export_spacing_y_callback(self):
        self.data_set.PixelSpacing= [self.dicom_export_spacing_x,
                                      self.dicom_export_spacing_y]
        
        
        
    @on_trait_change('image_position[]')
    def _image_position_callback(self):
        #this one has been obstacled
        self.data_set.ImagePosition = [str(self.image_position[0]),
                                       str(self.image_position[1]),
                                       str(self.image_position[2])]
                                       
    
        self.data_set.ImagePositionPatient = [str(self.image_position[0]),
                                       str(self.image_position[1]),
                                       str(self.image_position[2])]
        
        self.data_set.SliceLocation = str(self.image_position[2])        
        
        
        
        
        
    @on_trait_change('image_rows')  
    def _image_rows_callback(self):
        self.data_set.Rows = self.image_rows   
      
    
    @on_trait_change('image_colums')  
    def _image_colums_callback(self):
        self.data_set.Columns =  self.image_colums 
        
    @on_trait_change('image_pixel_array')
    def _image_pixel_array_callback(self):
        self.data_set.PixelData = self.image_pixel_array.tostring()


#*******************************************************
#  Study  related properties
#*******************************************************
         
    @on_trait_change('short_study_id')
    def _image_study_id_callback(self):
        full_study_id = '0108' + self.date + '000'+ self.short_study_id
        self.data_set.StudyID = full_study_id

     
    @on_trait_change('study_comment')
    def _image_study_comment_callback(self):
        self.data_set.StudyDescription = self.study_comment
    


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
        file_meta.MediaStorageSOPInstanceUID = self.uid_root + '1'  # !! Need valid UID here for real work
        file_meta.TransferSyntaxUID = '1.2.840.10008.1.2'
 
        file_meta.ImplementationClassUID = pydicom_root_UID + "1" # !!! Need valid UIDs here
    
        return  file_meta
        
        
        
    def init_time_related_variables(self):
        """initial the date and time related variables for further application.
        """
        
        from datetime import datetime
    
        tim = datetime.now()
        
        self.date = tim.strftime("%Y%m%d")
        self.time = tim.strftime("%H%M%S")
        self.year = tim.year
        self.time_stamp_str =  tim.strftime("%Y%m%d.%H%M%S")
    
    def gen_patient_module(self):
        """Generate the CT Image Storage Patient Module Attributes
        """
        self.data_set.PatientsName = self.patient_name
        self.data_set.PatientID = self.patient_id
        self.data_set.PatientsBirthDate =str(self.year - self.patient_age)
        self.data_set.PatientsSex = self.patient_sex

     
    def gen_general_study_module(self):
        """Generate the CT Image Storage General Study Module Attributes
        """
        self.data_set.StudyInstanceUID = self.uid_root + '5'
        self.data_set.StudyDate = self.date
        #self.data_set.StudyTime = self.time + '.00'
        self.data_set.StudyTime = self.time 
        self.data_set.AccessionNumber = '01'+self.date+self.time
        
        
        
        
        full_study_id = '0108' + self.date + '000'+ self.short_study_id
        self.data_set.StudyID =  full_study_id
        
        self.data_set.ReferringPhysiciansName = 'MagicalPhantomSoftware'
        self.data_set.StudyDescription = "StudyGeneratedbyMagicalPhantom"
        
    def gen_general_series_module(self):
        """Generate the CT Image Storage General Series Module Attributes
        """
        self.data_set.Modality = 'CT'
        self.data_set.SeriesInstanceUID =  self.uid_root + '8'
        self.data_set.PatientPosition = 'HFS'
        self.data_set.SeriesDescription = 'VitualScanSeries'       
        self.data_set.SeriesNumber = "2"
        self.data_set.OperatorsName = "MPhantom"
    def gen_frame_of_reference_uid_module(self):
        """Generate the CT Image Storage frame_of_reference_uid Module Attributes
        """
        self.data_set.FrameofReferenceUID = self.uid_root + '15'
        self.data_set.PositionReferenceIndicator = ' '
    
    def gen_general_equipment_module(self):
        """Generate the CT Image Storage General Equipment Module Attributes
        """    
        self.data_set.Manufacturer ='Zoulian@SichuanProvincialPeople\'sHospital'
        self.data_set.ManufacturersModelName = 'MagicalPhantom'
        self.data_set.PixelPaddingValue = '-1000'
        self.data_set.StationName = 'MPLabDicom'
    def gen_general_image_module(self):
        """Generate the CT Image Storage General Image Module Attributes
        """  
        self.data_set.InstanceNumber = self.image_number
        self.data_set.AcquisitionNumber = ''
        
    def gen_image_plane_module(self):
        """Generate the CT Image Storage Image Plane Module Attributes
        """  
        
        
        self.data_set.PixelSpacing= ['0.85','0.85']
                                             
        self.data_set.SliceThickness = '3.0'
        
        
                                       
        self.data_set.ImagePositionPatient = [str(self.image_position[0]),
                                       str(self.image_position[1]),
                                       str(self.image_position[2])]
        self.data_set.ImageOrientationPatient = ['1.0','0','0','0','1.0','0']
        self.data_set.SliceLocation = str(self.image_position[2])
        
        
    def gen_image_pixel_module(self):
        """Generate the CT Image Storage Image Pixel Module Attributes
        """  
        self.data_set.SamplesperPixel = 1
        self.data_set.PhotometricInterpretation = 'MONOCHROME2'
        self.data_set.Rows = self.image_rows   
        self.data_set.Columns =  self.image_colums 
        self.data_set.BitsAllocated = 16
        self.data_set.BitsStored = 16
        self.data_set.PixelRepresentation = 1
  
        self.data_set.PixelData = self.image_pixel_array.tostring()
        
        # self.data_set.PixelAspectRatio = '1:1'
        #the PixelData property will be assigned another place
   
    def gen_ct_image_module(self):
        """Generate the CT Image Storage CT Image Module Attributes
        """  
        self.data_set.ImageType = ['ORIGINAL','PRIMARY','AXIAL']
        self.data_set.RescaleIntercept = '0'
        self.data_set.RescaleSlope = '1'
        
        self.data_set.GantryDetectorTilt = '0'
        self.data_set.TableHeight = 129
        self.data_set.HighBit = 15
        
        self.data_set.KVP = ''
        self.data_set.BitsAllocated = 16
    
    def gen_sop_common_module(self):
        """Generate the CT Image Storage SOP Common Module Attributes
        """  
        self.data_set.SOPClassUID = '1.2.840.10008.5.1.4.1.1.2'
        self.data_set.SOPInstanceUID = self.uid_root + str(self.sop_instance_uid_start_value) # start value is 39
        
        self.data_set.SoftwareVersions = "1.0.0"
        
        self.data_set.SpecificCharacterSet = "ISO_IR 100"
        self.data_set.InstanceCreationDate = self.date
        self.data_set.InstanceCreationTime = self.time
        self.data_set.InstanceCreatorUID = self.uid_root
        
        
    def gen_init_dicom_dataset(self):
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
        self.gen_patient_module()
        self.gen_general_study_module()
        self.gen_general_series_module()
        self.gen_frame_of_reference_uid_module()
        self.gen_general_equipment_module()
        self.gen_general_image_module()        
        self.gen_image_plane_module()
        self.gen_image_pixel_module()
        self.gen_ct_image_module()
        self.gen_sop_common_module()
        
        
        
        
        

    def gen_dicom_files(self):
        
        self.dicoms_out_dir =   self.dicoms_out_dir +'/'+ self.export_style
        ensure_dir(self.dicoms_out_dir)
        
        if(self.image_3d is None):
            #from pyface.api import MessageDialog
            #dialog = MessageDialog(message="The 3D Image  is not Set,Please Solve the Problem befor Export the DICOM Files!",
            #                       title="Failure of  3D Image  Check", severity='information')
            #dialog.open()  
            print "check"
            return 
            
        else:
            dim3 = self.image_3d.dimensions
            origin = self.image_3d.origin
            spacing = self.image_3d.spacing
              
            center_x =  origin[0] + dim3[0]/2.0 * spacing[0]
            center_y =  origin[1] + dim3[1]/2.0 * spacing[1]
                
              
            for n in range(dim3[2]):
                #Set the 2D Image Values             
                current_x =  origin[0]
                current_y =  origin[1]
                current_z =  origin[2] + n*spacing[2]
                
              
                
                #****************************************************
                #Modify the Image properties
                
                self.sop_instance_uid = self.sop_instance_uid_start_value + n
                
                self.image_number = n  #as image slice number    
               
                self.slice_thickness = spacing[2]
                
                self.dicom_export_spacing_x = spacing[0]
                self.dicom_export_spacing_y = spacing[1]
                
                
                
                
                self.image_rows = dim3[1]    
                self.image_colums = dim3[0]                
    
                self.image_position = [current_x,current_y,current_z]
    
               
                #***************************************************
                #Update the reslice matrix
                 
                self.matrix_axial.set_element(0, 3, center_x)
                self.matrix_axial.set_element(1, 3, center_y)
                self.matrix_axial.set_element(2, 3, current_z) 
           
                image_2d =  self.get_slice_from_3d_image(self.image_3d,n)
               
               
               
               
                #get the image pixel array
                array_1d = image_2d.point_data.scalars.to_array()
                
               
                
                pixel_array = np.reshape(array_1d,(dim3[0],dim3[1]))
                
                self.image_pixel_array = pixel_array
          
          
              
            
                
                #****************************************************
                #Write out dicom image file
                self.out_file_name =self.dicoms_out_dir + '/'  + self.file_name_prefix \
                                    + str(n) + '.' + self.file_name_suffix 
                
                if self.export_style == 'Xio 4.3.1':
                    
                    # Set the transfer syntax
                    self.data_set.is_little_endian = True
                    self.data_set.is_implicit_VR = True
    
                    fds = FileDataset(self.out_file_name, self.data_set) 
                    fds.save_as(self.out_file_name)
                elif self.export_style == 'GeneralUse':
                    self.data_set.is_little_endian = True
                    self.data_set.is_implicit_VR = True 
                     
                     # Create the FileDataset instance (initially no data elements, but file_meta supplied)
                    fds = FileDataset(self.out_file_name, self.data_set, file_meta=self.file_meta_data, preamble="\0"*128) 
                    fds.save_as(self.out_file_name)
                    
                elif self.export_style == 'Xio 4.6.4':
                     # Set the transfer syntax
                    self.data_set.is_little_endian = True
                    self.data_set.is_implicit_VR = True
                    
                    fds = FileDataset(self.out_file_name, self.data_set, file_meta=self.file_meta_data) 
                    fds.save_as(self.out_file_name)
                    
           
           
           
           
    def get_slice_from_3d_image(self,image3d,slicenum,bgvalue=-1000):      
        """ Extract a slice in the desired orientation of the image3d.
            get the vtkImage 2D
        """        
        reslice = tvtk.ImageReslice()
        
        reslice.auto_crop_output = True      
        reslice.background_level = bgvalue      
        reslice.input = image3d
        
        reslice.output_dimensionality = 2
        reslice.reslice_axes =  self.matrix_axial
          
#        reslice.output_spacing =[self.dicom_export_spacing_x,
#                                 self.dicom_export_spacing_y,
#                                 self.slice_thickness ]       
#        

          
        reslice.interpolation_mode = vtkConstants.VTK_NEAREST_INTERPOLATION
    
        reslice.update()
        return reslice.output
    
       


    




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
    
   
    from  debug_helpers import gen_image_data_by_numpy         
    image = gen_image_data_by_numpy(220)
   
    print image
   
    dicom_exporter = DicomExporter()
    dicom_exporter.image_3d = image
    
    dicom_exporter.configure_traits()
    
    dicom_exporter.gen_dicom_files()

  
#*******************************************
# Test for file_meta
  
    print "***************************************/n"
 
  #  print "New file meta:", meta
    #dicom_exporter.gen_init_dicom_dataset()
   # print dicom_exporter.data_set.InstanceNumber    
    
 #   print dicom_exporter.data_set
#********************************************
    
    
