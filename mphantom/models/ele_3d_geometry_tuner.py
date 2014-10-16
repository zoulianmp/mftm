# -*- coding: utf-8 -*-
"""
Created on Mon Oct 07 11:26:21 2013

@author: ZouLian
@Joint Lab for Medical PhysicsEle3DGeometryTuner
@Oncology Department
@Sichuan People's Hospital
@Chengdu,Sichuan,China

"""
from traits.api import HasTraits, Enum, Float,Range, Bool,Instance, \
                       on_trait_change, Event

from traitsui.api import View, Item,Readonly,VGroup,Spring,HGroup,Label
from tvtk.api import tvtk
from ele_base_geometry_tuner import EleBaseGeometryTuner

class Ele3DGeometryTuner(EleBaseGeometryTuner):
    '''A help Class for Phantom Element,this class refine the geometry properties.
    '''
  
    # Geometry Shift alone x,y,z Aixes
     
    shift_x = Float(0.0)
    shift_y = Float(0.0)
    shift_z = Float(0.0)
    
    #Geometry Rotation about x,y,z Aixes
    rotate_x = Float(0.0) 
    rotate_y = Float(0.0) 
    rotate_z = Float(0.0) 
    
    #Geometry Scale alone x,y,z Aixes
    
    scale_x = Float(1.0) 
    scale_y = Float(1.0) 
    scale_z = Float(1.0) 
    
    
    
#    
#    axial = vtk.vtkMatrix4x4()
#    axial.DeepCopy((1, 0, 0, center[0],
#                   0, 1, 0, center[1],
#                   0, 0, 1, center[2],
#                   0, 0, 0, 1))
#    
    
    def __init__(self,**traits):
        super(Ele3DGeometryTuner,self).__init__(**traits)
    
    @on_trait_change('shift+, rotate+, scale+')
    def generate_current_transform(self):
        self.current_transform = tvtk.Transform()
        self.current_transform.post_multiply()
        
        self.current_transform.translate(self.shift_x,self.shift_y,self.shift_z)
        self.current_transform.rotate_x(self.rotate_x)
        self.current_transform.rotate_y(self.rotate_y)
        self.current_transform.rotate_z(self.rotate_z)
        self.current_transform.scale(self.scale_x,self.scale_y,self.scale_z)
        
        
        self.geo_tuner_changed = True
    
    def get_data_for_json(self):
        '''Get a dict data for json output '''
        data = [self.shift_x, self.shift_y, self.shift_z,
                self.rotate_x,self.rotate_y,self.rotate_z,
                self.scale_x, self.scale_y, self.scale_z]
        
        return data
        
        
        
        
        
        
        
    
    
    view = View( 
                 Label("The Initial Position is (0,0,0) "),
                 VGroup(
                        
                        HGroup(Item('shift_x', 
                                    label='X',
                                    width = 30,
                                    resizable = True),
                               Item('shift_y', 
                                    label='Y',
                                    width = 30,
                                    resizable = True),
                              Item('shift_z', 
                                    label='Z',
                                    width = 30,
                                    resizable = True),
                             label = "Shift (mm)   " ),
                         Spring(),  
                         Spring(),    
                         HGroup(Item('rotate_x', 
                                    label='X',
                                    width =30,
                                    resizable = True),
                               Item('rotate_y', 
                                    label='Y',
                                    width = 30,
                                    resizable = True),
                              Item('rotate_z', 
                                    label='Z',
                                    width = 30,
                                    resizable = True),
                             label = "Rot(degree)" ),
                        Spring(),     
                        Spring(),  
                        HGroup(Item('scale_x', 
                                    label='X',
                                    width = 30,
                                    resizable = True),
                               Item('scale_y', 
                                    label='Y',
                                    width = 30,
                                    resizable = True),
                              Item('scale_z', 
                                    label='Z',
                                    width = 30,
                                    resizable = True),
                
                             label = " Scale          " ),      
                        show_border = True,
                        ),
               
               )
                              
     

if __name__ == '__main__':
    a = Ele3DGeometryTuner()
    
    a.configure_traits()
    
  
    
    
    

    print a.current_transform
 
   
    