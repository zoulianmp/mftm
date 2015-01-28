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
    hu_min = -1000
    hu_max = 800
    
    
    y_label = Unicode('Relative Eletron Density')
   
    re_electronic_density=Array(value=[0,0.21,0.94,1.0,1.04,1.5])
    ed_min = 0
    ed_max = 1.5
  
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
        
        size = len (self.ct_hu)
     
        self.hu_min = int(self.ct_hu[0])
        self.hu_max = int(self.ct_hu[size-1])
        
        self.ed_min = float(self.re_electronic_density[0])
        self.ed_max = float(self.re_electronic_density[size-1])
  
        
    def update_show_curve(self):
        plotdata = ArrayPlotData(x=self.ct_hu, y=self.re_electronic_density)
        plot = Plot(plotdata)
        plot.plot(("x", "y"), type="line", color="blue")              
       
        plot.title = self.name
        self.plot = plot
        
           
    def get_edensity_from_hu(self,huvalue):
        
        """ Get the E Density frome HUArray """
        f = interp1d(self.ct_hu, self.re_electronic_density)
        
              
        if huvalue > self.hu_max :
            from .util import message_box
            message = "HU is bigger than the maximun of HU-EDensity curve, \
                       Using the curve's HU maximun for following processing.\
                       current HU = {0}, the curve HU maximun = {1}".format(huvalue,self.hu_max)
            title = "HU out of the HU-EDensity Curve Range"            
            message_box(message,title,"information")
            
            return float(f(self.hu_max))
            
        if huvalue < self.hu_min :
            from .util import message_box
            message = "HU is smaller than the minimun of HU-EDensity curve, \
                       Using the curve's HU minimun for following processing. \
                       current HU = {0}, the curve HU minimun = {1}".format(huvalue,self.hu_min)
            title = "HU out of the HU-EDensity Curve Range"            
            message_box(message,title,"information")
            
            return float( f(self.hu_min))
        
        return float(f(huvalue))


   
   
      
    def get_hu_from_edensity(self,edensityvalue):
        
        """ Get the E Density frome HUArray """
        f = interp1d(self.re_electronic_density,self.ct_hu)
        
                
        if edensityvalue > self.ed_max :
            from .util import message_box
            message = "Electronic density is bigger than the maximun of HU-EDensity curve, \
                       Using the curve's ED maximun for following processing.\
                       current ed = {0}, the curve ED maximun = {1}".format(edensityvalue,self.ed_max)
            title = "ED out of the HU-EDensity Curve Range"            
            message_box(message,title,"information")
            
            return int (f(self.ed_max))
            
        if edensityvalue < self.ed_min :
            from .util import message_box
            message = "Electronic density is smaller than the minimun of HU-EDensity curve, \
                       Using the curve's ED minimun for following processing.\
                       current ed = {0}, the curve ED minimun = {1}".format(edensityvalue,self.ed_min)
            title = "ED out of the HU-EDensity Curve Range"            
            message_box(message,title,"information")
            
            return int(f(self.ed_min))
            
            
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
   