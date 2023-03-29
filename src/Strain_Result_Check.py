# -*- coding: utf-8 -*-
"""
Author: Ronak Shoghi
Date: 24.05.22
Time: 15:08

"""
import os
from numpy import genfromtxt

def Max_Strain_Finder (Key):

    Current_Path = os.getcwd()
    Keys_Path ="{}/Keys".format(Current_Path)
    os.chdir(Keys_Path)
    Key_path = os.path.abspath(Key)
    Key_Results_Path = "{}/results".format(Key_path)
    os.chdir(Key_Results_Path)
    Strains = genfromtxt('E.out', delimiter=' ')
    os.chdir(Current_Path)
    return (max(Strains))