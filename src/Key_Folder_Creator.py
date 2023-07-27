# -*- coding: utf-8 -*-
"""
Author: Ronak Shoghi
Date: 17.05.22
Time: 11:42

This function creates a local folder with the specified path for each key.
"""
import os
import shutil


def create_key_folder(keys_folder_name, cp):
    keys_path = "{}/Keys".format(cp)
    if not os.path.exists(keys_path):
        os.mkdir(keys_path)
    os.chdir(keys_path)
    try:
        if not os.path.exists(keys_folder_name):
            os.makedirs(keys_folder_name)
    except OSError:
        print('Error: Creating directory {}.'.format(keys_folder_name))


# a function to create 2 subfolder of inputs and results for each key and copy the constant abaqus file into the input.

def create_sub_folder(key, cp_code='abaqus'):
    current_path = os.getcwd()
    if cp_code == 'abaqus':
        constant_files_path = "{}/Abaqus_Constant_Files".format(current_path)
    elif cp_code == 'openphase':
        constant_files_path = "{}/OpenPhase_Constant_Files".format(current_path)
    else:
        raise ValueError("cp_code {code} not valid. Must be abaqus or openphase.".format(code=cp_code))
    create_key_folder(key, current_path)

    if cp_code == 'abaqus':
        folders = ['inputs', 'results']
        for folder in folders:
            try:
                if not os.path.exists(os.path.join(key, folder)):
                    os.makedirs(os.path.join(key, folder))
            except OSError:
                print('Error: Creating directory. ' + os.path.join(key, folder))
        current_path_1 = os.path.abspath(key)
        key_inputs_path = "{}/inputs".format(current_path_1)
        for file_name in os.listdir(constant_files_path):
            source = os.path.join(constant_files_path, file_name)
            destination = os.path.join(key_inputs_path, file_name)
            if os.path.isfile(source):
                shutil.copy(source, destination)

    #TODO: Which are the OpenPhase files that need to be copied? Do I have constant files? Where are Temp Files copied?
    elif cp_code =='openphase':
        print('Current state: no constant files, all temporary. I do not create subfolders "input" and "results".')
    os.chdir(current_path)

