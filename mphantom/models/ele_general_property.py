# -*- coding: utf-8 -*-
"""
Created on Mon Oct 07 10:35:18 2013

@author: ZouLian
@Joint Lab for Medical Physics
@Oncology Department
@Sichuan People's Hospital
@Chengdu,Sichuan,China

"""


from traits.api import HasTraits, Unicode, Dict, Enum, Float, \
                       Range,Instance,Bool, Tuple,Event
                       
from traitsui.api import View, Item,Readonly,VGroup,Spring


from vtk.util import colors


######################################################################

class EleGeneralProperty(HasTraits):
    '''A help Class for Phantom Element,this contains general properties.
    '''
     
    
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
    
    # Predefined Color for material.
    
    color = Tuple(colors.black)
    
    #Priority of the Element 
    priority = Range(0.0, 10.0) 
    
    
    
    
    
    
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
    material_color_dict = Dict({'Air':colors.black, 
                               
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
                             
                    
                    
                    
    gener_vis_props_changed = Event          
                    
    def get_data_for_json(self):
        '''Get a dict data for json output '''
        data = {}
        
        data["Priority"] = self.priority
        data["RelEDensity"] = self.re_e_density
        data["TissueType"] = self.tissue_type
        
        return data
      
                    
    def _tissue_type_changed(self, value):
        """
        Set the default Relative ElectronDensity and  color based on tissue typle.
        """
        self.re_e_density = self.m_edensity_dict[value]
        
        
        self.color =self.material_color_dict[self.tissue_type]
        
        gener_vis_props_changed = True
        
       # print self.re_e_density, self.color 
                   
                    
       
    
    view = View( VGroup( Item(name='name',
                              label='ElementName',
                              resizable = True), 
                         Spring(),
                         Item(name='tissue_type',
                              label='TissueType',
                              width= 100,
                              resizable = True), 
                         Spring(),
                         Spring(),
                         Readonly(name='re_e_density',
                                  label='ReElectronDensity'),
                         Spring(),
                         Spring(),
                         Item('_'),
                         Spring(),
                         Spring(),
                         Item(name='priority',
                              label='Priority',
                              resizable = True),
                         show_border = True,
                         
                     
                      )
                
                
               )
               
               
   

if __name__ == '__main__':
    a = EleGeneralProperty()
    
    a.configure_traits()

    