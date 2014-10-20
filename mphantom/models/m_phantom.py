# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 14:37:11 2011

@author: ZouLian
@Oncology Department
@Sichuan People's Hospital
@Chengdu,Sichuan,China
"""

try:
    import vtk
except ImportError,m:
    m.args = ('%s\n%s\nDo you have vtk and its Python bindings installed properly?'%
                       (m.args[0],'_'*80),)

from traits.api import HasTraits, Instance,  List, Unicode, Event, \
                       on_trait_change, Str, Enum, Any, Int, DelegatesTo, \
                       Tuple
                       
from traitsui.api import View, Item, Spring, Group

from base_element import BaseElement
from three_dimension_element import ThreeDimensionElement

from mphantom.api import PhantomUpdateHelper,message_box
from mphantom.api import  ConeGeometry, CubeGeometry, CylinderGeometry, \
                          SphereGeometry, STLFileGeometry, VTKFileGeometry


######################################################################

class MPhantom(HasTraits):
    '''
    A 3D Phantom Model Class for Phantom Construction and CTScanner Output
    '''
    name = Str('3DVirtualPhantom')
    
    elements_ids= List(Str)
    
    helper = PhantomUpdateHelper()
    
    phase_index = Int(0)  #Used for 4DPhantom,The Motion phase
    
    phantom_type= Enum('3DPhantom','4DPhanotm','DeformablePhantom')   
    
    #The Single elements list 
    three_dimension_elements = List(BaseElement)
    
    four_dimension_elements = List(BaseElement)
    
    #Current Selected Element
    current_element = Instance(BaseElement)  
 
    
    #Flag the Phantom  is updated
    updated = Event
     
    def __init__(self):
        super(MPhantom, self).__init__()
        self.three_dimension_elements = []
        self.four_dimension_elements = [] 
        self.helper.on_trait_event(self.trig_updated,'phantom_modified')
        
        
          
    
    def trig_updated(self):
        
        self.updated = True
        
    def clear_phantom(self):
        
        self.elements_ids = []
        self.three_dimension_elements = []
        self.four_dimension_elements = []
        self.current_element = None
        
        
        
    def element_name_exist(self,element) :
          
        if element.name in self.elements_ids:
            message_box(message="The Element is Already Exist,Please Assign a New Name to New Element",
                                   title="Failure of Elements' Name Check", severity='error')
            return True
        else :         
            self.elements_ids.append(element.name)
            return False
            
            
            
        
        
                
    def add_3d_element(self,element):
        element.helper = self.helper
      
        if self.element_name_exist(element): return      
         
        self.three_dimension_elements.append(element)
        
        
        self.current_element = element
        
        self.updated = True
        
    
    def remove_3d_element(self,element):
        
        self.elements_ids.remove(element.name)
        
        self.three_dimension_elements.remove(element)
        
      
        if len(self.three_dimension_elements)>0 :
            self.current_element = self.three_dimension_elements[0]
        else :
            self.current_element = None
          
        
        self.updated = True
   
    def save_phantom(self, fname):
        """Given  a file name, this saves the current phantom to the 
        file as Json format.
        """
        data = {}
        
        
        data["Name"] = self.name       
        data["Type"] = self.phantom_type 
        
        data["CurrentElementIndex"] = self.get_current_element_Index()
        
        data["3DElementsSet"] = []
        
        if self.phantom_type == "3DPhantom":
            for element in self.three_dimension_elements:
                ele_json = element.get_data_for_json()
                data["3DElementsSet"].append(ele_json)
        
        
        
        elif self.phantom_type == "4DPhanotm":
            data["4DElementsSet"] = []
            for element in self.four_dimension_elements:
                ele_json = element.get_data_for_json()
                data["4DElementsSet"].append(ele_json)
        
                       
        
        import json        
        with open(fname, 'w') as outfile:  
            json.dump(data,outfile,sort_keys=True,indent=3)
    
    
    
    
    
      
    
    
    def pars_3d_geometry(self,geo_json2dict):
        
        geo_type = geo_json2dict["GeoType"]
        
        inits = geo_json2dict["InitialParams"]
           
        
        if geo_type == "Cone" :
           geometry =  ConeGeometry(angle = inits[0],
                                    center_x = inits[1],
                                    center_y = inits[2],
                                    center_z = inits[3],
                                    direction_x = inits[4],
                                    direction_y = inits[5],
                                    direction_z = inits[6],
                                    height = inits[7],
                                    radius = inits[8],
                                    resolution = inits[9]        
                                   )        
           
           return geometry
            
        elif geo_type == "Cube" :            
            geometry =  CubeGeometry(center_x = inits[0],
                                     center_y = inits[1],
                                     center_z = inits[2],
                                     length_x = inits[3],
                                     length_y = inits[4],
                                     length_z = inits[5]
                                    )   
           
            return geometry
            
        
        
        elif geo_type == "Cylinder" :          
            geometry =  CylinderGeometry(center_x = inits[0],
                                         center_y = inits[1],
                                         center_z = inits[2],
                                         height =  inits[3],
                                         radius =  inits[4],
                                         resolution =  inits[5]
                                        )
           
            return geometry
            
                                        
             
                          
        elif geo_type == "Sphere" :
            geometry =  SphereGeometry(radius = inits[0],
                                       center_x = inits[1],
                                       center_y = inits[2],
                                       center_z = inits[3])
            
            return geometry 
        
        
        elif geo_type == "VTKExternalFile" :
            geometry =  VTKFileGeometry(external_file_name = inits)
                  
            return geometry 
            
        
        
        elif geo_type == "STLExternalFile" :
            geometry =  STLFileGeometry(external_file_name = inits)
                    
            return geometry 
     
        else :
            print "The Geometry Type is not supported by MPhantom"                
                
        
               
        
    
    def parse_3d_element(self,ele_json2dict):
        
        genal_paras = ele_json2dict["GeneralParams"]

        vis_paras = ele_json2dict["VisParams"]

        geo_paras = ele_json2dict["GeometryParams"]

        tunner_paras =  ele_json2dict["GeoTunerParams"]
        
        
        
        ele_3d = ThreeDimensionElement()
        
        
        ele_3d.name = ele_json2dict["EleName"]
        
        
        ele_3d.geometry = self.pars_3d_geometry(geo_paras)
        
        
        
        
       
        ele_3d.general.tissue_type = genal_paras["TissueType"]
        ele_3d.general.priority = genal_paras["Priority"]
        ele_3d.general.re_e_density = genal_paras["RelEDensity"]
    
        
        ele_3d.visual.color =  vis_paras["Color"]
        ele_3d.visual.opacity = vis_paras["Opacity"]
        ele_3d.visual.representation = vis_paras["Representation"]
        ele_3d.visual.visibility =  vis_paras["Visibility"]
        
      
        
        ele_3d.geometry_tuner.shift_x = tunner_paras[0]
        ele_3d.geometry_tuner.shift_y = tunner_paras[1]
        ele_3d.geometry_tuner.shift_z = tunner_paras[2]
        
        ele_3d.geometry_tuner.rotate_x = tunner_paras[3]
        ele_3d.geometry_tuner.rotate_y = tunner_paras[4]
        ele_3d.geometry_tuner.rotate_z = tunner_paras[5]
        
        ele_3d.geometry_tuner.scale_x = tunner_paras[6]
        ele_3d.geometry_tuner.scale_y = tunner_paras[7]
        ele_3d.geometry_tuner.scale_z = tunner_paras[8]
        
          
        
        return ele_3d
        
        
   
        
     
    def load_phantom(self,fname):
        """Given a file name, this load the  phantom ."""
             
        self.clear_phantom()
        
        
        import json      
        with open(fname,'r') as infile:
            data = json.load(infile)
            
    
        self.name = data["Name"]
        
        self.phantom_type =data["Type"]
         
        
        for jsonele in data["3DElementsSet"]:
            element = self.parse_3d_element(jsonele)
            element.helper = self.helper
             
            self.add_3d_element(element)  #Add three-d elements and element names
            
            #self.three_dimension_elements.append(element) 
        
      
        self.set_current_element_by_Index(data["CurrentElementIndex"])
        
        self.updated = True
          
          
          
          
    def set_current_element_by_Index(self,Index):               
        index_table = [self.three_dimension_elements,self.four_dimension_elements]       
        list_id = Index[0]
        ele_id = Index[1]    
        self.current_element = index_table[list_id][ele_id]
        
         
    def get_current_element_Index(self):
               
        if self.current_element in self.three_dimension_elements:
            list_id = 0
            ele_id = self.three_dimension_elements.index(self.current_element)
            
            index = [list_id,ele_id]
            
            return index
            
        if self.current_element in self.four_dimension_elements:
            list_id = 1
            ele_id = self.four_dimension_elements.index(self.current_element)
            
            index = [list_id,ele_id]
            
            return index
             
             
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
    
      
    #Get the sorted elements by priority
    #The higher priority ,the fronter position of element
    def get_sorted_elements_by_priority(self):
        
        from collections import OrderedDict
        
        e_dict = { }
  
        for element in self.three_dimension_elements:
            key = element.general.priority 
            e_dict[key] = element
               
         
        for element in self.four_dimension_elements:
            key = element.general.priority 
            e_dict[key] = element
             
        
        # dictionary sorted by key
        orddict = OrderedDict(sorted(e_dict.items(), key=lambda t: t[0])) 
        #orddict = OrderedDict(sorted(e_dict.items(), key=lambda t: t[0],reverse=True)) 
       
        items = orddict.items()
        
        
        return orddict.items()
        




      
    #Get the Phantom Bounds          
    def get_bounds(self):
        
        xmin = 0
        xmax = 0
        
        ymin = 0
        ymax = 0

        zmin = 0
        zmax = 0
        
        if len(self.three_dimension_elements) >0:
            bounds = self.three_dimension_elements[0].get_bounds()
            xmin = bounds[0]
            xmax = bounds[1]
        
            ymin = bounds[2]
            ymax = bounds[3]

            zmin = bounds[4]
            zmax = bounds[5]
    
        else:
            return              
        
        #Iterating the three dimension elements
        for element in self.three_dimension_elements:
            tbounds = element.get_bounds()
            
            if tbounds[0] < xmin :
                xmin = tbounds[0]
            
            if tbounds[1] > xmax :
                xmax = tbounds[1]
                
            if tbounds[2] < ymin :
                ymin = tbounds[2]
                
            if tbounds[3] > ymax :
                ymax = tbounds[3]
                
            if tbounds[4] < zmin :
                zmin = tbounds[4]
                
            if tbounds[5] > zmax :
                zmax = tbounds[5]
              
              
        #Iterating the four dimension elements     
        
  
        bounds = (xmin,xmax,ymin,ymax,zmin,zmax)
        
        return bounds
            
        
        
        
    
    ######################
    

if __name__ == '__main__':

    from mphantom.api import CubeGeometry,ConeGeometry,STLFileGeometry
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
    
  
    print "the Phantom Bounds: ",phantom.get_bounds()
    
    
    
    print phantom.three_dimension_elements
    
    
    
    
    
    
    
    
    
  