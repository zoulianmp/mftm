 # -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 10:03:36 2011

@author: ZouLian
@Oncology Department
@Sichuan People's Hospital
@Chengdu,Sichuan,China
"""

from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'wx'

# Standard library imports.
import logging

# Plugin imports.
from envisage.core_plugin import CorePlugin
from envisage.ui.workbench.workbench_plugin import WorkbenchPlugin


from envisage.developer.developer_plugin import DeveloperPlugin
from envisage.developer.ui.developer_ui_plugin import DeveloperUIPlugin

# Local imports.
from mphantom.api import MPhantomApplication, RunManagerPlugin, \
                         MPhantomUIPlugin,set_element_lib_path
                           

   

def main(argv):
    """ Run the application.
    """
    
    import os
    print os.getcwd() 
    
    logging.basicConfig(level=logging.WARNING)

    plugins = [ CorePlugin(), 
                WorkbenchPlugin(), 
     
                RunManagerPlugin(),
                MPhantomUIPlugin(), ]
                    
              #    DeveloperPlugin(),
               # DeveloperUIPlugin()]
  
  
    app = MPhantomApplication(plugins=plugins)
    

    app.run()
  

    logging.shutdown()


if __name__ == '__main__':
    
    set_element_lib_path(__file__)

    
    import sys
   
    main(sys.argv)
