#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 11:04:40 2022

@author: smidtjzh

Script to create a material.inp file for an Abaqus input file. The material 
description is erased from the original inputfile and a sperate material file
is created. This new file is linked to the original inputfile with *Include.

matfile = Name of material file which is created
loadfile = Name of loadfile which is used in simulation (e.g. remPart.inp)
orifile = Name of file with grain orientations from MTEX or Kanapy
inputfile= Name of original, periodic input file

Returns:
    matfile (e.g. Material.inp)
    
"""
import numpy as np


matfile = 'Material.inp' 
loadfile = 'remPart.inp'
orifile = 'Ronak_Orientation.txt'
inputfile = 'geometry_Periodic.inp'

# Create Material.inp
angles = np.genfromtxt(orifile, skip_header=1)
mat_id = 2. # Refers to material id in 'mod_alloys.f' from UMAT       
mat_file = open(matfile, 'w+')
headlines = ['**\n', '** MATERIALS\n', '**\n']
mat_file.writelines(headlines)

for i, angle in enumerate(angles):
    ang_str = str(angle[0])+','+str(angle[1])+','+str(angle[2])
    content = ['*Material, name=Material-'+str(i+1)+'\n', '*Depvar\n','    200,\n',
               '*User Material, constants=4\n', str(mat_id)+','+ang_str+'\n']
    mat_file.writelines(content)
mat_file.write('**')
mat_file.close()

# Delete Material from input file
includelines = ['**\n', '*Include, input='+matfile+'\n',
                '**\n', '*Include, input='+loadfile+'\n','**\n']
with open(inputfile, 'r') as f:
    lines = f.readlines()
with open(inputfile, 'w') as f:
    for line in lines:
        f.write(line)
        if '*End Assembly' in line:
            break
    f.writelines(includelines)

        
