# -*- coding: utf-8 -*-
"""
Author: Ronak Shoghi
Date: 17.05.22
Time: 11:00

a function to create the load cases for the Abaqus input file. This script creates the remPart.inp file based on the 6D unit stresses distributed on surfce of unit sphere.
The result would be n rempart.inp files
the input required for this function is sigdata as text file.
"""
import numpy as np

# rempart_file = 'remPart.inp'
# load_cases = 'sigdata1.txt'

def Load_File_Generator(load_cases, rempart_file ):

    loads = np.genfromtxt(load_cases)
    with open(rempart_file, 'r') as f:
        lines = f.readlines()

    for i, load in enumerate(loads):
        with open("rempart_file_{}".format(i), 'w+') as f:
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
    #    if i==3:
    #        break
    return None
