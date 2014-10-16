# -*- coding: utf-8 -*-
"""
Created on Thu Dec 05 14:44:29 2013

@author: ZouLian
@Joint Lab for Medical Physics
@Oncology Department
@Sichuan People's Hospital
@Chengdu,Sichuan,China

"""

# configure_traits_view_buttons.py -- Sample code to demonstrate
#                                     configure_traits()

from traits.api import HasTraits, Str, Int
from traitsui.api import View, Item
from traitsui.menu import OKButton, CancelButton

class TestDialog(HasTraits):
    first_name = Str
    last_name = Str
    department = Str

    employee_number = Str
    salary = Int

    view1 = View(Item(name = 'first_name'),
             Item(name = 'last_name'),
             Item(name = 'department'),
             buttons = [OKButton, CancelButton],
             kind= 'livemodal')

