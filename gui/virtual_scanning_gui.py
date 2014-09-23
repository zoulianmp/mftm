# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 15:08:10 2011

@author: ZouLian
@Oncology Department
@Sichuan People's Hospital
@Chengdu,Sichuan,China
"""
  
  
  
# Enthought library imports.
from traits.api import HasTraits, Instance, DelegatesTo


from tvtk.api import tvtk              

from traitsui.api import View, UItem, HGroup, VGroup,Group, Spring, Item

from mphantom.api import MPhantom, VolumeImageSliceViews,Virtual_CT_Scanner




class VirtualScannningGUI(HasTraits):

    
    scanner = Instance(Virtual_CT_Scanner,()) 
    
    
    phantom  = DelegatesTo('scanner')    
    raw_data =  DelegatesTo('scanner')

    image_viewer = Instance(VolumeImageSliceViews)
    
    active = False
    
   
   
   
    #Init Property Value                   
    def __init__(self,**traits):
        super(VirtualScannningGUI, self).__init__(**traits)
        
        if self.scanner is None :
            self.scanner = Virtual_CT_Scanner()
         
        if self.image_viewer is None:
            self.image_viewer = VolumeImageSliceViews()
        
        self.scanner.on_trait_event(self._feed_image_to_viewer,'ready_for_view')
        self.scanner.on_trait_event(self.image_viewer.reset_slice_views,'reset_viewers')
        
    

    def _feed_image_to_viewer(self):
        
        if self.image_viewer is None:
            self.image_viewer = VolumeImageSliceViews()
   
        self.image_viewer.volume = self.raw_data[0]
        
            


    view = View(
                HGroup(
                       UItem('scanner',
                             style='custom',
                             padding =8),    
                                      
                                                         
                                 
                       UItem('image_viewer',
                              style='custom',
                              padding =5)
                    ),
                scrollable = False,          
                resizable = True )

                

  
if __name__ == "__main__":
    from mphantom.api import CubeGeometry,ConeGeometry, ThreeDimensionElement
    cube = CubeGeometry()
  
    cone = ConeGeometry()
  
    cube_element = ThreeDimensionElement()
    cube_element.geometry = cube
    
    
    cone_element = ThreeDimensionElement()
    cone_element.geometry = cone
    
    phantom = MPhantom()
    
    phantom.add_3d_element(cube_element)
    phantom.add_3d_element(cone_element)

    volumes = [tvtk.ImageData()]
    
    
    gui = VirtualScannningGUI(phantom= phantom, raw_data= volumes)
    
    gui.configure_traits()
