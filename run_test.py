 # -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 10:03:36 2011

@author: ZouLian
@Oncology Department
@Sichuan People's Hospital
@Chengdu,Sichuan,China
"""


"""
This is the Entry point for Invoke the Test codes


"""

from test.test_volume_image_slice_views import test_volume_image_slicer

from test.test_dicom_exporter import test_dicom_exporter

from mphantom.api import ActorsViewer,VTKFileGeometry, STLFileGeometry,ELEMENT_LIB_PATH,set_element_lib_path



if __name__ == '__main__':
    
    from enthought.traits.api import *
    
    class Test ( HasTraits ):
    
        value = Str( 'one' )
        values = List( [ 'one', 'two', 'three' ] )
        
        view = View( Item( 'value', editor = EnumEditor( name = 'values' ) ) )
        def _value_changed ( self, value ): 
           self.values.append( value + ' more' )
        
    Test().configure_traits()
        
        
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    set_element_lib_path(__file__)
#    print "ELEMENT_LIB_PATH : " , ELEMENT_LIB_PATH
#    
#    ELEMENT_LIB_PATH
#    
#    tt = "F:\PythonDir\MagicalPhantom\elements_lib\VTK\LiverData\IVC.vtk"
#    
#    tsize = len(tt)
#    prenum =  len(ELEMENT_LIB_PATH) 
#    
#    last = tt[prenum:tsize]
#    
#    
#    
#    print "lstrip : ", tt.lstrip(ELEMENT_LIB_PATH)
    
    a = VTKFileGeometry()
    
   
    a.configure_traits()

 
    jso = a.get_data_for_json()
    
    print jso
   
    
    viewer = ActorsViewer()
    viewer.add_actors(a.current_actor)
    viewer.configure_traits()
    
    
    