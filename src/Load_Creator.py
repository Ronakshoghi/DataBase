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


def load_file_generator(load, key):
    current_path = os.getcwd()
    temp_files_path = "{}/Abaqus_Temp_Files".format(current_path)
    rem_part_file = "{}/remPart.inp".format(temp_files_path)

    keys_path = "{}/Keys".format(current_path)
    os.chdir(keys_path)
    key_path = os.path.abspath(key)
    key_inputs_path = "{}/inputs".format(key_path)
    os.chdir(key_inputs_path)
    with open(rem_part_file, 'r') as f:
        lines = f.readlines()

    with open("{}_remPart_file.inp".format(key), 'w+') as f:
        for line in lines:
            if 'V2,1' in line:
                f.write('V2,1, {}\n'.format(load[0]))
            elif 'V4,2' in line:
                f.write('V4,2, {}\n'.format(load[1]))
            elif 'H1,3' in line:
                f.write('H1,3, {}\n'.format(load[2]))  # I think in Abaqus we have to flip this axis!
            elif 'H1,2' in line:
                f.write('H1,2, {}\n'.format(load[3]))
            elif 'V2,3' in line:
                f.write('V2,3, {}\n'.format(load[4]))
            elif 'V4,1' in line:
                f.write('V4,1, {}\n'.format(load[5]))
            else:
                f.write(line)
        f.close()

    os.chdir(current_path)
    return None
