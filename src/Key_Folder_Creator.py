# -*- coding: utf-8 -*-
"""
Author: Ronak Shoghi
Date: 17.05.22
Time: 11:42

This function creates a local folder with the specified path for each key.
"""
import os
Source_Path = os.getcwd()
os.chdir('..')
Current_Path = os.getcwd()

def Create_Key_Folder(Current_Path):
    try:
        if not os.path.exists(Current_Path):
            os.makedirs(Current_Path)
    except OSError:
        print ('Error: Creating directory. ' +  Current_Path)


def Create_Sub_Folder(Key):
    Create_Key_Folder(Key)
    folders = ['inputs', 'results']
    for folder in folders:
        os.mkdir(os.path.join(Key, folder))

# Key = "ABC"
# Create_Sub_Folder(Key)