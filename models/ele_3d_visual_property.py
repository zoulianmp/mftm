"""A very silly example of using a scene editor.  More complex examples are
available in mayavi.  """

# Author: Prabhu Ramachandran <prabhu [at] aero.iitb.ac.in>
# Copyright (c) 2007, Enthought, Inc.
# License: BSD Style.

from traits.api import HasTraits, Enum, Instance, Any, on_trait_change
from traitsui.api import View, Item,Readonly,VGroup,Spring



from tvtk.pyface.scene_model import SceneModel
from tvtk.pyface.scene_editor import SceneEditor
from tvtk.pyface import actors
from tvtk.api import tvtk


from mphantom.api import EleBaseVisualProperty


######################################################################
class Ele3DVisualProperty(EleBaseVisualProperty):
        
    # The scene model.
    scene = Instance(SceneModel)


  

    ######################
    view = View(
                VGroup( Item(name='visibility',
                              label='Visibility'), 
                         Spring(),
                         Item(name='representation',
                              label='Representation'), 
                         Spring(),
                         Item(name='opacity',
                              label='Opacity'),
                         show_border = True
                              ),
                                                        
                Item(name='scene',  
                     editor=SceneEditor(),
                     show_label=False,
                     width= 0.8,
                     height =0.8,
                     resizable=True,
                    ),
                        
                 
                resizable = True
                )

   
    ##############visual_viewer######################
    def __init__(self,**traits):
        super(Ele3DVisualProperty,self).__init__(**traits)

        self.scene = SceneModel()
               
     
    def update_scene(self):
        self.scene.render()

 
        
    def add_actors(self, actors):
        self.clear_actors()
        self.scene.add_actors(actors)
     
    def clear_actors(self):
        self.scene.actor_list = []
        
    def remove_actors(self, actors):
        if actors is not None:
            if actors is not None:
                self.scene.remove_actors(actors)

    def get_data_for_json(self):
        '''Get a dict data for json output '''
        data= {}
        
        data["Color"] = self.color
        data["Opacity"] = self.opacity
        data["Representation"] = self.representation 
        data["Visibility"] = self.visibility
        
        return data

   
   
   
    @on_trait_change('inner_actor')
    def Onchange_inner_actor(self):
        self.clear_actors()
        self.add_actors(self.inner_actor)
        self.vis_changed = True
    
    
    
      
    @on_trait_change('color')
    def Onchange_actor_color(self):
        
        if self.inner_actor is not None:
            self.inner_actor.property.color = self.color
            self.vis_changed = True
    
    
                                  
    @on_trait_change( 'visibility' ) 
    def update_visibility(self):
        if self.inner_actor is not None:
            self.inner_actor.visibility = self.visibility
            
            self.scene.render()
            self.vis_changed = True
    
    
    @on_trait_change( 'representation' ) 
    def update_representation(self):        
        if self.inner_actor is not None :
            self.inner_actor.property.representation = self.representation              
            self.scene.render()          
            self.vis_changed = True
          
      
      
    @on_trait_change( 'opacity' ) 
    def update_opacity(self):
        if self.inner_actor is not None :
            self.inner_actor.property.opacity = self.opacity
            self.scene.render()       
            self.vis_changed = True
        

if __name__ == '__main__':

   from mphantom.api import ConeGeometry
   
   
   cone =  ConeGeometry()
   
   
   
   viewer =  Ele3DVisualProperty()
    
   viewer.add_actors(cone.current_actor)
    
  
   viewer.configure_traits()
