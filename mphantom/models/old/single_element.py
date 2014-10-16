# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 14:37:11 2011

@author: ZouLian
@Oncology Department
@Sichuan People's Hospital
@Chengdu,Sichuan,China
"""

from traits.api import Unicode, Dict, Instance, HasTraits, Bool 
from traitsui.api import View, Item,Readonly, UItem, VGroup, \
                         Tabbed, Spring, HGroup


from tvtk.api import tvtk



from tvtk.pyface import actors

from tvtk.pyface.actor_editor import ActorEditor



from base_element import BaseElement
from buildin_sgeometry import BuildinSGeometry

######################################################################

class SingleElement(BaseElement):
    '''A Single Model Element Class for Phantom Construction 
    '''
    
    name = Unicode('SElement') #default name is SingleModel
    
    
    #########################
    # ITVTKView Model traits.

    # This maintains a dictionary mapping objects (by identity) to lists (or
    # single items) of TVTK Actors or 3D Widgets that represent them in the
    # scene. Adding and removing objects from this dictionary adds and removes
    # them from the scene. This is the trait that will be edited by a
    # ActorEditor.
    

    
    #########################################
    # Actor Scene
    simplescene =  Dict()

    #Element Actor 
    current_element_actor = Instance(tvtk.Actor)
    
    
    geometry_ready = Bool(False)
  
                
    def __init__(self):
        super(SingleElement, self).__init__()
        if self.splash_switch == True:
           self._show_splash()
               
        

    def _current_element_actor_changed(self,actor):
        if actor is not None:
            actor.property = self.element_prop 
            self.simplescene={self.name : actor}
        
                
        
    def _name_changed(self, name):
        
        self.simplescene={name : self.current_element_actor}
        
        
       
    def _tissue_type_changed(self, value):
         
        super(SingleElement, self)._tissue_type_changed(value)
        if self.geometry is not None:
            self.geometry.geometry[0].property = self.element_prop
   
      
         
       
    
    ########################################################
    #Add Buildin Single  Geometry 
    def _add_buildin_sgemometry(self):
        sg = BuildinSGeometry()
           
        ui = sg.edit_traits(kind='livemodal')
         
        if ui.result:
            self.name = sg.geometry_name
            self.current_element_actor = sg.geometry[0]
            self.geometry = sg
            self.geometry_ready = True
   
        
    
          
       
    ########################################################
    #Set up the Real Geometry Chain
    
    def setup_geometry(self,geotype):
        # Remove the splash geometry
        self.splash_switch = False
        
        if geotype == 'buildin':    
            self._add_buildin_sgemometry()
            
   
          
      
    tab1 = VGroup(
                  VGroup(Item(name='name',
                            label=' ElementName'),    
                       Item(name='tissue_type',
                            label=' TissueType'),
                       Readonly(name='re_e_density',
                                label=' ReElectronDensity'),
                       Item('_'),
                       HGroup(Item(name='priority',label='Priority'),
                              Spring()
                              ),
                       Item('_'),
  
                      ),
                   UItem(name='simplescene',
                         editor=ActorEditor(scene_kwds={'background':(0.2,0.2,0.2)})
                         ),
                   label= 'ElementParameters'
                     )

    tab2= VGroup(Item(name='element_prop',
                      style='custom',
                      show_label =False),
                 label = 'VisualProp')
                   
    tab3 = VGroup(Item(name='current_element_actor',
                       style='custom',
                       show_label =False),
                      # resizable = True),
                   label = 'Geometry')                
    
    view = View(
                Tabbed(tab1,
                       tab2,          
                       tab3)    
                    
               )
                     

   
   
                   
    #Show the default splash Element
    def _show_splash(self):
               
        tempgeo = BuildinSGeometry()
        tempgeo.geometry = [actors.cone_actor()]
        tempgeo.geometry[0].property = self.element_prop 
        
        self.geometry = tempgeo
        
        self.current_element_actor=  tempgeo.geometry[0]
        
        
    def _splash_switch_changed(self,old,new):
        if new == False:
            self.geometry =None
            self.current_element_actor= None
            self.simplescene = {}
            
    

    
    ####################################

if __name__ == '__main__':
    
    a = SingleElement()
    
  #  a.splash_switch = False
    
    a.setup_geometry('buildin')
    
  #  a.geometry = actors.cone_actor()
#    a.element_prop = tvtk.Property(representation='w')
    
    print a.current_element_actor.bounds
    
    print a.get_bounds()
    
    
   
    a.configure_traits()
    
   # a.element_prop = tvtk.Property(representation='w')
