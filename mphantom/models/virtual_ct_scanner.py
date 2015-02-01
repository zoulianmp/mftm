# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 15:08:10 2011

@author: ZouLian
@Oncology Department
@Sichuan People's Hospital
@Chengdu,Sichuan,China
"""

# Enthought library imports.
from traits.api import Array, HasTraits, Float, Instance, \
                       List, Str, Int, Enum, Button, Event, \
                       Bool

from traitsui.api import View, Item, VGroup, HGroup,Spring,Label,UItem

from mphantom.api import message_box
from tvtk.api import tvtk
from vtk.util import vtkConstants

from pyface.api import ImageResource
from math import ceil


from ct_scanner_parameters import CT_Scanner_Parameters

from m_phantom import MPhantom

from image_set_exporter import ImageSetExporter

class Virtual_CT_Scanner(HasTraits): 
    
    #the scanning parameters of ct scanner
    scanning_paras = Instance(CT_Scanner_Parameters)
    
    
    #### 'Virtual Scan Output Image interface #################################
    #The Image world coordinates is based on Unit: mm 
    raw_data =List(tvtk.ImageData) 
        
    material_index_data = List(tvtk.ImageData) 
    
    material_density_data =  List(tvtk.ImageData)  
   
    
    #A broker for dicom export
    image_exporter = Instance (ImageSetExporter)
    
    #the patient needs to scan
    phantom = Instance(MPhantom)
  
  
    
    ###### Star Scan Interface#################################################
    start_scan_button = Button(label = 'Start Scan')
    
    
    has_cached_raw_data = Bool(False)
    
    
    ready_for_view = Event()
    
    reset_viewers = Event() #Event for reset the slice viewers
    
    ready_for_export = Bool(False)
    ##########################################################################

  
  
    
    ###### Star Scan Interface#################################################
    start_scan_button = Button(label = 'Start Scan')
    
    export_button = Button(label='Image Files Export')
   
    
    
   
   
    def __init__(self,**traits):
        super(Virtual_CT_Scanner, self).__init__(**traits)
        
        self.scanning_paras = CT_Scanner_Parameters()
        self.image_exporter = ImageSetExporter()
        self.raw_data =[]
        self.material_index_data = [] 
        self.material_density_data =[]
       
    
        
       


    #Check the elements of Phantom for virtual Scan  ,
    #Pass the Check return True
    #Fail the check return False
    def phantom_elements_check(self,phantom):
        
        print "len(phantom.three_dimension_elements) >0", len(phantom.three_dimension_elements) >0
        
        print "len(phantom.four_dimension_elements) >0",len(phantom.four_dimension_elements) >0
       
        
        c1 = len(phantom.three_dimension_elements) >0
        c2 =  len(phantom.four_dimension_elements) >0
        
        t = c1|c2
              
         
        if (c1 | c2):
            return True
        else:
            message_box(message="The Phantom is Empty,Please Construct the Phatom Before Scanning!",
                                   title="Failure of Elements Check", severity='error')
            return False
        
              
              
   
    #Check the Boundary of Phantom for virtual Scan  ,
    #Pass the Check return True
    #Fail the check return False
    def phantom_boundary_check(self,phantom):
              
        bounds = phantom.get_bounds()
           
        width = bounds[1]-bounds[0]
        lenth = bounds[3]-bounds[2]
        
        width_limit = self.scanning_paras.slice_size[0] * self.scanning_paras.spacing_x
        lenth_limit = self.scanning_paras.slice_size[1] * self.scanning_paras.spacing_y
           
           
 
           
        if width > width_limit or lenth > lenth_limit :
            message_box(message="The Phantom Boundary Overflow,Bigger than the Scanner Range!",
                                   title="Failure of Boundary Check", severity='error')
 
          
            return False
        else:
            return True
     
    #Check the Boundary of Phantom for virtual Scan  ,
    #Pass the Check return True
    #Fail the check return False
    def elements_priority_check(self,phantom):
        
        elist = phantom.get_sorted_elements_by_priority()
        
#        print "elist", elist
#        print "len(elist):", len(elist)
#        
        if len(elist): 
            return True
        else:
            return False
            
#        
#        
#        p_list = []
#  
#        for eletuple in elist:
#            
#            element = eletuple[1]
#            
#            p_value = element.general.priority 
#            if (p_list.count(p_value) > 0 ) :
#                message_box(message="The Priority of Element Conflict,Check the Priority Attribute of Element!",
#                                   title="Failure of Element Priority Check", severity='error')
#       
#                return False
#            p_list.append(p_value)
#               
#         
##        for element in phantom.compound_elements:
##            p_value = element.priority 
##            if (p_list.count(p_value) > 0 ) :
##                from pyface.api import MessageDialog
##                dialog = MessageDialog(message="The Priority of Element Conflict,Check the Priority Attribute of Element!",
##                                   title="Failure of Element Priority Check", severity='error')
##                dialog.open()
#           
#                return False
#            p_list.append(p_value)
        
     #   return True
             
       
    #Generate the White Image data for mask the phantom model 
    def _gen_image_data_by_numpy(self,defaultvalue=0.0,pixeltype = 0):
         """
         Phantom coordinates:
               bounds = self.phantom.get_bounds(),get the phantom bound.
               x,y bound can't break the Image bound.

               z bound decide the image zmin, slice number.
               
        
        
         Image Coordinates:
            Image.origin place at（xmin，ymin，zmin），
        
         pixeltype = 0 , pixel type is  np.int16
         pixeltype = 1 , pixel type is  np.float32
        
         """
    
         params = self.scanning_paras       
    
     
         bounds = self.phantom.get_bounds()
       
         print "phantom.bounds", bounds
    
      
         spacing_z = params.slice_thickness
       
     
         # self.slice_num  = int(ceil((bounds[5] - bounds[4])/self.spacing_z))+1
         params.slice_num  = int(ceil((bounds[5] - bounds[4])/spacing_z))
       
       
         #The phantom center
         params.center_x = (bounds[1] + bounds[0])/2.0
         params.center_y = (bounds[3] + bounds[2])/2.0
      
         params.center_z = (bounds[5] + bounds[4])/2.0
       
       
         #The Image Parameters
         spacing = ( params.spacing_x, params.spacing_y, spacing_z)
     
         image_bounds = [-0.5* (params.slice_size[0]-1)*spacing[0], 0.5* (params.slice_size[0]-1)*spacing[0],
       
                         -0.5* (params.slice_size[1]-1)*spacing[1], 0.5* (params.slice_size[1]-1)*spacing[1],
       
                         -0.5* (params.slice_num-1)*spacing[2] + params.center_z, -0.5* (params.slice_num-1)*spacing[2] + params.center_z
                        ]
       
         origin = (image_bounds[0],image_bounds[2],image_bounds[4])  
       
       
       
         image = tvtk.ImageData()
       
         dim= (params.slice_size[0],params.slice_size[1], params.slice_num )
       
         print "The VTK Image Dims:", dim
      
         exten = (0,dim[0]-1,0,dim[1]-1,0,dim[2]-1)
     
         #the background HU Value of air 
         # bgvalue = self._get_air_hu_value()
       
     
         #Initialize the volume value
         import numpy as np
         if pixeltype == 0:
             scalars = np.ones(dim,dtype = np.int16) * defaultvalue
             image.scalar_type = vtkConstants.VTK_SHORT
             
         elif pixeltype == 1:
             scalars = np.ones(dim,dtype = np.float32) * defaultvalue
             image.scalar_type = vtkConstants.VTK_FLOAT
     
         #set image property
         image.origin = origin
         image.spacing = spacing
         image.extent = exten
       
        
         image.point_data.scalars = scalars.ravel()
    
         print "Initial Generate the image array,in the _gen_image_data_by_numpy(self): "
         return image
       
           
       
    #get the air HU Value from selected scanner
    def _get_air_hu_value(self):
        air = 0.001
        return self.scanning_paras.ed_hu_curve.get_hu_from_edensity(air)
    
        
    ###############################################
    ##########  Virtual Scan Related fucitons
    ###############################################     
    def _start_scan_button_fired(self):
        from pyface.api import ConfirmationDialog, YES
        dialog = ConfirmationDialog(message= "Are you sure start virtual scan ?",
                                    title = "Confirm Scan Action")
       
               
        choice = dialog.open()
        
        print "Current spacing: ",self.scanning_paras.spacing_x, \
                                  self.scanning_paras.spacing_y, \
                                  self.scanning_paras.slice_thickness 
    
   
    
        
        if self.has_cached_raw_data:
            self.raw_data =[]
            
         
        if choice == YES:    
            self.reset_viewers = True # Reset the slice views first
           
            if self.phantom.phantom_type =='3DPhantom':
                
                self._3d_phantom_scanning()    
                
                self.ready_for_view = True
                
                print "Fire the ready_for_view EVENT"
                
                self.has_cached_raw_data = True
       
       
                self.image_exporter.image_sets = self.raw_data 
                
                self.image_exporter.index_sets =  self.material_index_data # Phantom's index set
                self.image_exporter.density_sets = self.material_density_data #Phantom's density set  
             
              
                
              #  print "The Phantom Materials: ", self.g4_materials
                
                
                self.ready_for_export = True


                
            elif  self.phantom.phantom_type == '4DPhanotm':
                pass
            
            elif self.phantom.phantom_type == 'DeformablePhantom':
                pass
        
            else:
                pass
            
            #self._3d_phantom_scanning()
            
        else:
            print "Cancle the scan action"
            
            
          
            
    def _export_button_fired(self):
        
        print "enter the button fired"       
        ui =  self.image_exporter.edit_traits()
    
              
        if ui.result:
            print "Let the image export brocker to do job! \n"
            self.image_exporter.do_export_job()
       
        else:
           print "You has cancer the export action !"
           return
           
       
      
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
    def _phantom_checks(self):
        
        if self.phantom is not None:
              
            ''' If the Phantom pass the constraints check ,return the True
            '''
            if not self.phantom_elements_check(self.phantom): return False
            
            if not self.phantom_boundary_check(self.phantom): return False    
            
            if not self.elements_priority_check(self.phantom): return  False
    
            return True        
        else:
            return False
              
    
            
            
    def _3d_phantom_scanning(self):
        
        if not self._phantom_checks():
            print "The Phantom Don't Pass The Check."
            return
  
  
        #Get the initial 3d Image data ,index data,density data  
        init_huv = self._get_air_hu_value()
        rawdata = self._gen_image_data_by_numpy(init_huv,pixeltype =0)
        
        init_index = 0
        index_data = self._gen_image_data_by_numpy(init_index,pixeltype = 0)
        
        init_density = 0.1
        density_data = self._gen_image_data_by_numpy(init_density,pixeltype = 1)
        
        
        
        
        
        #Do the real Scan for elements coordinate to priority of elements
        elements_list =  self.phantom.get_sorted_elements_by_priority()
        
        print "elements_list",elements_list
        
        outdata_list = self._do_virtual_scan(rawdata,index_data,density_data,elements_list)
        
        
        self.raw_data.append(outdata_list[0])
        self.material_index_data.append(outdata_list[1])
        self.material_density_data.append(outdata_list[2])
    
      
            
            
    #Do the real virtual scan job ,correspond to elements_list       
    def _do_virtual_scan(self,rawdata,indexdata,densitydata,elements_list):
       
        
        in_image = rawdata  
        in_index = indexdata
        in_density = densitydata
         
        #Do the HU Image set updated
        for item in elements_list:
            element = item[1]
          
            hu = self.scanning_paras.ed_hu_curve.get_hu_from_edensity(element.general.re_e_density)
            
            index = element.general.material_index
            
            material =  element.general.tissue_type
            
            density =  element.general.mass_density           
            
#            mat_pair = (index,material)
#            
#            self.g4_materials.append(mat_pair)
            
            print "element.name = ",element.name, hu, index, material, density 
            
            polydata = element.geometry.transformed_poly
               
          
            tem_image = self._polydata_to_image(in_image,polydata,hu)
            tem_index = self._polydata_to_image(in_index,polydata,index)
            tem_density =  self._polydata_to_image(in_density,polydata,density)
                       
            
            
            in_image = tem_image
            in_index = tem_index
            in_density = tem_density
         
      
        return [in_image,in_index,in_density]
      
      
       
        

    #Mask the polydata to volume image with vaiue HU     
    def _polydata_to_image(self,image,polydata,bghu):
        
        print "Do polydata to image "
       
#        #*******************************************
#        sphere = tvtk.SphereSource()
#        sphere.phi_resolution = 80
#        sphere.theta_resolution = 80
#        sphere.center = (0,0,0)
#        sphere.radius = 30
#        sphere.update()        
   
         
        triangle = tvtk.TriangleFilter()
        triangle.input = polydata
        
        #triangle.input = sphere.output
  
        stripper =tvtk.Stripper()
        stripper.input = triangle.output
        
        dataToStencil = tvtk.PolyDataToImageStencil()
        dataToStencil.input = stripper.output
                   
        dataToStencil.output_spacing = image.spacing
        dataToStencil.output_origin= image.origin
        dataToStencil.tolerance = 0.01
         
        stencil = tvtk.ImageStencil()
        stencil.input = image
        stencil.stencil = dataToStencil.output
        
        stencil.reverse_stencil = True
        
        stencil.background_value = bghu
        
        stencil.update()   
        return stencil.output
        
        
        
        
        
        
        
        
        
        
        
        
    ##########################
    ##########  UI Related
    ###############################################           
           
    space =  VGroup(Spring(),
                    Spring(),
                    Spring()
                   )
            
   

    view = View( VGroup(Item(name='scanning_paras',
                            style ='custom',
                            show_label= False),
                        HGroup(   
                               Spring(),
                               UItem('start_scan_button'),
                               Spring(),
                               UItem('export_button',   
                               visible_when='ready_for_export'),  
                               )
                   ),
                            
                             
                 scrollable =True,
                 resizable = True )

   
    

  
if __name__ == "__main__":
   
    from three_dimension_element import ThreeDimensionElement
     
    from mphantom.api import CubeGeometry,ConeGeometry
    cube = CubeGeometry()
    cube.configure_traits()
    
    cone = ConeGeometry()
    cone.configure_traits()
    
    cube_element = ThreeDimensionElement()
    cube_element.geometry = cube
    cube_element.configure_traits()
    
    
    cone_element = ThreeDimensionElement()
    cone_element.geometry = cone
    
    phantom = MPhantom()
    
    phantom.add_3d_element(cube_element)
    phantom.add_3d_element(cone_element)
    
    
 
      
    scanner =  Virtual_CT_Scanner()
    
    scanner.phantom = phantom
    
    
    scanner.configure_traits()
    
