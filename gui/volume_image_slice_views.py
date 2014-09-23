# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 15:08:10 2011

@author: ZouLian
@Oncology Department
@Sichuan People's Hospital
@Chengdu,Sichuan,China
"""

from traits.api import  HasTraits, List, Instance, on_trait_change,Int, Dict, \
                        Range

from traitsui.api import View, HSplit, VSplit,HGroup,VGroup, Group, Item, RangeEditor



from tvtk.pyface.api import Scene


from tvtk.pyface.scene_model import SceneModel
from tvtk.pyface.scene_editor import SceneEditor


from tvtk.api import tvtk


from vtk.util import vtkConstants


class VolumeImageSliceViews(HasTraits):
   
    volume = Instance(tvtk.ImageData)
    
    # The direction in which the panel is split.
    view_annote  = List(['T','S','C'])

    # The `Scene` instance into which VTK renders.
    view_translate = Instance(SceneModel)
    view_coronal = Instance(SceneModel)
    view_sagital = Instance(SceneModel)
   
    viewers = {0:view_translate,
               1:view_coronal,
               2:view_sagital
              }
    
    # Matrices for axial, coronal, sagittal, oblique view orientations
    
    axial =Instance(tvtk.Matrix4x4)
        
    coronal = Instance(tvtk.Matrix4x4)
    
    sagittal = Instance(tvtk.Matrix4x4)
     
     
    default_position = List([0,0,0]) 
    
    curent_position = List([0,0,0])    
    
    #******************************************************************
    # Properties for Callback setup
    current_interactor = Instance(tvtk.GenericRenderWindowInteractor)
    
    actions = Dict({})
 
    
    #The current_matrix setup for get defined image plane
    current_matrix =Instance(tvtk.Matrix4x4)  
        
    #viewid: (0,1,2),0: Translate,1:coronal,2:sagital
    current_view_id = Int(0)
    
    
    #Image viewer window Level and Width
    level_min = -1000
    level_max = 1000

    image_gray_level = Range(low=level_min,high=level_max,value=(level_min+level_max)/2)
    
    width_min = 0
    width_max = 2000
    image_gray_Width = Range(low=width_min,high=width_max,value= (width_min + width_max)/2)
    
    intensity_low = Int(-1000)
          
    intensity_high = Int(1000)
    
      

    
    
    #**********************************************
    #Init Property Value   
                  
    def __init__(self,**traits):
        super(VolumeImageSliceViews, self).__init__(**traits)
        self.actions["Slicing"] = 0           
                    
    def _axial_default(self):
        axial = tvtk.Matrix4x4()      
        axial.deep_copy((1, 0, 0, 0,
                         0, 1, 0, 0,
                         0, 0, 1, 0,
                         0, 0, 0, 1))
        return axial
                            
                            
    def _coronal_default(self):
        coronal = tvtk.Matrix4x4()      
        coronal.deep_copy((1, 0, 0, 0,
                           0, 1, 0, 0,
                           0, 0, 1, 0,
                           0, 0, 0, 1))
        return coronal
    
    def _sagittal_default(self):
        sagittal = tvtk.Matrix4x4()      
        sagittal.deep_copy((1, 0, 0, 0,
                            0, 1, 0, 0,
                            0, 0, 1, 0,
                            0, 0, 0, 1))
        return sagittal
                       
                           
    
    def _view_translate_default(self):
        return SceneModel()

    def _view_sagital_default(self):
        return SceneModel()

    def _view_coronal_default(self):
        return SceneModel()




    #Extract the Desired Slice image from a volume
    def _create_image_slice(self,inimage,matrix,bgvalue=-1000):
        
        #Record the current position
        
        self.curent_position[0] =   matrix.get_element(0, 3)
        self.curent_position[1] =   matrix.get_element(1, 3)
        self.curent_position[2] =   matrix.get_element(2, 3)        
         
        # Extract a slice in the desired orientation
        reslice = tvtk.ImageReslice()
        reslice.auto_crop_output = True
        
        reslice.background_level = bgvalue
        
        reslice.input = inimage
        
        reslice.output_dimensionality = 2
        reslice.reslice_axes = matrix
        
        
        reslice.interpolation_mode = vtkConstants.VTK_NEAREST_INTERPOLATION
    
        return reslice.output
    
        
        
    def _gen_image2d_actor(self,image2d,intensity_low,intensity_high):
        
        
        # Create a greyscale lookup table
        table = tvtk.LookupTable()
        table.range = (intensity_low,intensity_high) # image intensity range
        table.value_range = (0.0, 1.0) # from black to white
        table.saturation_range = (0.0, 0.0) # no color saturation
        table.ramp = 'linear'
        table.build()
    
        # Map the image through the lookup table
        color = tvtk.ImageMapToColors()
        color.lookup_table = table
        color.input = image2d
    
        # Display the image
        actor = tvtk.ImageActor()
        actor.input = color.output
        
        return actor
        
        
        
        
        
    
    def _gen_view_label(self,label):
        textActor = tvtk.TextActor()
        
        textActor.position = (10, 10)
        
        textActor.input = label
             
        tprop = textActor.text_property
        tprop.font_size = 22
        tprop.font_family = 'arial'
        tprop.justification = 'left'
        
        tprop.bold = True
        tprop.italic= True
  
        tprop.color =(0, 1, 1)
        
        return textActor


    def _update_image_views(self):
        
        #Update Translate View
        t_pre_actor_list = self.view_translate.actor_list
        self.view_translate.remove_actors(t_pre_actor_list)
                
        t_image2d = self._create_image_slice(self.volume, self.axial) 
                
        t_actor = self._gen_image2d_actor(t_image2d,self.intensity_low,self.intensity_high)
               
        self.view_translate.add_actors(t_actor)
        self.view_translate.add_actors(self.creat_T_view_label())
        
        
        #Update Sagital View
      
        s_pre_actor_list = self.view_sagital.actor_list
        self.view_sagital.remove_actors(s_pre_actor_list)
       
        s_image2d = self._create_image_slice(self.volume,self.sagittal) 
        
        s_actor = self._gen_image2d_actor(s_image2d,self.intensity_low,self.intensity_high)
     
        self.view_sagital.add_actors(s_actor)
        self.view_sagital.add_actors(self.creat_S_view_label())
        
 
 
        #Update Coronal View
 
        c_pre_actor_list = self.view_coronal.actor_list
        self.view_coronal.remove_actors(c_pre_actor_list)
               
        c_image2d = self._create_image_slice(self.volume,self.coronal)  
        c_actor = self._gen_image2d_actor(c_image2d,self.intensity_low,self.intensity_high)
               
        self.view_coronal.add_actors(c_actor)
        self.view_coronal.add_actors(self.creat_C_view_label())
                  
        
    #---------------------------------------------------------------------------
    # Traits  Notified and callback
    #---------------------------------------------------------------------------
    @on_trait_change('image_gray_level')
    def update_image_gray_level(self):
        self.intensity_low = self.image_gray_level - self.image_gray_Width/2
        self.intensity_high = self.image_gray_level + self.image_gray_Width/2
        self._update_image_views()
          
    @on_trait_change('image_gray_Width')
    def update_image_gray_width(self):
        self.intensity_low = self.image_gray_level - self.image_gray_Width/2
        self.intensity_high = self.image_gray_level + self.image_gray_Width/2
        self._update_image_views()
   
  
        
   
        
    
    @on_trait_change('volume')
    def setup_init_views(self):
        bounds = self.volume.bounds     
        center =(((bounds[1] + bounds[0])/2.0),
                 ((bounds[3] + bounds[2])/2.0),
                 ((bounds[5] + bounds[4])/2.0))
        
        self.default_position = [center[0],center[1],center[2]]
                 
        self.axial.deep_copy((-1, 0, 0, center[0],
                              0, 1, 0, center[1],
                              0, 0, -1, center[2],
                              0, 0, 0, 1))
                
   
        self.coronal.deep_copy((-1, 0, 0, center[0],
                                0, 0, 1, center[1],
                                0, 1, 0, center[2],
                                0, 0, 0, 1))
    
   
        self.sagittal.deep_copy((0, 0,-1, center[0],
                                 0, 1, 0, center[1],
                                 1, 0, 0, center[2],
                                 0, 0, 0, 1))
           
        
        
        self.view_translate.scene.background = (0, 0, 0)                      
        t_image2d = self._create_image_slice(self.volume,self.axial)  
     
        t_actor = self._gen_image2d_actor(t_image2d,self.intensity_low,self.intensity_high)
        
        
        self.view_translate.add_actors(t_actor)
        self.view_translate.add_actors(self.creat_T_view_label())
        
        
        self.view_coronal.scene.background = (0, 0, 0)
        c_image2d= self._create_image_slice(self.volume,self.coronal)   
        
        
        
        c_actor = self._gen_image2d_actor(c_image2d,self.intensity_low,self.intensity_high)
                
        
        self.view_coronal.add_actors(c_actor)
        self.view_coronal.add_actors(self.creat_C_view_label())
        
     
        self.view_sagital.scene.background = (0, 0, 0)       
        s_image2d = self._create_image_slice(self.volume,self.sagittal)
        
        
        s_actor = self._gen_image2d_actor(s_image2d,self.intensity_low,self.intensity_high)
                
        self.view_sagital.add_actors(s_actor)
        self.view_sagital.add_actors(self.creat_S_view_label())
    
 #-------------------------------------------------------------------------
 # Activated Viewers
 #-------------------------------------------------------------------------   
    @on_trait_change('view_translate.activated')
    def change_interactor_of_translate(self):
        
           
        t_interactor = self.view_translate.scene.interactor
               
        t_interactor.interactor_style = tvtk.InteractorStyleImage()
        iterstyle = t_interactor.interactor_style         
        
        iterstyle.add_observer("LeftButtonPressEvent", self.press_in_TView)
        iterstyle.add_observer( "LeftButtonReleaseEvent", self.press_in_TView)
   
        
    
    @on_trait_change('view_coronal.activated')
    def change_interactor_of_coronal(self):
    
        c_interactor = self.view_coronal.scene.interactor
     
        c_interactor.interactor_style = tvtk.InteractorStyleImage()
        iterstyle = c_interactor.interactor_style
       
        iterstyle.add_observer("LeftButtonPressEvent", self.press_in_CView)
        iterstyle.add_observer( "LeftButtonReleaseEvent",self.press_in_CView)
     
    
   
    @on_trait_change('view_sagital.activated')
    def change_interactor_of_sagital(self):
     
        
        s_interactor = self.view_sagital.scene.interactor
        
        s_interactor.interactor_style = tvtk.InteractorStyleImage()     
        iterstyle = s_interactor.interactor_style
       
        iterstyle.add_observer("LeftButtonPressEvent", self.press_in_SView)
        iterstyle.add_observer( "LeftButtonReleaseEvent",self.press_in_SView)
       
    
    #---------------------------------------------------------------------------
    # CallBack   for interactor
    #---------------------------------------------------------------------------
    @on_trait_change('current_interactor')
    def setup_callback_for_interactor(self):
        #viewid: (0,1,2),0: Translate,1:coronal,2:sagital
       
         
        iterstyle = self.current_interactor.interactor_style
      #  iterstyle.add_observer("MouseMoveEvent", self.MouseMoveCallback)
        iterstyle.add_observer("MiddleButtonPressEvent",self.MiddleButtonCallback)

        iterstyle.add_observer("MouseWheelForwardEvent",self.MouseWheelCallback)
        iterstyle.add_observer("MouseWheelBackwardEvent",self.MouseWheelCallback)


    
    def press_in_TView(self,obj, event):
        print event
        if event == "LeftButtonPressEvent":     
            self.current_view_id = 0
            self.actions["Slicing"] = 1
            self.current_interactor = self.view_translate.scene.interactor
 
        else :
            self.actions["Slicing"] = 0
   
            
            
    def press_in_CView(self,obj, event):
        if event == "LeftButtonPressEvent":     
          
            self.current_view_id = 1
            self.actions["Slicing"] = 1   
            self.current_interactor = self.view_coronal.scene.interactor   
        
        else :
            self.actions["Slicing"] = 0
   
        
    def press_in_SView(self,obj, event):
        if event == "LeftButtonPressEvent":     
           
            self.current_view_id = 2
            self.actions["Slicing"] = 1   
            self.current_interactor = self.view_sagital.scene.interactor
   
        else :
            self.actions["Slicing"] = 0
            
            
################################################
#Creat the views labels
   
    def creat_T_view_label(self):
        
        T_label = 'T:   '+str(self.curent_position[2])+'   (mm)'
        textactor1 = self._gen_view_label(T_label)
        return textactor1
        
      
    def creat_C_view_label(self):
        
        C_label = 'C:   '+str(self.curent_position[1])+'   (mm)'       
        textactor2 = self._gen_view_label(C_label)
        return textactor2
    
    def creat_S_view_label(self):
          
        S_label = 'S:   '+str(self.curent_position[0])+'   (mm)'
        textactor3 = self._gen_view_label(S_label)
        return textactor3


    def MiddleButtonCallback(self,obj, event):
   
        if event == "MiddleButtonPressEvent":     
           
            if self.current_view_id == 0:
                t_matrix = self.axial
                t_matrix.set_element(0, 3, self.default_position[0])
                t_matrix.set_element(1, 3, self.default_position[1])
                t_matrix.set_element(2, 3, self.default_position[2])
               
                pre_actor_list = self.view_translate.actor_list
                self.view_translate.remove_actors(pre_actor_list)
                
                current_image2d = self._create_image_slice(self.volume,t_matrix) 
                
                current_actor = self._gen_image2d_actor(current_image2d,self.intensity_low,self.intensity_high)
               
                
                self.view_translate.add_actors(current_actor)
                self.view_translate.add_actors(self.creat_T_view_label())
        
                
            elif self.current_view_id == 1:
                t_matrix = self.coronal
                t_matrix.set_element(0, 3, self.default_position[0])
                t_matrix.set_element(1, 3, self.default_position[1])
                t_matrix.set_element(2, 3, self.default_position[2])
                
                pre_actor_list = self.view_coronal.actor_list
                self.view_coronal.remove_actors(pre_actor_list)
               
                current_image2d = self._create_image_slice(self.volume,t_matrix)  
                
                current_actor = self._gen_image2d_actor(current_image2d,self.intensity_low,self.intensity_high)
               
                self.view_coronal.add_actors(current_actor)
                self.view_coronal.add_actors(self.creat_C_view_label())
                  
            elif self.current_view_id == 2:
                t_matrix = self.sagittal
                t_matrix.set_element(0, 3, self.default_position[0])
                t_matrix.set_element(1, 3, self.default_position[1])
                t_matrix.set_element(2, 3, self.default_position[2])
               
                pre_actor_list = self.view_sagital.actor_list
                self.view_sagital.remove_actors(pre_actor_list)
               
                current_image2d = self._create_image_slice(self.volume,t_matrix) 
                
                current_actor = self._gen_image2d_actor(current_image2d,self.intensity_low,self.intensity_high)
             
             
                self.view_sagital.add_actors(current_actor)
                self.view_sagital.add_actors(self.creat_S_view_label())
                
            else:
                 pass
        else:     
            pass
         
               
                

    
    #interactorStyle.add_observer("MouseMoveEvent", MouseMoveCallback)
  
    
    def MouseMoveCallback(self,obj, event):
        print event
        print "MouseMovecallback"
  
        (lastX, lastY) =  self.current_interactor.last_event_position
        (mouseX, mouseY) =  self.current_interactor.event_position
        
       
        if self.actions["Slicing"] == 1:
            deltaY = int((mouseY - lastY)/2.0)
            
            spacing = self.volume.spacing
            
            sliceSpacing = spacing[0]
            
            
            if self.current_view_id == 0 :
                self.current_matrix = self.axial  
                sliceSpacing = spacing[0]
                viewer = self.view_translate
                
            elif self.current_view_id == 1 :
                self.current_matrix = self.coronal  
                sliceSpacing = spacing[1]
                viewer = self.view_coronal
                
            elif self.current_view_id == 2 :
                self.current_matrix = self.sagittal  
                sliceSpacing = spacing[0]
                viewer = self.view_sagital
                
            # move the center point that we are slicing through
            deta_slice =  sliceSpacing*deltaY   
            
            print "deta_slice",deta_slice
            center = self.current_matrix.multiply_point((0, 0, deta_slice, 1))
            
            self.current_matrix.set_element(0, 3, center[0])
            self.current_matrix.set_element(1, 3, center[1])
            self.current_matrix.set_element(2, 3, center[2])
            
          
              
            current_image2d = self._create_image_slice(self.volume,self.current_matrix)  
            current_actor = self._gen_image2d_actor(current_image2d,self.intensity_low,self.intensity_high)
             
            
            viewer.add_actors(current_actor)
            viewer.render()
            
        else:
            self.current_interactor.interactor_style.on_mouse_move()
    
    
    def  MouseWheelCallback(self,obj, event):
        print event
        delta = 0
        if event == "MouseWheelForwardEvent":
            delta = 1
        elif  event == "MouseWheelBackwardEvent":
            delta = -1
       
            
        spacing = self.volume.spacing
       
        print delta
        
        if self.current_view_id == 0 :
            self.current_matrix = self.axial    
            sliceSpacing = spacing[2]
            viewer = self.view_translate
            
        elif self.current_view_id == 1 :
            self.current_matrix = self.coronal  
            sliceSpacing = spacing[1]
            viewer = self.view_coronal
            
        elif self.current_view_id == 2 :
            self.current_matrix = self.sagittal  
            sliceSpacing = spacing[0]
            viewer = self.view_sagital
            
        print self.curent_position
        self.current_matrix.set_element(0, 3, self.curent_position[0])
        self.current_matrix.set_element(1, 3, self.curent_position[1])
        self.current_matrix.set_element(2, 3, self.curent_position[2])
        
            
        # move the center point that we are slicing through
        deta_slice =  sliceSpacing*delta 
     
      
        new_position = self.current_matrix.multiply_point((0, 0, deta_slice, 1))
        
        self.current_matrix.set_element(0, 3, new_position[0])
        self.current_matrix.set_element(1, 3, new_position[1])
        self.current_matrix.set_element(2, 3, new_position[2])
        
    
        pre_actor_list = viewer.actor_list
        viewer.remove_actors(pre_actor_list)
                
        current_image2d = self._create_image_slice(self.volume,self.current_matrix)      
        current_actor = self._gen_image2d_actor(current_image2d,self.intensity_low,self.intensity_high)
             
             
        viewer.add_actors(current_actor)
        
         
        if self.current_view_id == 0 :
            viewer.add_actors(self.creat_T_view_label())
          
        elif self.current_view_id == 1 :
            viewer.add_actors(self.creat_C_view_label())
        
        elif self.current_view_id == 2 :
            viewer.add_actors(self.creat_S_view_label())
             
        viewer.render()
        
    def reset_slice_views(self):
        print "reset slice views"
        
        t_alist =   self.view_translate.actor_list        
        self.view_translate.remove_actors(t_alist)
        
        
        c_alist =   self.view_coronal.actor_list    
        self.view_coronal.remove_actors(c_alist)
        
      
        s_alist =   self.view_sagital.actor_list
        self.view_sagital.remove_actors(s_alist)
        
        
        
    
    #---------------------------------------------------------------------------
    # The layout of the dialog created
    #---------------------------------------------------------------------------
    view = View(               
                 VGroup(
                      HGroup(Item('image_gray_level',
                                   editor= RangeEditor(mode = 'slider',
                                                       low_name = 'level_min',
                                                       high_name = 'level_max'
                                                       ),
                                   label  = 'Image Level',
                                   
                                 height = 0.1
                                 ),
                             Item('image_gray_Width',
                                  editor= RangeEditor(mode='slider',
                                                      low_name = 'width_min',
                                                      high_name = 'width_max'
                                                      ),
                                  label  = 'Image Width',
                                  height = 0.1
                                 
                                 )
                                                      
                                                  
                        ),  
                      Group(
                           Item('view_translate',
                                editor=SceneEditor(scene_class=Scene),
                                #editor=SceneEditor(),
                                height=0.6,
                                resizable = True),
                           
                           show_labels=False,
                           
                           ),
                      HGroup(
                           Item('view_sagital',
                                editor=SceneEditor(scene_class=Scene),
                                height=250, width=300,
                                resizable = True),
                           Item('view_coronal',
                                editor=SceneEditor(scene_class=Scene),
                                height=250, width=300,
                                resizable = True),
                           show_labels=False,
                      ),
                ),
                scrollable =False,
                resizable=True,
                #title='Volume Slicer',
                )
                

if __name__ == '__main__':
    
    
    
    from mphantom.api import gen_image_data_by_numpy         
    image = gen_image_data_by_numpy(220)
   
    viewers = VolumeImageSliceViews()
    viewers.volume = image
    
    viewers.configure_traits()
  
    
    
