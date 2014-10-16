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

from traitsui.api import View, Item, VGroup, HGroup,Spring,Label
from e_density_hu_curve import EDensityHUCurve
from phantom_model import PhantomModel
from tvtk.api import tvtk
from vtk.util import vtkConstants

from pyface.api import ImageResource
from math import ceil

class VirtualScanModel(HasTraits): 
    
    #Electronic Density to HU Transform Curves Interface    
    ed_hu_files = List(Str)  
    scanner_names = List(Str)
    
    scanner =Enum(values='scanner_names')
    show_curve_button = Button(label = 'Show ED-HU Curve')
    
    ed_hu_curve = Instance(EDensityHUCurve)
    
    #ED-HU Files Dir
    #files_root = Str('./../scanners')
    files_root = Str()
    
    #### 'Virtual Scan Output Image interface #################################
    #The Image world coordinates is based on Unit: mm 
    image_data = Instance(tvtk.ImageData)    
    
    imag_slice_type = Enum('512 x 512','256 x 256')
    
    slice_size =Array(value=[512,512])
    
    ########################################################
    # The center Value
    
    center_x = Float(0.0)
    center_y = Float(0.0)
    center_z = Float(0.0)
    
    ########################################################
    #The Spacing
    
    spacing_x = Float(0.850)
    spacing_y = Float(0.850)
    spacing_z = Float(0.0)
    
    
    slice_num = Int()
    slice_thickness = Float(5) 
        
    
    #the phatom need to scan
    phantom = Instance(PhantomModel)
  
  
    
    ###### Star Scan Interface#################################################
    start_scan_button = Button(label = 'Start Scan')
    
    
    import os
    prepath = os.getcwd()
    sufpath = ".\mphantom\images"
    path = os.path.join(prepath,sufpath) 
    cslog =  ImageResource('cslog.png',search_path=[path])
    
     
    cslogregion = Button(image=cslog)
    
    
    
    ready_for_view = Event()
    reset_viewers = Event() #Event for reset the slice viewers
    
    ready_for_export = Bool(False)
    ##########################################################################

    def __init__(self,**traits):     
        super(VirtualScanModel,self).__init__(**traits)
               
        if len(self.ed_hu_files) > 0:
            self.ed_hu_curve = EDensityHUCurve(path = self.ed_hu_files[0] )
        else:
            self.ed_hu_curve = EDensityHUCurve()
    ###############################################
    ########## File Related funcitons
    ###############################################    
    def _files_root_changed(self, newpath):
        self._get_ed_hu_files(newpath)
        self.ed_hu_curve = EDensityHUCurve(path = self.ed_hu_files[0] )
   
        
   
    def _get_ed_hu_files(self,path):
        import os
        filelist = []
        fnamelist = []
        
        for file in os.listdir(path):
            
            ed_hu_file = os.path.join(path,file)
            
            if os.path.isfile(ed_hu_file):
                tfile = os.path.splitext(ed_hu_file) 
                fname = os.path.basename(tfile[0])            
                filelist.append(ed_hu_file)
                fnamelist.append(fname)
                
        self.ed_hu_files = filelist
        self.scanner_names = fnamelist
           
           
    def _scanner_changed(self,newvalue):
        index = self.scanner_names.index(self.scanner)
      
        self.ed_hu_curve.path = self.ed_hu_files[index]
        
      
        
    def _show_curve_button_fired ( self ):
        self.ed_hu_curve.configure_traits()
        
 
    ###############################################
    ##########  Image Slice Related fucitons
    ###############################################    
    def _imag_slice_type_changed(self,newvalue):
    
        if newvalue == '512 x 512':
            self.slice_size[0] = 512
            self.slice_size[1] = 512
            
        elif newvalue == '256 x 256':
            self.slice_size[0] = 256
            self.slice_size[1] = 256
            
   

    #Check the elements of Phantom for virtual Scan  ,
    #Pass the Check return True
    #Fail the check return False
    def phantom_elements_check(self,phantom):
        if len(phantom.single_elements) >0 :
            return True
        else:
            from pyface.api import MessageDialog
            dialog = MessageDialog(message="The Phantom is Empty,Please Construct the Phatom Before Scanning!",
                                   title="Failure of Elements Check", severity='error')
            dialog.open()
          
            return False
        
              
              
   
    #Check the Boundary of Phantom for virtual Scan  ,
    #Pass the Check return True
    #Fail the check return False
    def phantom_boundary_check(self,phantom):
              
        bounds = phantom.get_bounds()
           
        width = bounds[1]-bounds[0]
        lenth = bounds[3]-bounds[2]
        
        width_limit = self.slice_size[0] * self.spacing_x
        lenth_limit = self.slice_size[1] * self.spacing_y
           
           
 
           
        if width > width_limit or lenth > lenth_limit :
            from pyface.api import MessageDialog
            dialog = MessageDialog(message="The Phantom Boundary Overflow,Bigger than the Scanner Range!",
                                   title="Failure of Boundary Check", severity='error')
            dialog.open()
          
            return False
        else:
            return True
     
    #Check the Boundary of Phantom for virtual Scan  ,
    #Pass the Check return True
    #Fail the check return False
    def elements_priority_check(self,phantom):
        
        p_list = []
  
        for element in phantom.single_elements:
            p_value = element.priority 
            if (p_list.count(p_value) > 0 ) :
                from pyface.api import MessageDialog
                dialog = MessageDialog(message="The Priority of Element Conflict,Check the Priority Attribute of Element!",
                                   title="Failure of Element Priority Check", severity='error')
                dialog.open()
           
                return False
            p_list.append(p_value)
               
         
#        for element in phantom.compound_elements:
#            p_value = element.priority 
#            if (p_list.count(p_value) > 0 ) :
#                from pyface.api import MessageDialog
#                dialog = MessageDialog(message="The Priority of Element Conflict,Check the Priority Attribute of Element!",
#                                   title="Failure of Element Priority Check", severity='error')
#                dialog.open()
#           
#                return False
#            p_list.append(p_value)
        
        return True
             
       
    #Generate the White Image data for mask the phantom model 
    def _gen_image_data_by_numpy(self):
           fixed_size = (512,512)
           
           bounds = self.phantom.get_bounds()
           
           print "phantom.bounds", bounds
        
#           self.spacing_x = fixed_size[0] / self.slice_size[0]
#           self.spacing_y = fixed_size[1] / self.slice_size[1]
            
           self.spacing_z = self.slice_thickness
         
          # self.slice_num  = int(ceil((bounds[5] - bounds[4])/self.spacing_z))+1
           self.slice_num  = int(ceil((bounds[5] - bounds[4])/self.spacing_z))
           
           self.center_x = (bounds[1] + bounds[0])/2.0
           self.center_y = (bounds[3] + bounds[2])/2.0
           self.center_z = (bounds[5] + bounds[4])/2.0
               
           
           spacing = ( self.spacing_x, self.spacing_y, self.spacing_z)
           
           print "Spacing = ",spacing
           
           offset_x = (self.slice_size[0] * spacing[0])/2.0
           offset_y = (self.slice_size[1] * spacing[1])/2.0
           offset_z = (self.slice_num * spacing[2])/2.0
          
           origin_x = self.center_x  - offset_x
           origin_y = self.center_y  - offset_y
           origin_z = self.center_z  - offset_z
           
           image = tvtk.ImageData()
           
           dim= (self.slice_size[0],self.slice_size[1], self.slice_num )
           
           
           origin = ( origin_x, origin_y, origin_z)
           
          
           exten = (0,dim[0]-1,0,dim[1]-1,0,dim[2]-1)
         
           #the background HU Value of air 
           bgvalue = self._get_air_hu_value()
           
         
           #Initialize the volume value
           import numpy as np
           
           scalars = np.ones(dim,dtype = np.int16) * bgvalue
           
         
           #set image property
           image.origin = origin
           image.spacing = spacing
           image.extent = exten
           
           image.scalar_type = vtkConstants.VTK_SHORT
           image.point_data.scalars = scalars.ravel()
        
           self.image_data = image
       
    #get the air HU Value from selected scanner
    def _get_air_hu_value(self):
        air = 0.001
        return self.ed_hu_curve.get_hu_from_edensity(air)
    
        
    ###############################################
    ##########  Virtual Scan Related fucitons
    ###############################################     
    def _start_scan_button_fired(self):
        from pyface.api import ConfirmationDialog, YES
        dialog = ConfirmationDialog(message= "Are you sure start virtual scan ?",
                                    title = "Confirm Scan Action")
       
               
        choice = dialog.open()
         
        if choice == YES:    
            self.reset_viewers = True # Reset the slice views first
         
            if self.phantom is not None:
                if not self.phantom_elements_check(self.phantom): return 
                if not self.phantom_boundary_check(self.phantom): return     
                if not self.elements_priority_check(self.phantom): return                
                
               
                self._gen_image_data_by_numpy()
                
                #Do the real Scan for elements coordinate to priority of elements
                elements_list =  self.phantom.get_sorted_elements_by_priority()
                
                print "elements_list",elements_list
                
                self._do_virtual_scan(elements_list)
                
                self.ready_for_view = True
               
                self.ready_for_export = True
            
        else:
            print "Cancle the scan action"
            
            
            
    #Do the real virtual scan job ,correspond to elements_list       
    def _do_virtual_scan(self,elements_list):
       
        
        in_image = self.image_data   
       
         
        
        for item in elements_list:
            element = item[1]
         
            hu = self.ed_hu_curve.get_hu_from_edensity(element.re_e_density)
            
            print "element.name = ",element.name, hu
            polydata = element.geometry.get_polydata()
               
          
            tem_image = self._polydata_to_image(in_image,polydata,hu)
            
            in_image = tem_image
        
      
        self.image_data = in_image
      
      
       
        

    #Mask the polydata to volume image with vaiue HU     
    def _polydata_to_image(self,image,polydata,bghu):
        
        print "Do polydata to image "
       
#        #*******************************************
        sphere = tvtk.SphereSource()
        sphere.phi_resolution = 80
        sphere.theta_resolution = 80
        sphere.center = (0,0,0)
        sphere.radius = 30
        sphere.update()        
   
         
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
            
   

    view = View( VGroup(
                    
                     Label("Unit of This Page's Quantity is mm :"),
                     Spring(),
                     VGroup(
                             

                             HGroup(Item('imag_slice_type', 
                                           label='Slice Size',
                                         ),
                                    Spring(),
                              
                                  ),
    
                             
                             '_',
                          
                             HGroup(Item('slice_thickness', 
                                         label='Slice Thickness'),
                                    Spring(),
                                  
                                  ),
                             '_',
                             space,
                             Item('slice_num',
                                  label='Slice Number',
                                  style='readonly'),
                                  
                      
                             HGroup(Item('center_x', 
                                         label='X',
                                         style='readonly',
                                         width = 50),
                                    Item('center_y', 
                                         label='Y',
                                         style='readonly',
                                          width = 50),
                                    Item('center_z', 
                                         label='Z',
                                         style='readonly',
                                         width = 50),
                                   
                                    label = "Center "
                                  
                                  ),
                                  
                             HGroup(Item('spacing_x', 
                                         label='X',
                                       #  style='readonly',
                                         width = 50),
                                    Item('spacing_y', 
                                         label='Y',
                                       #  style='readonly',
                                         width = 50),
                                         
                                 
                                         
                                    label = "Spacing"
                                  
                                  ),
                                
                           
                                  
                             label = "Image Volume Properties",
                             show_border = True,
                            
                                  ),
                       space,
                       HGroup(Item('scanner', 
                                    label='CurrentScanner'),
                              Item('show_curve_button',
                                    show_label= False),
                              
                          ),
                      space,
                      space,
                      VGroup(
                         Item(name='cslogregion',
                                  style ='custom',
                                  show_label= False),
                         HGroup(Spring(),      
                                Spring(),
                            
                                Item('start_scan_button',
                                   show_label= False),
                                Spring())
                            )
                          
                          
                          ),
                            
                             
                 scrollable =True,
                 resizable = True )

   
    

  
if __name__ == "__main__":
   
#     a = PhantomModel()
#     from single_element import SingleElement
#     
#     print "Setup Air Range"
#     selement1 = SingleElement()
#     selement1.setup_geometry('buildin')
#     selement1.tissue_type = 'Air'    
#     
#     selement1.priority = 1
#     
#     
#     
#     print "Setup mask sphere"
#     selement2 = SingleElement()
#     selement2.setup_geometry('buildin')
#     selement2.tissue_type = 'StraitedMuscle'    
#     selement2.priority = 3
#     
#     
#    
#     print "Single Element Bounds: ", selement2.get_bounds()
#
#     a.single_elements = [selement1,selement2]
#     
#  
     
     vscan = VirtualScanModel()
     
     print " vscan.spacing_x " ,vscan.spacing_x
     vscan.files_root = './../config'
 #    vscan.phantom = a
     
     
  
    
  #  path = './../scanners/GE64.txt'
    

     vscan.configure_traits()
   