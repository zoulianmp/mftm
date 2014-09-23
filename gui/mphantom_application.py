# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 09:25:45 2011

@author: ZouLian
@Oncology Department
@Sichuan People's Hospital
@Chengdu,Sichuan,China
"""

# Enthought library imports.




# Standard library imports.
from logging import DEBUG

# Enthought library imports.
from envisage.ui.workbench.api import WorkbenchApplication
from pyface.api import AboutDialog, ImageResource, SplashScreen



class MPhantomApplication(WorkbenchApplication):
    """ The  Magical Phantom Tasks application.
    """
    #### 'IApplication' interface ###########################################

    # The application's globally unique identifier.
    id = 'mphantom_app'
    
    # Branding information.
    #
    # The icon used on window title bars etc.
    icon = ImageResource('magicalphantom.ico')


    # The application's user-visible name.
    name = 'MagicalPhantom'
    
    ###########################################################################
    # 'WorkbenchApplication' interface.
    ###########################################################################

    def __init__(self,**traist):
        super(MPhantomApplication, self).__init__(**traist)
        
           
       # print "self.gui", self.gui.window
       # self.window.active_perspective = self.window.perspectives[0]

 



    def _about_dialog_default(self):
        """ Trait initializer. """

        about_dialog = AboutDialog(
            parent = self.workbench.active_window.control,
            image  = ImageResource('about')
        )

        return about_dialog

    def _splash_screen_default(self):
        """ Trait initializer. """

        splash_screen = SplashScreen(
            image             = ImageResource('splash'),
            show_log_messages = True,
            log_level         = DEBUG
        )

        return splash_screen

#### EOF ######################################################################



   
