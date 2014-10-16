# -*- coding: utf-8 -*-
"""
Created on Mon Oct 07 11:26:21 2013

@author: ZouLian
@Joint Lab for Medical Physics
@Oncology Department
@Sichuan People's Hospital
@Chengdu,Sichuan,China

"""
from traits.api import HasTraits, Enum, Float,Range, Bool,Instance, \
                       on_trait_change, Event

from traitsui.api import View, Item,Readonly,VGroup,Spring,HGroup,Label
from tvtk.api import tvtk

class EleBaseGeometryTuner(HasTraits):
    '''A help Class for Phantom Element,this class refine the geometry properties.
    '''
    current_transform =  Instance(tvtk.LinearTransform) 
    geo_tuner_changed = Event
     
    def __init__(self,**traits):
        super(EleBaseGeometryTuner,self).__init__(**traits)
        self.current_transform = tvtk.IdentityTransform()
    
    def get_data_for_json(self):
        '''Get a dict data for json output '''
        pass  

if __name__ == '__main__':
    a = EleBaseGeometryTuner()
    
    a.configure_traits()

    