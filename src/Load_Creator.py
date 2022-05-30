# -*- coding: utf-8 -*-
"""
Author: Ronak Shoghi
Date: 17.05.22
Time: 11:00

a function to create the load cases for the Abaqus input file. This script creates the remPart.inp file based on the 6D unit stresses distributed on surfce of unit sphere.
The result would be n rempart.inp files
the input required for this function is sigdata as text file.

"""
import os

def Load_File_Generator(load, key ):
    Current_Path = os.getcwd()
    Abaqus_Temp_Files_Path = "{}/Abaqus_Temp_Files".format(Current_Path)
    remPart_File = "{}/remPart.inp".format(Abaqus_Temp_Files_Path)
    Keys_Path ="{}/Keys".format(Current_Path)
    os.chdir(Keys_Path)
    Key_path = os.path.abspath(key)
    Key_Inputs_Path = "{}/inputs".format(Key_path)
    os.chdir(Key_Inputs_Path)
    with open(remPart_File, 'r') as f:
        lines = f.readlines()

    with open("{}_remPart_file.inp".format(key), 'w+') as f:
        for line in lines:
            if 'V2,1' in line:
                f.write('V2,1, {}\n'.format(load[0]))
            elif 'V4,2' in line:
                f.write('V4,2, {}\n'.format(load[1]))
            elif 'H1,3' in line:
                f.write('H1,3, {}\n'.format(load[2]))
            elif 'H1,2' in line:
                f.write('H1,2, {}\n'.format(load[3]))
            elif 'V2,3' in line:
                f.write('V2,3, {}\n'.format(load[4]))
            elif 'V4,1' in line:
                f.write('V4,1, {}\n'.format(load[5]))
            else:
                f.write(line)
        f.close()

    os.chdir(Current_Path)
    return None
