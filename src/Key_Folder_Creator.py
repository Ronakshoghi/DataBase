# -*- coding: utf-8 -*-
"""
Author: Ronak Shoghi
Date: 17.05.22
Time: 11:42

This function creates a local folder with the specified path for each key.
"""
import os
import shutil


def Create_Key_Folder(Keys_Folder_Name, CP):
    Keys_Path = "{}/Keys".format(CP)
    os.chdir(Keys_Path)
    try:
        if not os.path.exists(Keys_Folder_Name):
            os.makedirs(Keys_Folder_Name)
    except OSError:
        print ('Error: Creating directory. ' +  Keys_Folder_Name)


# a function to create 2 subfolder of inputs and results for each key and copy the constant abaqus file into the input.

def Create_Sub_Folder(Key):
    Current_Path = os.getcwd()
    Abaqus_Constant_Files_Path = "{}/Abaqus_Constant_Files".format(Current_Path)
    Create_Key_Folder(Key, Current_Path)
    folders = ['inputs', 'results']
    for folder in folders:
        try:
            if not os.path.exists(os.path.join(Key, folder)):
                os.makedirs(os.path.join(Key, folder))
        except OSError:
            print('Error: Creating directory. ' + os.path.join(Key, folder))
    Current_Path_1 = os.path.abspath(Key)
    Key_Inputs_Path = "{}/inputs".format(Current_Path_1)
    for file_name in os.listdir(Abaqus_Constant_Files_Path):
        source = os.path.join(Abaqus_Constant_Files_Path, file_name)
        destination = os.path.join(Key_Inputs_Path, file_name)
        if os.path.isfile(source):
            shutil.copy(source, destination)
    os.chdir(Current_Path)

