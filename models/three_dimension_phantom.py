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
                       on_trait_change, Str
                       
from traitsui.api import View, Item, Spring, Group

from base_element import BaseElement
from three_dimension_element import ThreeDimensionElement


######################################################################

class MPhantom(HasTraits):
    '''
    A 3D Phantom Model Class for Phantom Construction and CTScanner Output
    '''
    name = Str('3DVirtualPhantom')
    
    phantom_type= Unicode('3DPhantom')   
    
    #The Single elements list 
    three_dimension_elements = List()
    
    #Current Selected Element
    current_element = Instance(BaseElement)
    
    #Flag the Phantom  is updated
    updated = Event
     
    def __init__(self):
        super(ThreeDimensionPhantom, self).__init__()
        self.three_dimension_elements = []
                
                
    def add_3d_element(self,element):
        self.three_dimension_elements.append(element)
        self.current_element = element
    
    def remove_3d_element(self,element):
        self.three_dimension_elements.remove(element)
        self.current_element = self.three_dimension_elements[0]
        
        
   
    def save_phantom(self, file_or_fname):
        """Given a file or a file name, this saves the current phantom to the 
        file.
        """
        pass
     
    def load_phantom(self,file_or_fname):
        """Given a file or a file name, this load the  phantom ."""
        pass
     
     
    
      
    #Get the sorted elements by priority
    #The higher priority ,the fronter position of element
    def get_sorted_elements_by_priority(self):
        
        from collections import OrderedDict
        
        e_dict = { }
  
        for element in self.three_dimension_elements:
            key = element.priority 
            e_dict[key] = element
               
#         
#        for element in self.compound_elements:
#            key = element.priority 
#            e_dict[key] = element
#             
        
        # dictionary sorted by key
        orddict = OrderedDict(sorted(e_dict.items(), key=lambda t: t[0])) 
        #orddict = OrderedDict(sorted(e_dict.items(), key=lambda t: t[0],reverse=True)) 
       
        
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
#     
        else:
            return              
        
        #Iterating the single elements
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
  
        bounds = (xmin,xmax,ymin,ymax,zmin,zmax)
        
        return bounds
            
        
        
        
    
    ######################
    

if __name__ == '__main__':

    from MagicalPhantom.api import CubeGeometry,ConeGeometry,STLFileGeometry
    cube = CubeGeometry()
    cube.configure_traits()
    
    cone = ConeGeometry()
    cone.configure_traits()
    
    cube_element = ThreeDimensionElement()
    cube_element.geometry = cube
    cube_element.configure_traits()
    
    
    cone_element = ThreeDimensionElement()
    cone_element.geometry = cone
    
    phantom = ThreeDimensionPhantom()
    
    phantom.add_3d_element(cube_element)
    phantom.add_3d_element(cone_element)
    
  
    print "the Phantom Bounds: ",phantom.get_bounds()
    
    
    
    print phantom.three_dimension_elements
    
    
    
    
    
    
    
    
    
  