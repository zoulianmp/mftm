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
                       Range,Instance,Bool, Tuple,Event,File,Str,List
                       
from traitsui.api import View, Item,Readonly,VGroup,Spring,EnumEditor


from vtk.util import colors


######################################################################

class EleGeneralProperty(HasTraits):
    '''A help Class for Phantom Element,this contains general properties.
    '''
     
    materials_list =  File()
    
    name = Unicode('BaseElement') 
         
    EnumEditor
        
    materials_table ={}
    

    tissue_type =Str()
    namelist = List([])
    
    # A simple trait to Set the Element material.
    #tissue_type =  Enum('Air', 
              #         'Lung')
    
#    tissue_type = Enum('Air', 
#                       'Lung', 'LungInhale','LungExhale',              
#                       'AdiposeTissue','BreastTissue',
#                       'Water',
#                       'StraitedMuscle','Muscle','MuscleWithoutSucrose',
#                       'LiverTissue',
#                       'SolidTrabecularBone','SolidDenseBone_1',
#                       'SolidDenseBone_2','Bone','CorticalBone',
#                       'Aluminum','FilmEmulsion',
#                       'Titanium','Iron','Cropper','Molybdenum',
#                       'Lead','Uranium','Tungsten')

    # Relative Electronic Density 
    re_e_density = Float(0.001)
    
    # Predefined Color for material.
    
   #  color = Instance(Tuple(0,0,0))
    color = Tuple(colors.black)
    
    #Priority of the Element 
    priority = Range(0.0, 10.0) 
    
    
    
    
    
    
  
                    
                    
                    
    gener_vis_props_changed = Event          
    
    def __init__(self,**traits):
        super(EleGeneralProperty, self).__init__(**traits)
        
        #Set the default MaterialListFile
        from .util import MATE_LIST_FILE
        #global CFG_PATH
      
        self.materials_list = MATE_LIST_FILE
        self.read_material_list(self.materials_list)
        
     
                    
    def _materials_list_changed(self,old,new): 
         
        print "The Material List Changed to --> ", new
                       
        from .util import update_material_list
                     
        update_material_list(new)
  
  
  
        self.read_material_list(new)
                 
                         
                         
    def read_material_list(self, fname):
        
        self.namelist = []
        self.materials_table = {}
        
        import csv   
        with open(fname, 'rb') as csvfile:
            material_set = csv.DictReader(csvfile) 
              
            for row in material_set:
                name = row["MaterialName"]
                RED =  float(row["RelativeEDensity"])
                clour = (float(row["R"]),float(row["G"]),float(row["B"]))
                
                self.namelist.append(name)
                self.materials_table[name] = (RED,clour)
           
        csvfile.close() 
           
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
        
        self.re_e_density = self.materials_table[value][0]
        #self.re_e_density = self.m_edensity_dict[value]
        
        self.color = self.materials_table[value][1]
       # self.color = self.material_color_dict[self.tissue_type]
        
        self.gener_vis_props_changed = True
        
       # print self.re_e_density, self.color 
                   
                    
       
    
    view = View( VGroup( Item(name='name',
                              label='ElementName',
                              resizable = True), 
                         Spring(),
                         Item(name='materials_list',
                              label='MaterialsList'),
                         Item(name='tissue_type',
                              label='TissueType',
                              width= 100,
                              editor = EnumEditor( name = 'namelist' ), 
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
    
    
    CFG_PATH = "F:\PythonDir\MagicalPhantom\mphantom\config"
    
    a = EleGeneralProperty()
    
    a.configure_traits()

    