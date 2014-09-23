#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-
# util.py
"""Several utility functions that don't really belong anywhere."""
#


import imp, os, sys




def get_main_dir():
          
    mainpath = os.getcwd()
    return mainpath


#**********************************************
#Ensure the directory is here
#**********************************************
def ensure_dir(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)