from tvtk.api import tvtk
from traits.api import File,HasTraits
from traitsui.api import View, Item


class VTKExternalFileReader(HasTraits):
    
     external_file_name = File()
     
     poly_data_reader = tvtk.PolyDataReader()
     
     output = poly_data_reader.output
     

         
     def _external_file_name_changed(self,old,new): 
        self.poly_data_reader.file_name = new
     
     
     
     
     traits_view = View(
                Item(name='external_file_name')
                     #filter = '*.vtk')
                )
       
      


if __name__ == '__main__':
    a = VTKExternalFileReader()
    
    a.configure_traits()

