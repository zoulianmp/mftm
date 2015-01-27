# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 10:40:43 2011

@author: IMRTQA
"""


#*******************************************
# Gloable Varians  import
#*******************************************
from models.util import ELEMENT_LIB_PATH,CFG_PATH,MATE_LIST_FILE
from models.util import set_system_path,get_residual_filename, \
                        makesure_element_in_lib,update_material_list





from models.util import get_main_dir, ensure_dir, message_box, get_slice_from_3d_image

from models.debug_helpers import polydata_render,image_volume_render, image_volume_slice_view, \
                                 gen_image_data_by_numpy, polydata_to_image
                                
                            
from models.phantom_update_helper import PhantomUpdateHelper

from gui.test_dialog import TestDialog

#*******************************************
# Base GUI import
#*******************************************

from gui.actors_viewer import ActorsViewer

#*******************************************************
# Models import
#*********************************************EleBaseVisualProperty**********
from models.ele_base_visual_property import EleBaseVisualProperty
from models.ele_base_geometry_tuner import EleBaseGeometryTuner
from models.ele_3d_geometry_tuner import Ele3DGeometryTuner


from models.ele_general_property import EleGeneralProperty


from models.ele_3d_visual_property import Ele3DVisualProperty

from models.base_geometry import BaseGeometry
from models.cone_geometry import ConeGeometry
from models.cube_geometry import CubeGeometry
from models.cylinder_geometry import CylinderGeometry
from models.sphere_geometry import SphereGeometry

from models.stl_file_geometry import STLFileGeometry
from models.vtk_file_geometry import VTKFileGeometry



from models.base_element import BaseElement
from models.three_dimension_element import ThreeDimensionElement


from models.m_phantom import MPhantom


from models.image_set_exporter import ImageSetExporter
from models.image_export_property import ImageExportProperty
from models.image_set_info import ImageSetInfo

from models.virtual_ct_scanner import Virtual_CT_Scanner


#*******************************************************
# gui import
#*******************************************************
from gui.actors_viewer import ActorsViewer
from gui.m_phantom_tree_view import MPhantomTreeView
from gui.m_phantom_visual_view import MPhantomVisualView
from gui.element_configure_view import ElementConfigureView
from gui.phantom_editor_view import PhantomEditorView

from gui.start_up_visual_view import StartUpVisualView
from gui.volume_image_slice_views import VolumeImageSliceViews

from gui.virtual_scanning_gui import VirtualScannningGUI
from gui.phantom_factory_gui import PhantomFactoryGUI
from gui.add_3d_element_dialog import Add3DElementDialog

#*******************************************************
#Application import 
#*******************************************************
from gui.mphantom_application import MPhantomApplication


#*******************************************************
#Plugins import 
#*******************************************************

from gui.run_manager_plugin import RunManagerPlugin, RunManager
from gui.mphantom_ui_plugin import MPhantomUIPlugin





#*******************************************
# Actions import
#*******************************************

from gui.mphantom_actions import NewPhantomAction,LoadPhantomAction

from gui.mphantom_actions import RenamePhantomAction, LoadPhantomAction, SavePhantomAction, \
                                 Add3DElementAction, DeletCurrentElementAction
                                 
from gui.mphantom_actions import ScannerTaskAction,ModelingTaskAction,StartupTaskAction



#*******************************
#*** Test Functions ************
#*******************************

#from debug_helpers import image_volume_render, polydata_render

