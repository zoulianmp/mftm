# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 10:27:44 2011

@author: ZouLian
@Oncology Department
@Sichuan People's Hospital
@Chengdu,Sichuan,China

"""
from tvtk.api import tvtk
from vtk.util import vtkConstants


###################################
# Useage Examples
"""
   from debug_helpers import polydata_render         
   polydata_render(polydata)
"""
##################################

def polydata_render(polydata):
    
    #Create the standard renderer, render window and interactor
    ren = tvtk.Renderer()
    renWin = tvtk.RenderWindow()
    renWin.add_renderer(ren)
    iren = tvtk.RenderWindowInteractor()
    iren.render_window = renWin
    
    mapper =tvtk.PolyDataMapper()
    mapper.input = polydata
    
    actor = tvtk.Actor()
    actor.mapper = mapper
    
    ren.add_actor(actor)

    ren.background = (0, 0, 0)
    renWin.size = (600, 600)
    renWin.render()
    
    def CheckAbort(obj, event):
        if obj.GetEventPending() != 0:
            obj.SetAbortRender(1)
     
    renWin.add_observer("AbortCheckEvent", CheckAbort)
    
    iren.initialize()
    renWin.render()
    iren.start()
###########################################################################
# vtkImageData Volume Render
###########################################################################


###################################
# Useage Examples
"""
   from debug_helpers import image_volume_render         
   image_volume_render(image)
"""
##################################

def image_volume_render(image):  
    
    # print "Int Image Volume render !"
    
    #Create the standard renderer, render window and interactor
    ren = tvtk.Renderer()
    renWin = tvtk.RenderWindow()
    renWin.add_renderer(ren)
    iren = tvtk.RenderWindowInteractor()
    iren.render_window = renWin
    
    # Create transfer mapping scalar value to opacity
    opacityTransferFunction = tvtk.PiecewiseFunction()
    opacityTransferFunction.add_point(20, 0.0)
    opacityTransferFunction.add_point(255, 0.2)
    
    # Create transfer mapping scalar value to color
    colorTransferFunction = tvtk.ColorTransferFunction()
    colorTransferFunction.add_rgb_point(0.0, 0.0, 0.0, 0.0)
    colorTransferFunction.add_rgb_point(64.0, 1.0, 0.0, 0.0)
    colorTransferFunction.add_rgb_point(128.0, 0.0, 0.0, 1.0)
    colorTransferFunction.add_rgb_point(192.0, 0.0, 1.0, 0.0)
    colorTransferFunction.add_rgb_point(255.0, 0.0, 0.2, 0.0)
    
    # The property describes how the data will look
    volumeProperty = tvtk.VolumeProperty()
    volumeProperty.set_color(colorTransferFunction)
    volumeProperty.set_scalar_opacity(opacityTransferFunction)
    volumeProperty.shade = True
    volumeProperty.interpolation_type = vtkConstants.VTK_LINEAR_INTERPOLATION
    
    # The mapper / ray cast function know how to render the data
    compositeFunction = tvtk.VolumeRayCastCompositeFunction()
    volumeMapper = tvtk.VolumeRayCastMapper()
    volumeMapper.volume_ray_cast_function = compositeFunction
    volumeMapper.input = image
    
    # The volume holds the mapper and the property and
    # can be used to position/orient the volume
    volume = tvtk.Volume()
    volume.mapper = volumeMapper
    volume.property = volumeProperty
    
    ren.add_volume(volume)
    ren.background = (0, 0, 0)
    renWin.size = (600, 600)
    renWin.render()
    
    def CheckAbort(obj, event):
        if obj.GetEventPending() != 0:
            obj.SetAbortRender(1)
     
    renWin.add_observer("AbortCheckEvent", CheckAbort)
    
    iren.initialize()
    renWin.render()
    iren.start()


###################################
# Useage Examples
"""
   from debug_helpers import image_volume_slice_view         
   image_volume_slice_view(image)
"""
##################################
    
def image_volume_slice_view(inimage):
    bounds = inimage.bounds
    center =(((bounds[1] + bounds[0])/2.0),
             ((bounds[3] + bounds[2])/2.0),
             ((bounds[5] + bounds[4])/2.0))
        
    # Matrices for axial, coronal, sagittal, oblique view orientations
    axial = tvtk.Matrix4x4()
    axial.deep_copy((1, 0, 0, center[0],
                    0, 1, 0, center[1],
                    0, 0, 1, center[2],
                    0, 0, 0, 1))
    
    coronal = tvtk.Matrix4x4()
    coronal.deep_copy((1, 0, 0, center[0],
                      0, 0, 1, center[1],
                      0,-1, 0, center[2],
                      0, 0, 0, 1))
    
    sagittal = tvtk.Matrix4x4()
    sagittal.deep_copy((0, 0,-1, center[0],
                       1, 0, 0, center[1],
                       0,-1, 0, center[2],
                       0, 0, 0, 1))
    
    oblique = tvtk.Matrix4x4()
    oblique.deep_copy((1, 0, 0, center[0],
                      0, 0.866025, -0.5, center[1],
                      0, 0.5, 0.866025, center[2],
                      0, 0, 0, 1))

    # Extract a slice in the desired orientation
    reslice = tvtk.ImageReslice()
    
    reslice.input = inimage
    
    reslice.output_dimensionality = 2
    reslice.reslice_axes = axial
    
    #reslice.SetResliceAxes(coronal)
    #reslice.SetResliceAxes(sagittal)
    #reslice.SetResliceAxes(oblique)
    reslice.interpolation_mode = vtkConstants.VTK_LINEAR_INTERPOLATION


    
    # Create a greyscale lookup table
    table = tvtk.LookupTable()
    table.range = (0, 2000) # image intensity range
    table.value_range = (0.0, 1.0) # from black to white
    table.saturation_range = (0.0, 0.0) # no color saturation
    table.ramp = 'linear'
    table.build()

    # Map the image through the lookup table
    color = tvtk.ImageMapToColors()
    color.lookup_table = table
    color.input = reslice.output

    # Display the image
    actor = tvtk.ImageActor()
    actor.input = color.output
    


 #Create the standard renderer, render window and interactor
    ren = tvtk.Renderer()
    ren.add_actor(actor)
    
    window = tvtk.RenderWindow()
    window.add_renderer(ren)
    
    iren = tvtk.RenderWindowInteractor()
    iren.render_window = window


    # Set up the interaction
    interactorStyle = tvtk.InteractorStyleImage()
    
    iren.interactor_style = interactorStyle
    
    
    window.interactor = iren
    window.render()
    
    # Create callbacks for slicing the image
    actions = {}
    actions["Slicing"] = 0
    
    def ButtonCallback(obj, event):
        if event == "LeftButtonPressEvent":
            actions["Slicing"] = 1
        else:
            actions["Slicing"] = 0
    
    def MouseMoveCallback(obj, event):
        (lastX, lastY) = iren.last_event_position
        (mouseX, mouseY) = iren.event_position
        if actions["Slicing"] == 1:
            deltaY = int((mouseY - lastY)/2.0)
            reslice.get_output().update_information()
            spacing = reslice.output.spacing
            sliceSpacing = spacing[2]
            matrix = reslice.reslice_axes
            # move the center point that we are slicing through
            center = matrix.multiply_point((0, 0, sliceSpacing*deltaY, 1))
            print center
            matrix.set_element(0, 3, center[0])
            matrix.set_element(1, 3, center[1])
            matrix.set_element(2, 3, center[2])
            window.render()
        else:
            interactorStyle.on_mouse_move()
            
    
    interactorStyle.add_observer("MouseMoveEvent", MouseMoveCallback)
    interactorStyle.add_observer("LeftButtonPressEvent", ButtonCallback)
    interactorStyle.add_observer("LeftButtonReleaseEvent", ButtonCallback)
    
    # Start interaction
    
    iren.start()





###################################
# Useage Examples
"""
   from debug_helpers import gen_image_data_by_numpy         
   gen_image_data_by_numpy()
"""
##################################

#Generate the White Image data for mask the phantom model 
def gen_image_data_by_numpy( bgvalue = -600):
 
       bounds = [-50,50,-50,50,-30,30]
       
       width = bounds[1] - bounds[0]
       lenth = bounds[3] - bounds[2]
       heigh = bounds[5] - bounds[4]
       
       spacing_x = 1
       spacing_y = 1
       spacing_z = 3
       
       size_x = width/spacing_x
       size_y = lenth/spacing_y 
       size_z  = heigh/spacing_z
                    
       spacing = ( spacing_x, spacing_y,spacing_z)
       
       image = tvtk.ImageData()
       
       dim= (size_x ,size_y,size_z )
       
       origin = (bounds[0],bounds[2],bounds[4])     
       exten = (0,dim[0]-1,0,dim[1]-1,0,dim[2]-1)
     
         
       #Initialize the volume value
       import numpy as np
       
       scalars = np.ones(dim,dtype = np.int16) * bgvalue
       
       scalars[:,10:90,10:90] = 500
       #scalars[:,16:24,16:24] = 800
      
       
       #set image property
       image.origin = origin
       image.spacing = spacing
       image.extent = exten
       
       image.scalar_type = vtkConstants.VTK_SHORT
       image.point_data.scalars = scalars.ravel()
    
       return image
   
   

#Mask the polydata to volume image with vaiue HU     
def polydata_to_image(image):
    
   
#        #*******************************************
    sphere = tvtk.SphereSource()
    sphere.phi_resolution = 180
    sphere.theta_resolution = 180
    sphere.center = (30,0,0)
    sphere.radius = 40
    sphere.update()        
   

    bghu =1789      
    
    triangle = tvtk.TriangleFilter()
  
    
    triangle.input = sphere.output
  
    stripper =tvtk.Stripper()
    stripper.input = triangle.output
    
    dataToStencil = tvtk.PolyDataToImageStencil()
    dataToStencil.input = stripper.output
               
    print " image.spacing :" , image.spacing        
    dataToStencil.output_spacing = image.spacing
    dataToStencil.output_origin = image.origin
    dataToStencil.tolerance = 0.01

    stencil = tvtk.ImageStencil()
    stencil.input = image
    stencil.stencil = dataToStencil.output
   
    stencil.reverse_stencil = True
    
    stencil.background_value = bghu
    
    stencil.update()   
    return stencil.output
        
#################################################################################

if __name__ == '__main__':
    
    image = gen_image_data_by_numpy()
    
    #print "Volume Render the Image :"
    #image_volume_render(image)

    #print "Slice Show the Image: "
    #image_volume_slice_view(image)
    
    outimage = polydata_to_image(image)
    
    print "After Mask Slice Show"
    image_volume_slice_view(outimage)
    
    from pyface.api import MessageDialog
    dialog = MessageDialog(message="message", title="title", severity='error')
    dialog.open()
     
   