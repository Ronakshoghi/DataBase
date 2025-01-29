# -*- coding: utf-8 -*-
"""
Author: Ronak Shoghi
Date: 23.05.22
Time: 11:23

Abaqus runner scrip for each key using the prepared input files
"""

import os

def Abaqus_Runner(Key, ncpu):
    print(Key)
    Current_Path = os.getcwd()
    print(Current_Path)
    Keys_Path ="{}/Keys".format(Current_Path)
    print(Keys_Path)
    os.chdir(Keys_Path)
    Key_path = os.path.abspath(Key)
    Key_Inputs_Path = "{}/inputs".format(Key_path)
    print(Key_Inputs_Path)
    os.chdir(Key_Inputs_Path)
    print('abaqus job='+ Key+'_Abaqus_Input_File.inp user=umat.f cpus='+str(ncpu)+' int')
    os.system('abaqus job='+ Key+'_Abaqus_Input_File.inp user=umat.f cpus='+str(ncpu)+' int')
    os.system('abaqus python Abaqus_Post_Processing.py')
    os.chdir(Current_Path)

