""" The MagicalPhantom UI plugin. """


# Enthought library imports.
from envisage.api import Plugin
from pyface.workbench.api import Perspective, PerspectiveItem
from pyface.workbench.api import TraitsUIView
from traits.api import List

#Local Import 
from mphantom.api import RunManager, Virtual_CT_Scanner

from mphantom.api import StartUpVisualView,VirtualScannningGUI, PhantomFactoryGUI
                        



#-------------------------------------------------------------------
#            Set Up Application Perspectives
#-------------------------------------------------------------------
class StartupPerspective(Perspective):
    """ A perspective When the MagicalPhantom startup """

    name             = 'Startup'
    show_editor_area = False

    contents = [
                  PerspectiveItem(id='mphantom.startup',
                                  position='right')
               ]



class PhantomConfigPerspective(Perspective):
    """ A perspective containing the MagicalPhantom Construction views. """

    name             = 'PhantomConfig'
    show_editor_area = False

    contents = [           
                PerspectiveItem(id='mphantom.phantomfactory',
                                position='right')
               ]



class VirtualScanPerspective(Perspective):
    """ A perspective containing the default Phantom Virtual views. """

    name             = 'VirtualScan'
    show_editor_area = False

    contents = [
                PerspectiveItem(id='mphantom.virtualscanning',
                                position='right'
                                )
               ]





class MPhantomUIPlugin(Plugin):
    """ The MagicalPhantom UI plugin.

    This plugin is part of the  MagicalPhantom application.

    """

    # Extension points Ids.
    PERSPECTIVES   = 'envisage.ui.workbench.perspectives'
    VIEWS          = 'envisage.ui.workbench.views'
    ACTION_SETS    = 'envisage.ui.workbench.action_sets'

    #### 'IPlugin' interface ##################################################

    # The plugin's unique identifier.
    id = 'magicalphantom.ui.plugin'

    # The plugin's name (suitable for displaying to the user).
    name = 'MagicalPhantom UI'

    #### Contributions to extension points made by this plugin ################

    # Perspectives.
    perspectives = List(contributes_to=PERSPECTIVES)

    def _perspectives_default(self):
        """ Trait initializer. """

        return [StartupPerspective,PhantomConfigPerspective,VirtualScanPerspective]

     #   return [StartupPerspective,PhantomConfigPerspective,VirtualScanPerspective]

      
    # Views.
    views = List(contributes_to=VIEWS)

    def _views_default(self):
        """ Trait initializer. """
        
        startup_view = self._create_startup_view
        factory_view = self._creat_phantom_factory_view
        
        scanning_view = self._creat_virutal_scanning_view
                
        return [startup_view,factory_view,scanning_view ]
        
    # Actions
    action_sets = List(contributes_to=ACTION_SETS)
    
    def _action_sets_default(self):
        from startup_ui_action_set import StartupUIActionSet
        from phantom_config_ui_action_set import PhantomConfigUIActionSet
        from virtual_scanner_ui_action_set import VirtualScannerUIActionSet
        
        return [StartupUIActionSet,PhantomConfigUIActionSet]
        #,VirtualScannerUIActionSet]
  
        
        

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _create_startup_view(self, **traits):
         
         startup_view = TraitsUIView(
            id   = 'mphantom.startup',
            name = 'Start Up Show',
            obj  = StartUpVisualView(),
            **traits
         )
        
         return startup_view
        




    def _creat_phantom_factory_view(self, **traits):
        
       
        run_manager = self.application.get_service('mphantom.api.RunManager')
        
        print run_manager         
        
        phantom = run_manager.model
        
        
        factory_view = TraitsUIView(
            id   = 'mphantom.phantomfactory',
            name = 'Phantom Factory',
            obj  = PhantomFactoryGUI(phantom= phantom),
            **traits
        )
        
        return factory_view

   
        
    def _creat_virutal_scanning_view(self, **traits):
         
          
        run_manager = self.application.get_service('mphantom.api.RunManager')
        
          
        #Initialize the scanning gui for bind the RunManager's Scanner,phantom,rawdata  
        scanning_gui = VirtualScannningGUI(scanner =  run_manager.scanner )                                                                              
                                        
    
        
            
        virtul_scanner_view = TraitsUIView(
            id   = 'mphantom.virtualscanning',
            name = 'Virtual Scanning View',
            obj  = scanning_gui,
            **traits
        ) 
        
        return virtul_scanner_view
        
        
   
        
    #### Trait event handlers #################################################

        

#### EOF ######################################################################
