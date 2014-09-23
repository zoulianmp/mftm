 # Enthought library imports.

from traits.api import HasTraits, Str, List,Instance,DelegatesTo
from traitsui.api import TreeEditor, TreeNode, Item, View
         
from traitsui.menu \
    import Menu, Action, Separator




from mphantom.api import BaseElement, MPhantom,ThreeDimensionElement
#from phantom_actions import RenamePhantomAction

############################################################
# Phantom Tree View Nodes Classes,Used for User UI
############################################################


class MPhantomTreeView(HasTraits):
    
    # phantom = Instance(PhantomModel)
   
    
    tree_editor = Instance(TreeEditor)
    
    phantom = Instance(MPhantom)
    
    current_element =DelegatesTo('phantom')
    
    def _tree_editor_default(self):
           
        editor = TreeEditor(
                    editable=False,
                    nodes = [
                    
                    TreeNode( node_for  = [ MPhantom ],
                              auto_open = True,
                              children  = '',
                              label     = 'name',
                              menu      = Menu(),
                              view      = View()),

                                                  
                    TreeNode( node_for  = [ MPhantom ],
                              auto_open = True,
                              children  = 'three_dimension_elements',
                              label     = '=3DElements',
                              menu      = Menu(),
                              view      = View(),
                              add       = [  ]),
                             
                    
                    TreeNode( node_for  = [ ThreeDimensionElement ],
                              auto_open = True,
                              label     = 'name',
                              menu      = Menu(),
                              view = View()),
#                              
#                    TreeNode( node_for  = [ CompoundElement ],
#                              auto_open = True,
#                              label     = 'name',
#                              menu      = Menu(),
#                              view = View())
                              
                             ],
                   selected = 'current_element', 
                   on_select = self._on_node_selection
                 )
                 
        return editor


                                               


    def default_traits_view(self):

         trait_view = View(
                            Item(
                            name = 'phantom',
                            id = 'phantom Tree ',
                            editor = self.tree_editor,
                            show_label = False,
                            width = 300,
                            resizable = True ),
                          )
         return trait_view
         
#### Private traits #######################################################

    def _on_node_selection(self,object):
                 
        if isinstance(object,BaseElement):
           
            self.phantom.current_element = object
            
          
       
####################################

if __name__ == '__main__':
    
    from mphantom.api import CubeGeometry,ConeGeometry,STLFileGeometry, \
                                   ThreeDimensionElement
    cube = CubeGeometry()
   # cube.configure_traits()
    
    cone = ConeGeometry()
   # cone.configure_traits()
    
    cube_element = ThreeDimensionElement()
    cube_element.geometry = cube
   # cube_element.name = "Cube"
    cube_element.configure_traits()
    
    
    cone_element = ThreeDimensionElement()
    cone_element.geometry = cone
    cone_element.name = "Cone"
    
    phantom = MPhantom()
    
    
    phantom.add_3d_element(cube_element)
    phantom.add_3d_element(cone_element)
    
    tree =  MPhantomTreeView(phantom = phantom)
    
      
    tree.configure_traits()
    
#    tree = PhantomTreeView(phantom = phantom)
#    tree.configure_traits(view = view)
    
 
        
       