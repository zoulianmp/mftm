from tvtk.api import tvtk
from traits.api import File,HasTraits,Str
from traitsui.api import View, Item

from base_geometry import BaseGeometry

class STLFileGeometry(BaseGeometry):
    
    
     geometry_typle = Str('STLFileGeometry')
    
     external_file_name = File()
     
     file_reader = tvtk.STLReader()
    
     
     def __init__(self,**traits):
        super(STLFileGeometry,self).__init__(**traits)
        self.geometry_typle = 'STLFileGeometry'
        
        
         
     def _external_file_name_changed(self,old,new): 
         
          self.file_reader.file_name = new
          self.file_reader.update()
          self.init_poly = self.file_reader.output
          
    
     def get_data_for_json(self):
          '''Get a dict data for json output '''
          data = {}
          data["GeoType"] = "STLExternalFile" 
          data["InitialParams"] = [self.external_file_name]
       
          return data       
     
     
     
     traits_view = View(
                Item(name='external_file_name')
                     #filter = '*.vtk')
                )
       
      


if __name__ == '__main__':
    a = STLFileGeometry()
    
    a.configure_traits()

 

    
    from mphantom.api import ActorsViewer
    
    viewer = ActorsViewer()
    viewer.add_actors(a.current_actor)
    viewer.configure_traits()
    
    
    