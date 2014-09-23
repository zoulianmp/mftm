 # -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 14:37:11 2011

@author: ZouLian
@Oncology Department
@Sichuan People's Hospital
@Chengdu,Sichuan,China
"""

from traits.api import HasTraits, Unicode, Dict, Enum, Float,Range,Instance,Bool
from traitsui.api import View, Item,Readonly,VGroup,Tabbed

from tvtk.api import tvtk
from vtk.util import colors


from tvtk.pyface import actors

#local import 
from base_geometry import BaseGeometry


######################################################################
'''
A Based Class for Phantom Construction Element
'''
class BaseElement(HasTraits):
    
    
    #**********************************************************
    #Public Data interface
    #**********************************************************
    
    
    name = Unicode('BaseElement') 
    
    
    # A simple trait to Set the Element material.
    tissue_type = Enum('Air', 
                       'Lung', 'LungInhale','LungExhale',              
                       'AdiposeTissue','BreastTissue',
                       'Water',
                       'StraitedMuscle','Muscle','MuscleWithoutSucrose',
                       'LiverTissue',
                       'SolidTrabecularBone','SolidDenseBone_1',
                       'SolidDenseBone_2','Bone','CorticalBone',
                       'Aluminum','FilmEmulsion',
                       'Titanium','Iron','Cropper','Molybdenum',
                       'Lead','Uranium','Tungsten')

    # Relative Electronic Density 
    re_e_density = Float(0.001)
    
    #Priority of the Element 
    priority = Range(0.0, 10.0) 
    
    
    #**********************************************************
    #Protected Data interface
    #**********************************************************
    #Property in visualization for element
    element_prop =Instance(tvtk.Property)
    
    # Predefinded Material Relative Electronic Dict
    m_edensity_dict = Dict( {'Air':0.001, 
                             
                             'Lung':0.294, 
                             'LungInhale':0.190,
                             'LungExhale':0.489,      
                             
                             'AdiposeTissue':0.926,                                                    
                             'BreastTissue':0.976,                          
                             
                             'Water':1.000,
                             
                             'StraitedMuscle':1.031,
                             'Muscle':1.043,                             
                             'MuscleWithoutSucrose':1.060,
                             
                             'LiverTissue':1.052,                             
                             
                             'SolidTrabecularBone':1.117,
                             'SolidDenseBone_1':1.456,
                             'SolidDenseBone_2':1.695,
                             'Bone':1.506,
                             'CorticalBone':1.737,
                             
                             
                             'Aluminum':2.345,
                             'FilmEmulsion':3.180,
                             'Titanium':3.759,
                             'Iron':6.592,
                             'Cropper':7.366,
                             'Molybdenum':8.059,
                             'Lead':8.092,
                             'Uranium':13.194,
                             'Tungsten':13.994})
                        
    # Predefinded Material Relative Electronic Dict
    element_color_dict = Dict({'Air':colors.black, 
                               
                               'Lung':colors.grey,              
                               'LungInhale':colors.light_grey,
                               'LungExhale':colors.slate_grey,
                             
                               
                               'AdiposeTissue':colors.yellow_light,
                               'BreastTissue':colors.brown_madder,
                               
                               'Water':colors.blue,
                               
                               'StraitedMuscle':colors.orange,
                               'Muscle':colors.dark_orange,
                               'MuscleWithoutSucrose':colors.cadmium_orange,
                               
                               'LiverTissue':colors.orange_red,
                               
                              
                               
                               'SolidTrabecularBone':colors.mint_cream,
                               'SolidDenseBone_1':colors.eggshell,
                               'SolidDenseBone_2':colors.seashell,
                               'Bone':colors.honeydew,
                               'CorticalBone':colors.white_smoke,
                               
                               
                               'Aluminum':colors.chocolate,
                               'FilmEmulsion':colors.banana,
                               'Titanium':colors.cyan,
                               'Iron':colors.red,
                               'Cropper':colors.green,
                               'Molybdenum':colors.flesh,
                               'Lead':colors.violet,
                               'Uranium':colors.goldenrod_dark,
                               'Tungsten':colors.melon})
    
    
    #The geometry of current element    
    geometry = Instance(BaseGeometry)
 
    #Element Actor for Show 
    current_element_actor = Instance(tvtk.Actor)
    
    
    #The switch for Splash Element
    splash_switch = Bool(True)
    

    ######################
    
    tab1 = VGroup( Item(name='tissue_type',
                           label='TissueType'), 
                      Readonly(name='re_e_density',
                           label='ReElectronDensity'),
                      Item('_'),
                      Item(name='priority',
                           label='Priority'), 
                      label= 'PhysicParameters ')
    tab2= VGroup(Item(name='element_prop',
                           style='custom',
                           show_label =False),
                 label = 'VisualProp')
                      
    
    view = View(Tabbed( tab1,
                        tab2)          
               )
    
    
    def __init__(self):
        super(BaseElement, self).__init__()
        
       #Set the default Relative ElectronDensity and Default VisualProperty
        color = self.element_color_dict[self.tissue_type]
        
     #   print  '%s %s' %(self.tissue_type,color)
 
        self.element_prop = tvtk.Property(color=color)
        
       
 
    ####################################
    # Private traits.
  
    def _tissue_type_changed(self, value):
        self.re_e_density = self.m_edensity_dict[value]
        
        #Set the default Relative ElectronDensity and Default VisualProperty
        newcolor = self.element_color_dict[self.tissue_type]
     
        self.element_prop.color = newcolor
        
   

    ########################################################
    #Set up the Real Geometry Chain 
    def setup_geometry(self):
        pass
       
       
    #Show the default splash Element
    def _show_splash(self):
        pass
    
    #Get the Element's geometry bounds                      
    def get_bounds(self):
   
        if self.geometry is not None:
            bounds = self.geometry.get_bounds()
            return bounds
    
    
    
    #mask the inimage by the element's geometry ,and fill the 
    #inimage by bgvalue on the voxels in the element's geometry
    #range
    def mask_image_by_geometry(self,inimage,bgvalue):
        pass
        
    

if __name__ == '__main__':
    a = BaseElement()
    
    a.configure_traits()
