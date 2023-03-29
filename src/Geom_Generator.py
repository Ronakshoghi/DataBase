# -*- coding: utf-8 -*-
"""
Author: Ronak Shoghi
Date: 18.05.22
Time: 10:55

The generated geometry_Periodic.inp from Abaqus containes materials description which needs to be deleted as our own
material.inp file can be created based on the grain orientation description as orientation.txt file come from
MTEX or Kanapy. This Material.inp file needs to be added to the final geometry_Periodic.inp using *Include

geometry_Periodic.inp still lacks the load file in it.
This file needs to be written in the Abaqus_Constant_File.

for this code the geometry file and the remPart should be available in the key folder.
"""
import os
import shutil

def Geom_Input_Generator(Abaqus_Temp_Files_Path):
    Geometry_File_Path = "{}/geometry_Periodic.inp".format(Abaqus_Temp_Files_Path)
    with open(Geometry_File_Path, "r") as fr:
        material_addition = ['**\n', '*Include, input='+"Material.inp"+'\n']
        prev_line = False
        lines = []
        for line in fr:
            if not prev_line:
                lines.append(line)
            if '*End Assembly' in line:
                prev_line = True
    with open(Geometry_File_Path, 'w') as fr:
        for line in lines:
            fr.write(line)
        fr.writelines(material_addition)
    return None

# A function to generate the geometry input file for each key, look for the key folder and write the geom file in that.
# The name also changes for each key
# Abaqus_Temp_Files_Path = "{}/Abaqus_Temp_Files".format(Current_Path)


def Abaqus_Input_Generator(Key):
    Current_Path = os.getcwd()
    Abaqus_Temp_Files_Path = "{}/Abaqus_Temp_Files".format(Current_Path)
    Geom_Input_Generator(Abaqus_Temp_Files_Path)
    Geometry_File_Path = "{}/geometry_Periodic.inp".format(Abaqus_Temp_Files_Path)
    Material_File_Path = "{}/Material.inp".format(Abaqus_Temp_Files_Path)
    Orientation_File_Path = "{}/Orientation.txt".format(Abaqus_Temp_Files_Path)
    Keys_Path ="{}/Keys".format(Current_Path)
    os.chdir(Keys_Path)
    Key_path = os.path.abspath(Key)
    Key_Inputs_Path = "{}/inputs".format(Key_path)
    files_path = [Geometry_File_Path, Material_File_Path, Orientation_File_Path]
    for file in files_path:
        shutil.copy2(file, Key_Inputs_Path)
    result = []
    for root, dir, files in os.walk(Key_Inputs_Path):
        for filename in files:
            if "remPart" in filename:
                result.append(os.path.join(root, filename))
    Load_File_Path = result[0]
    Load_File_Name = os.path.basename(Load_File_Path)
    Geom_File_Path = "{}/geometry_Periodic.inp".format(Key_Inputs_Path)
    with open(Geom_File_Path, "a") as fr:
         load_addition = ['**\n', '*Include, input='+Load_File_Name+'\n','**\n']
         fr.writelines(load_addition)
    fr.close()
    Geom_File_Name_New = Key + "_Abaqus_Input_File.inp"
    os.chdir(Key_Inputs_Path)
    Geom_File_Name_New_path = os.path.abspath(Geom_File_Name_New)
    os.rename(Geom_File_Path, Geom_File_Name_New_path)
    os.chdir(Current_Path)




