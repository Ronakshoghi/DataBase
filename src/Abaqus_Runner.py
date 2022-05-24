# -*- coding: utf-8 -*-
"""
Author: Ronak Shoghi
Date: 23.05.22
Time: 11:23

Abaqus runner scrip for each key using the prepared input files
"""

import os

def Abaqus_Runner(Key, ncpu):

    Current_Path = os.getcwd()
    Keys_Path ="{}/Keys".format(Current_Path)
    os.chdir(Keys_Path)
    Key_path = os.path.abspath(Key)
    Key_Inputs_Path = "{}/inputs".format(Key_path)
    os.chdir(Key_Inputs_Path)
    os.system('abaqus job='+Key+'_Abaqus_Input_File.inp user=umat.f cpus='+str(ncpu)+' int')
    os.system('abaqus python Abaqus_Post_Processing.py')
    os.chdir(Current_Path)

