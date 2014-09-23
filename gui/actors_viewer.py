"""A very silly example of using a scene editor.  More complex examples are
available in mayavi.  """

# Author: Prabhu Ramachandran <prabhu [at] aero.iitb.ac.in>
# Copyright (c) 2007, Enthought, Inc.
# License: BSD Style.

from traits.api import HasTraits, Enum, Instance, Any
from traitsui.api import View, Item
from tvtk.pyface.scene_model import SceneModel
from tvtk.pyface.scene_editor import SceneEditor
from tvtk.pyface import actors
from tvtk.api import tvtk


######################################################################
class ActorsViewer(HasTraits):

     # The scene model.
    scene = Instance(SceneModel)



    ######################
    view = View(
                Item(name='scene',  
                     editor=SceneEditor(),
                     show_label=False,
                     width= 0.8,
                     height =0.8,
                     resizable=True,
                    )
                )

    def __init__(self,**traits):
        super(ActorsViewer,self).__init__(**traits)
        self.scene = SceneModel()
        
    ####################################
    # Private traits.
    def add_actors(self, actors):
        
        if actors is not None:
             self.scene.add_actors(actors)
             
    def clear_actors(self):
        self.scene.actor_list = []
     
        
    def remove_actors(self, actors):
        if actors is not None:
             self.scene.remove_actors(actors)

if __name__ == '__main__':
    a = ActorsViewer()
    
    cone = actors.cone_actor()
    
    a.add_actors(cone)
    a.configure_traits()
