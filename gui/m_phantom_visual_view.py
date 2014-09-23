 # Enthought library imports.
from traits.api import Str,Instance
from traitsui.api import View, Item

from mphantom.api import MPhantom
from actors_viewer import ActorsViewer

from tvtk.pyface.scene_model import SceneModel
from tvtk.pyface.scene_editor import SceneEditor


class MPhantomVisualView(ActorsViewer):

    #### 'ITaskPane' interface ################################################

    id = Str('mphantom.3dphantomvisual')
    name =Str('3DPhantomVisual')



    #The Phantom to be Visualization
    phantom = Instance(MPhantom)
    
    
   
    #### Private traits #######################################################
    def __init__(self,**traits):
        super(MPhantomVisualView, self).__init__(**traits)
       
   

    def _phantom_changed(self,new):
       
        self._update_phantom_visual()
        
        
#  
#        if new is not None:         
#            self.phantom.on_trait_event(self._update_phantom_visual,'updated')
#        
#        
#    
#        
      
   
    ###########################################################################
    # Protected interface.
    ###########################################################################

    #### Trait change handlers ################################################

   
    def update_visualization(self):
        self._update_phantom_visual()
   
    def _update_phantom_visual(self):
               
       
        phantom = self.phantom
        
        self.clear_actors()
        
        if  len(phantom.three_dimension_elements) > 0:            
            for selement in phantom.three_dimension_elements:
             
                self.add_actors(selement.geometry.current_actor)
                              
    
    view = View(
                Item(name='scene',  
                     editor=SceneEditor(),
                     show_label=False,
                     resizable=True,
                    ),
                width = 700,
                height = 700
                
                )
              
          
   
####################################

if __name__ == '__main__':
   
    from mphantom.api import CubeGeometry,ConeGeometry,STLFileGeometry, \
                                   ThreeDimensionElement, MPhantom
    
    cube = CubeGeometry()
    #cube.configure_traits()
    
    cone = ConeGeometry()
   # cone.configure_traits()
    
    cube_element = ThreeDimensionElement()
    cube_element.geometry = cube
    cube_element.configure_traits()
    
    
    cone_element = ThreeDimensionElement()
    cone_element.geometry = cone
    cone_element.configure_traits()
   
    phantom = MPhantom()
    
    phantom.add_3d_element(cube_element)
    phantom.add_3d_element(cone_element)
    
    print phantom.get_bounds()
    
    
    vis =  MPhantomVisualView()
    vis.phantom = phantom
   
   
    vis.configure_traits()
    
 
        
       