# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 14:37:11 2011

@author: ZouLian
@Oncology Department
@Sichuan People's Hospital
@Chengdu,Sichuan,China
"""


from traits.api import HasTraits, Event
          


######################################################################

class PhantomUpdateHelper(HasTraits):
    
    phantom_modified = Event
    
    elements_name_modified = Event
   