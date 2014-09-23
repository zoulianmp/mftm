 # Enthought library imports.


from traits.api import Str
from actors_viewer import ActorsViewer


class StartUpVisualView(ActorsViewer):

    #### 'ITaskPane' interface ################################################

    id = Str('mphantom.startupvisual')
    name =Str('StartUpVisual')


    
        
        
    def __init__(self,**traits):
        super(StartUpVisualView,self).__init__(**traits)
        
        self._splash_screen()
        
          
    def _splash_screen(self):
        from tvtk.api import tvtk
        
        txtprop1 = tvtk.TextProperty()
        txtprop1.font_size = 55
      #  txtprop1.shadow = False
        txtprop1.color = (1,0.7,0.5)
        
        txtactor1 = tvtk.TextActor3D()
        txtactor1.input ="Magical Phantom " 
        txtactor1.text_property = txtprop1
        txtactor1.position = (-100,100,0)
        
        
        txtprop11 = tvtk.TextProperty()
        txtprop11.font_size = 25
      #  txtprop1.shadow = False
        txtprop11.color = (1,0.7,0.5)
        
        txtactor11 = tvtk.TextActor3D()
        txtactor11.input ="Version 2.0 " 
        txtactor11.text_property = txtprop11
        txtactor11.position = (250,80,0)
        
        
   
        
        txtprop2 = tvtk.TextProperty()
        txtprop2.font_size = 30
      #  txtprop2.shadow = False
        txtprop2.color = (1,0.7,0.5)
        txtactor2 = tvtk.TextActor3D()
        txtactor2.input ="Created by " 
        txtactor2.text_property = txtprop2
        txtactor2.position = (20,0,0)
        
        
        
        
        txtprop3 = tvtk.TextProperty()
        txtprop3.font_size = 60
      #  txtprop3.shadow = True
        txtprop3.color = (1,0.7,0.5)
        
        txtactor3 = tvtk.TextActor3D()
        txtactor3.input ="Zou Lian " 
        txtactor3.text_property = txtprop3
        txtactor3.position = (80,-100,10)
        
       
        txtprop4 = tvtk.TextProperty()
        txtprop4.font_size = 25
       # txtprop4.shadow = True
        txtprop4.color = (1,0.7,0.5)
        
        txtactor4 = tvtk.TextActor3D()
        txtactor4.input ="Joint Lab for Medical Physics &" 
        txtactor4.text_property = txtprop4
        txtactor4.position = (-80,-220,10)
        
        txtactor5 = tvtk.TextActor3D()
        txtactor5.input ="Department of Oncology," 
        txtactor5.text_property = txtprop4
        txtactor5.position = (-80,-250,10)
        
        txtactor6 = tvtk.TextActor3D()
        txtactor6.input ="Sichuan Provincial People's Hospital" 
        txtactor6.text_property = txtprop4
        txtactor6.position = (-80,-280,10)
        
        
        
        self.add_actors([txtactor1,txtactor11,txtactor2,txtactor3,
                         txtactor4,txtactor5,txtactor6])
        
        
            
   
####################################

if __name__ == '__main__':
   
   
    startup = StartUpVisualView()
   
   
    startup.configure_traits()
    
 
        
       