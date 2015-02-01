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
def gen_g4geometry_by_numpy( bgvalue = -600):
       
       nvoxles_x = 5
       nvoxles_y = 4
       nvoxles_z = 3     
       
       spacing_x = 1.0
       spacing_y = 1.0
       spacing_z = 3.0
       
       bounds = [-0.5* (nvoxles_x-1)*spacing_x, 0.5* (nvoxles_x-1)*spacing_x,
                   
                   -0.5* (nvoxles_y-1)*spacing_y, 0.5* (nvoxles_y-1)*spacing_y,
                   
                   -0.5* (nvoxles_z-1)*spacing_z, 0.5* (nvoxles_z-1)*spacing_z,
       
                   ]
       
       origin = (bounds[0],bounds[2],bounds[4])  
       
       
       print "manual caculated bounds_x : ", bounds
       
     
     
       size_x = nvoxles_x
       size_y = nvoxles_y
       size_z  = nvoxles_z
                    
       spacing = ( spacing_x, spacing_y,spacing_z)
       
       image = tvtk.ImageData()
       
       dim= (size_z ,size_y, size_x) #in numpy (z,y,x)
       
       origin = (bounds[0],bounds[2],bounds[4])  
       
   #    origin = (bounds[0]+(spacing_x/2.0),bounds[2]+(spacing_y/2.0), \
    #             bounds[4]+(spacing_z/2.0))  
       
       
       exten = (0,dim[2]-1,0,dim[1]-1,0,dim[0]-1)   # x,y,z in vtk images
   #    exten = (1,dim[0] ,1,dim[1],1,dim[2] )
     
         
       #Initialize the volume value
       import numpy as np
       
       scalars = np.ones(dim,dtype = np.int16) * bgvalue
       
       scalars[0,0,1:4] = 6
       scalars[0,2,1:4] = 3
       scalars[1,1,1:4] = 8
       scalars[2,1,1] = 7
       scalars[2,2,2] = 7
       scalars[2,3,3] = 7
       
       print scalars
      
       
       #set image property
       image.origin = origin
       image.spacing = spacing
       image.extent = exten
       
       image.scalar_type = vtkConstants.VTK_SHORT
       image.point_data.scalars = scalars.ravel()
    
       return image
   
   
#Generate the White Image data for mask the phantom model 
def gen_image_data_by_numpy( bgvalue = -600):
 
       
       nvoxles_x = 5
       nvoxles_y = 5
       nvoxles_z = 5      
       
       spacing_x = 1.0
       spacing_y = 1.0
       spacing_z = 3.0
       
       bounds = [-0.5* (nvoxles_x-1)*spacing_x, 0.5* (nvoxles_x-1)*spacing_x,
                   
                   -0.5* (nvoxles_y-1)*spacing_y, 0.5* (nvoxles_y-1)*spacing_y,
                   
                   -0.5* (nvoxles_z-1)*spacing_z, 0.5* (nvoxles_z-1)*spacing_z,
       
                   ]
       
       print "manual caculated bounds_x : ", bounds
       
     
     
       size_x = nvoxles_x
       size_y = nvoxles_y
       size_z  = nvoxles_z
                    
       spacing = ( spacing_x, spacing_y,spacing_z)
       
       image = tvtk.ImageData()
       
       dim= (size_x ,size_y,size_z )
       
       origin = (bounds[0],bounds[2],bounds[4])  
       
   #    origin = (bounds[0]+(spacing_x/2.0),bounds[2]+(spacing_y/2.0), \
    #             bounds[4]+(spacing_z/2.0))  
       
       
       exten = (0,dim[0]-1,0,dim[1]-1,0,dim[2]-1)
   #    exten = (1,dim[0] ,1,dim[1],1,dim[2] )
     
         
       #Initialize the volume value
       import numpy as np
       
       scalars = np.ones(dim,dtype = np.int16) * bgvalue
       
       scalars[:,10:90,10:90] = 500
       scalars[:,16:24,16:24] = 800
      
       
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


###################################
# Useage Examples
"""
   from debug_helpers import resample_image         
   resample_image(image)
"""
##################################

def print_image_info(image):
    
    image.update()
    
    image.compute_bounds()
     
    
    print "###########################################"
    print "#########Begin of Print Image Infor #######"

       #set image property

    print "image.origin = ", image.origin
    print "image.spacing = ", image.spacing 
    print "image.extent = ", image.extent   #dimenstion 
    print "image.whole_extent = ", image.whole_extent       
    print "image.data_dimension = ", image.data_dimension
    print "image.center = ",image.center
    print "image.bounds = ", image.bounds 

   
    print "#########End of Print Image Infor #######"
    print "###########################################"







###################################
# Useage Examples
"""
   from debug_helpers import resample_image         
   resample_image(image)
"""
##################################




def resample_image(image,dealflag = 0 ):
    
    resampler = tvtk.ImageResample()
    
    resampler.input = image
    
     
    x_factor = 2
    y_factor = 2
    z_factor = 2
    
        
    resampler.interpolation_mode = 'cubic' 
    resampler.set_axis_magnification_factor(0, x_factor)
    
    resampler.set_axis_magnification_factor(1, y_factor)
    resampler.set_axis_magnification_factor(2, z_factor)
    
    resampler.update()
    
#    resampler.output.origin = new_origin
    
    return resampler.output
    
    
    
    
def image_cast_for_visualization(image):

    castor = tvtk.ImageCast()
    castor.input = image
    
    castor.set_output_scalar_type_to_unsigned_char()
    castor.update()
    
    return castor.output
    
    
    

def numpy_array_test():
     import numpy as np
     
     size_x = 5
     size_y = 4
     size_z = 3
     
     dim= (size_z ,size_y, size_x)  #index style
       
     scalars = np.ones(dim,dtype = np.int16) 
     
     print scalars
     
     scalars[1,1,:] = 45
     
   

     print scalars
     
     scalars1 = np.ones(dim,dtype = np.int16)*90 
     
     import csv
     
     
     
     import csv
    
     
     mates = ["sggsdg","sagjfwlkejoi", "asdgagag"]
     
     mas_dic = ["asg",5545,"weew",809808]
     
     
     
     import csv


    
     
     fname = "e:/test_numpy.txt"
     with open(fname, 'w') as csvfile:
         
        writer = csv.writer(csvfile,delimiter = ' ', lineterminator='\n')
        
        writer.writerow(mates)
        writer.writerow(mas_dic)
        
        
              
        scalars.tofile(csvfile, sep=" ", format="%f") 
        scalars1.tofile(csvfile, sep=" ", format="%f") 
     csvfile.close()


def save_list_to_file_test():
      
     
     import csv

     res = ["sggsdg","sagjfwlkejoi", "asdgagag"]
     csvfile = "e:/test_listout.txt"

     #Assuming res is a flat list
     with open(csvfile, "w") as output:
        writer = csv.writer(output,delimiter = ' ', lineterminator='\n')
        
        writer.writerow(res)
        writer.writerows(res)
        
      #  mas_dic = {"asg":5545,"weew":809808}
        
       # writer.writerow(mas_dic)
     
        for val in res:
            writer.writerow([val])    

    #Assuming res is a list of lists
    # with open(csvfile, "w") as output:
    #    writer = csv.writer(output, lineterminator='\n')
    #    writer.writerows(res)
        
        
       
    
    
def extract_image_voi(image):
    
    extractor =tvtk.ExtractVOI()
    
    extractor.input = image
    
    extractor.voi = (30, 160, 30, 160, 3, 6)
     
     
    extractor.update ()
    return extractor.output
    
    
#     
#     extract = vtk.vtkExtractVOI()
#     151 extract.SetVOI(31, 31, 0, 63, 0, 92)
#     152 extract.SetSampleRate(1, 1, 1)
#     153 extract.SetInputConnection(shifter.GetOutputPort())
#     154 extract.ReleaseDataFlagOff()
#     155 #
#     156 








if __name__ == '__main__':
    
    
   #  save_list_to_file_test()
    # numpy_array_test()
    
#    
     image = gen_g4geometry_by_numpy()
     
     
     import numpy as np

     vtk_array = image.point_data.scalars
     
   
     #np(z,y,x)
     shape = (3,4,5)
            
     array_pointer =  vtk_array.to_array()

      
            
     result = np.frombuffer(array_pointer, dtype=np.int16)
     
     print "Pre reshaped:"
     print result
     
     result.shape = shape 
     print "After reshaped:"
     print result
     
     with open("e:/test.nump.txt", 'w') as csvfile:
         
         result.tofile(csvfile, sep=" ", format="%i")

    # Get the data via the buffer interface
#  
#    result = numpy.frombuffer(vtk_array, dtype=dtype)
#    if shape[1] == 1:
#        shape = (shape[0], )
#    result.shape = shape
#    return result 
#     
#     
     
     
     
     
     
     
     
     
     
     
     
     
     
#    print "The raw image:"
#    print_image_info(image)
#    
#    resam_image = resample_image(image)
#    
#    print "The resampledimage:"
#    
#    print_image_info(resam_image)
#    
#    voi = extract_image_voi(resam_image)
#    
#    
#    print "The voi:"
#    
#    print_image_info(voi)
#        
#        
#        
#    dis_voi = image_cast_for_visualization(voi)
#    
#   # print "Volume Render the Image :"
#  #  image_volume_render(dis_voi)
#    
#    dis_resampl_image = image_cast_for_visualization(image)
#    
#
#    print "Slice Show the Image: "
#    image_volume_slice_view(dis_resampl_image)
#    
#    
#    image_volume_slice_view(image)
#    
##    outimage = polydata_to_image(image)
#    
#    print "After Mask Slice Show"
#    image_volume_slice_view(outimage)
#    
#    from pyface.api import MessageDialog
#    dialog = MessageDialog(message="message", title="title", severity='error')
#    dialog.open()
#     
#   