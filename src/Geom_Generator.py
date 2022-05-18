# -*- coding: utf-8 -*-
"""
Author: Ronak Shoghi
Date: 18.05.22
Time: 10:55

The generated geometry_Periodic.inp from Abaqus containes materials description which needs to be deleted as our own
material.inp file can be created based on the grain orientation description as orientation.txt file come from
MTEX or Kanapy. This Material.inp file needs to be added to the final geometry_Periodic.inp using *Include

geometry_Periodic.inp still lacks the load file in it.
"""
import os
import numpy as np
Source_Path = os.getcwd()
os.chdir('..')
Current_Path = os.getcwd()
def Geom_Input_Generator(Abaqus_Temp_Files_Path):

    Geoemtry_File_Path = "{}/geometry_Periodic.inp".format(Abaqus_Temp_Files_Path)
    with open(Geoemtry_File_Path, "r") as fr:
        material_addition = ['**\n', '*Include, input='+"Material.inp"+'\n']
        prev_line = False
        lines = []
        for line in fr:
            if not prev_line:
                lines.append(line)
            if '*End Assembly' in line:
                prev_line = True
    with open(Geoemtry_File_Path, 'w') as fr:
        for line in lines:
            fr.write(line)
        fr.writelines(material_addition)

# Abaqus_Temp_Files_Path = "{}/Abaqus_Temp_Files".format(Current_Path)


