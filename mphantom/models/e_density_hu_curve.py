# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 15:08:10 2011

@author: ZouLian
@Oncology Department
@Sichuan People's Hospital
@Chengdu,Sichuan,China
"""

# Enthought library imports.
from traits.api import Array, HasTraits, Unicode,Float,Instance,Str

from traitsui.api import View, Item
from chaco.api import Plot, ArrayPlotData
from enable.component_editor import ComponentEditor
import numpy as np

from scipy.interpolate import interp1d


class EDensityHUCurve(HasTraits):
    """ The model object for the EDensity HU Curve.
    """
    #Path for multi Electronic Density to HU Curve Files
    path = Str("./") #"The Path for Selected ED to HU Curve File"



    #### 'EDensityHUCurve' interface #################################################

    name = Unicode('ED - HU Curve of Scanner')
    
    
    x_label= Unicode('Hounsfield Units') 
    
    ct_hu =Array(value=[-1000,-840,-80,0,20,800])
    
    
    
    y_label = Unicode('Relative Eletron Density')
   
    re_electronic_density=Array(value=[0,0.21,0.94,1.0,1.04,1.5])
   
  
    # Chaco Plot Interface
    plot = Instance(Plot)
    traits_view = View(
        Item('plot',editor=ComponentEditor(), 
             show_label=False),
        width=500, 
        height=500, 
        resizable=True, 
        kind = 'livemodal',
        title= 'Selected Scanner ED-HU Curve')
    
    ###########################################################################
    # 'EDensityHUCurve' interface.
    ###########################################################################
    def __init__(self,**traits):
        super(EDensityHUCurve, self).__init__(**traits)
        self.update_show_curve()
        
    def _path_changed(self,newpath):
        self._get_data_from_file(newpath)
        self.update_show_curve()
        
                
        
    def _get_data_from_file(self,fname):
        array = np.loadtxt(fname, delimiter=',',dtype=float)        
        self.re_electronic_density = array[:,1]
        self.ct_hu = array[:,0]
        
        
    def update_show_curve(self):
        plotdata = ArrayPlotData(x=self.ct_hu, y=self.re_electronic_density)
        plot = Plot(plotdata)
        plot.plot(("x", "y"), type="line", color="blue")              
       
        plot.title = self.name
        self.plot = plot
        
           
    def get_edensity_from_hu(self,huvalue):
        
        """ Get the E Density frome HUArray """
        f = interp1d(self.ct_hu, self.re_electronic_density)
        
        return f(huvalue)


   
   
      
    def get_hu_from_edensity(self,edensityvalue):
        
        """ Get the E Density frome HUArray """
        f = interp1d(self.re_electronic_density,self.ct_hu)
        
        return int(f(edensityvalue))

   
    
    ###########################################################################
    # Protected interface.
    ###########################################################################

  
if __name__ == "__main__":
   
    A = EDensityHUCurve()
    
  #  path = './../scanners/GE64.txt'
    
  #  A.get_data_from_file(path)
       
  # A.update_curve()
    
    ed = 1.1
    hu = A.get_hu_from_edensity(ed)
    
    print "ed = ", ed
    print "hu = ", hu
     
    edrec = A.get_edensity_from_hu(hu+1)
    
    print " edrec = " , edrec
    A.configure_traits()
   