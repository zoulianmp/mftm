# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 14:37:11 2011

@author: ZouLian
@Oncology Department
@Sichuan People's Hospital
@Chengdu,Sichuan,China
"""

try:
    import vtk
except ImportError,m:
    m.args = ('%s\n%s\nDo you have vtk and its Python bindings installed properly?'%
                       (m.args[0],'_'*80),)

from traits.api import HasTraits, Instance,  List, Unicode, Event,on_trait_change
from traitsui.api import View, Item, Spring, Group


from base_element import BaseElement
from single_element import SingleElement
#from compound_element import CompoundElement

from traitsui.menu import OKCancelButtons


from apptools.persistence import state_pickler

######################################################################

class PhantomModel(HasTraits):
    '''
    A Phantom Model Class for Phantom Construction and CTScanner Output
    '''
    
    phantomname = Unicode('NewPhantom')    
    #The Single elements list 
    single_elements = List(SingleElement)
    
    
    # The Compound elements list
    #compound_elements = List(CompoundElement)
    
    #Current Selected Element
    current_element = Instance(BaseElement)
    
    #Flag the Phantom  is updated
    updated = Event
    
   
    
    # ct_scanner = BaseElement
    
     
    space =Group( Spring (),
                  Spring (),
                  Spring (),
                  Spring ())
      
    ######################
    view = View(  
                  Spring (),
                  Item(name ='phantomname',
                       label='The New Phantom Name',),
                  Item('_'),
               
                  Spring (),
                  Spring (),
                  
                
                  
                  space,
                  buttons = OKCancelButtons,
                  title = ' New Phantom ....',
                  height= 400,
                  width = 250,
                  kind = 'livemodal'
                  
                )
  

###########################################################
#'object' interface
###########################################################
#  
    
    
    
    def __get_pure_state__(self):
        d = self.__dict__.copy()
        for x in ['updated','space','view']:
            d.pop(x,None)
            
        return d
        
        
        
    def __set_pure_state__(self,state):
                
        #################################################
        # Utility for Single_elements
        #################################################
        
        #current number single elements
        n_s = len(self.single_elements)
        
        #number of single elements in saved state
        n_saved_s = len(state.single_elements)        
        
        #remove extra ones
        for i in range(n_s - n_saved_s):
            self.single_elements.pop(-1)
        
        #add New ones 
        for i in range(n_saved_s - n_s):
            se = SingleElement()
            
            self.single_elements.append(se)
            
        #################################################
        # Utility for compound_elements
        #################################################
        
        #current number single elements
        n_c = len(self.compound_elements)
        
        #number of single elements in saved state
        n_saved_c = len(state.compound_elements)        
                
        
        #remove extra ones
        for i in range(n_c - n_saved_c):
            self.compound_elements.pop(-1)
        
        #add New ones 
        for i in range(n_saved_c - n_c):
            se = CompoundElement()
            
            self.compound_elements.append(se)
            
        #################################################class_name
        # Utility for set current_element
        #################################################
        
        state_ce = state.current_element
        
        classname = state_ce.__metadata__['class_name']
        
        if classname =='SingleElement':
            ce = SingleElement()
        elif classname =='CompoundElement':
            ce = CompoundElement()
        else:
            ce = BaseElement()
                
       
        self.current_element = ce
            
        #################################################    
        # Set State
        
        state_pickler.set_state(self,state)
        
    
        
   ###############################################################
   # Phantom Model Interface
   ###############################################################
   
    def save_phantom(self, file_or_fname):
        """Given a file or a file name, this saves the current phantom to the 
        file.
        """
        o = vtk.vtkObject 
        w = o.GetGlobalWarningDisplay()
        o.SetGlobalWarningDisplay(0) # Turn it off
        
        try:
            state_pickler.dump(self,file_or_fname)
        finally:
            #Reset the warning state
            o.SetGlobalWarningDisplay(w)
            
            
    
    def load_phantom(self,file_or_fname):
        """Given a file or a file name, this load the  phantom ."""
        
        #Save the state of VTK's gloabl warning display.
        o = vtk.vtkObject 
        w = o.GetGlobalWarningDisplay()
        o.SetGlobalWarningDisplay(0) # Turn it off
        
        try:
            
            state = state_pickler.load_state(file_or_fname)
            state_pickler.update_state(state)
            self.__set_pure_state__(state)
        
            
            print file_or_fname
            #Get the state from the file 
         
          
            
        finally:
            #Reset the warning state
            o.SetGlobalWarningDisplay(w)
            
    # Save the current element geometry    
    def save_current_element_geometry(self,fname):
        geometry = self.current_element.geometry
        
        geometry.save_geometry(fname)
      
      
    #Get the sorted elements by priority
    #The higher priority ,the fronter position of element
    def get_sorted_elements_by_priority(self):
        
        from collections import OrderedDict
        
        e_dict = { }
  
        for element in self.single_elements:
            key = element.priority 
            e_dict[key] = element
               
#         
#        for element in self.compound_elements:
#            key = element.priority 
#            e_dict[key] = element
#             
        
        # dictionary sorted by key
        orddict = OrderedDict(sorted(e_dict.items(), key=lambda t: t[0])) 
        #orddict = OrderedDict(sorted(e_dict.items(), key=lambda t: t[0],reverse=True)) 
       
        
        return orddict.items()
        




      
    #Get the Phantom Bounds          
    def get_bounds(self):
        
        xmin = 0
        xmax = 0
        
        ymin = 0
        ymax = 0

        zmin = 0
        zmax = 0
        
        if len(self.single_elements) >0:
            bounds = self.single_elements[0].get_bounds()
            xmin = bounds[0]
            xmax = bounds[1]
        
            ymin = bounds[2]
            ymax = bounds[3]

            zmin = bounds[4]
            zmax = bounds[5]
#        elif len(self.compound_elements) >0 :
#            bounds = self.compound_elements[0].get_bounds()
#            xmin = bounds[0]
#            xmax = bounds[1]
#        
#            ymin = bounds[2]
#            ymax = bounds[3]
#
#            zmin = bounds[4]
#            zmax = bounds[5]
        else:
            return              
        
        #Iterating the single elements
        for element in self.single_elements:
            tbounds = element.get_bounds()
            
            if tbounds[0] < xmin :
                xmin = tbounds[0]
            
            if tbounds[1] > xmax :
                xmax = tbounds[1]
                
            if tbounds[2] < ymin :
                ymin = tbounds[2]
                
            if tbounds[3] > ymax :
                ymax = tbounds[3]
                
            if tbounds[4] < zmin :
                zmin = tbounds[4]
                
            if tbounds[5] > zmax :
                zmax = tbounds[5]
            
##         #Iterating the single elements      
##         for element in  self.compound_elements:
##             tbounds = element.get_bounds()
##             
##             if tbounds[0] < xmin :
##                 xmin = tbounds[0]
##             
##             if tbounds[1] > xmax :
##                 xmax = tbounds[1]
##                 
##             if tbounds[2] < ymin :
##                 ymin = tbounds[2]
##                 
##             if tbounds[3] > ymax :
##                 ymax = tbounds[3]
##                 
##             if tbounds[4] < zmin :
##                 zmin = tbounds[4]
##                 
##             if tbounds[5] > zmax :
##                 zmax = tbounds[5]
##             
        bounds = (xmin,xmax,ymin,ymax,zmin,zmax)
        
        return bounds
            
        
        
        
    
    ######################
    

if __name__ == '__main__':
     a = PhantomModel()
    
     selement = SingleElement()
     
     selement.setup_geometry('buildin')
     
     print "Single Element Bounds: ", selement.get_bounds()

     a.single_elements = [selement]
     a.current_element = selement
           
           
           
     
     print "Phantom Bounds:",a.get_bounds()
  

#