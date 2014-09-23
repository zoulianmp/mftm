# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 10:52:41 2011

@author: ZouLian
@Oncology Department
@Sichuan People's Hospital
@Chengdu,Sichuan,China
"""


# Enthought library imports.
from envisage.api import Plugin, ServiceOffer
from traits.api import List, Str

from traits.api import HasTraits, List

from mphantom.api import MPhantom
from tvtk.api import tvtk


class DataServer (HasTraits):
    model = MPhantom()   
    raw_data = List(tvtk.ImageData())

    dev_root = Str()
    run_root = Str()
    
    dev_image_path = Str()
    
    run_image_path = Str()
    
    
       
       
    def __init__(self,**traits):       
        super(DataServer,self).__init__(**traits)
      
        import os

        self.dev_root = 'F:/PythonDir/DicomSolution/mphantom/gui'
        self.run_root =  os.getcwd()
     
        self.dev_image_path = os.path.join(self.dev_root,'images') 
        #the Coordinate for scanner
        
        self.run_image_path = os.path.join(self.run_root,'images') 
       
    



class DataServerPlugin(Plugin):

    #### Contributions to extension points made by this plugin ################
    """
    The Magical Phantom plugin.
    This plugin is part of the 'MagicalPhantom'  application.

    """

    # Extension points Ids.
    SERVICE_OFFERS = 'envisage.service_offers'

    #### 'IPlugin' interface ##################################################

    # The plugin's unique identifier.
    id = 'magical_phantom'

    # The plugin's name (suitable for displaying to the user).
    name = 'MagicalPhantom'

    #### Contributions to extension points made by this plugin ################

    # Service offers.
    service_offers = List(contributes_to=SERVICE_OFFERS)

    def _service_offers_default(self):
        """ Trait initializer. """

        data_service_offer = ServiceOffer(
             protocol = 'mphantom.api.DataServer',
             factory  = 'mphantom.api.DataServer'
        )

        return [data_service_offer]

#### EOF ######################################################################

                             
          
####################################

if __name__ == '__main__':
    dataserver = DataServer()
    
    print dataserver.model
    
    print dataserver.raw_data


