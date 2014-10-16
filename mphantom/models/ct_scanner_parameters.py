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
                       Bool, on_trait_change,Trait

from traitsui.api import View, Item, VGroup, HGroup,Spring,Label,ImageEnumEditor
from e_density_hu_curve import EDensityHUCurve

from tvtk.api import tvtk
from vtk.util import vtkConstants

from pyface.api import ImageResource
from math import ceil

import os
       


class CT_Scanner_Parameters(HasTraits): 
    
    enable_4d = Bool(False)
    #Electronic Density to HU Transform Curves Interface    
    ed_hu_files = List(Str)  
    scanner_names = List(Str)
    
    scanner =Enum(values='scanner_names')
    show_curve_button = Button(label = 'Show ED-HU Curve')    
    ed_hu_curve = Instance(EDensityHUCurve)


    
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
    
    slice_thickness = Float(5) #The spacing_z value
    
 
    
    slice_num = Int()
   
    
    dev_root = 'F:/PythonDir/mphantom/'
    run_root =  os.getcwd() + '/mphantom/'
    
 
    dev_image_path = os.path.join(dev_root,'gui/images') 
    #the Coordinate for scanner
    
    run_image_path = os.path.join(run_root,'gui/images') 
    
    print "run_image_path:",run_image_path
   
    
    dev_scatter_path = os.path.join(dev_root,'config/scanner') 
    #the Coordinate for scanner
    
    run_scatter_path = os.path.join(run_root,'config/scanner') 

    
     
    cslogregion = Button(image= ImageResource('cslog.png',search_path=[dev_image_path,run_image_path]))
    
    
  
    
    
    def __init__(self,**traits):       
        super(CT_Scanner_Parameters,self).__init__(**traits)
        self._setup_scanners()
        if len(self.ed_hu_files) > 0:
            self.ed_hu_curve = EDensityHUCurve(path = self.ed_hu_files[0] )
        else:
            self.ed_hu_curve = EDensityHUCurve()
    ###############################################
    ########## File Related funcitons
    ###############################################    
    def _setup_scanners(self):
        if os.path.exists(self.dev_scatter_path):
             #print "setup scanners:  ", self.dev_scatter_path
             self._get_ed_hu_files(self.dev_scatter_path)
             self.ed_hu_curve = EDensityHUCurve(path = self.ed_hu_files[0] )
        elif os.path.exists(self.run_scatter_path):
             self._get_ed_hu_files(self.run_scatter_path)
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
            
       
    
    
    
    

    view = View( VGroup(
    
                    
                     Label("Unit of This Page's Quantity is mm :"),
                     Spring(),
                     VGroup( Item('enable_4d',
                                  label ='Enable 4D Scan'),
                             '_',
                             
                             HGroup(Item('imag_slice_type', 
                                           label='Slice Size',
                                         ),
                                    Item('slice_thickness', 
                                         label='Slice Thickness'),
                              
                                  ),
    
                             '_',
                             
                             Item('slice_num',
                                  label='Total Slices',
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
                       
                       HGroup(Item('scanner', 
                                    label='CurrentScanner'),
                              Item('show_curve_button',
                                    show_label= False),
                              
                          ),
                       Item(name='cslogregion',
                            style ='custom',
                            show_label= False),
                   
                      )
                      )





  
if __name__ == "__main__":
   
   
    pa =  CT_Scanner_Parameters()
    
    print "before assign to root_path"
    pa.root_path = "F:\PythonDir\DicomSolution\mphantom"
    
    print "rootpath" ,pa.root_path
    
    pa.configure_traits()
