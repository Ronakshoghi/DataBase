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


def geom_input_generator(abaqus_temp_files_path):
    geometry_file_path = "{}/geometry_Periodic.inp".format(abaqus_temp_files_path)
    with open(geometry_file_path, "r") as fr:
        material_addition = ['**\n', '*Include, input=' + "Material.inp" + '\n']
        prev_line = False
        lines = []
        for line in fr:
            if not prev_line:
                lines.append(line)
            if '*End Assembly' in line:
                prev_line = True
    with open(geometry_file_path, 'w') as fr:
        for line in lines:
            fr.write(line)
        fr.writelines(material_addition)
    return None


# A function to generate the geometry input file for each key, look for the key folder and write the geom file in that.
# The name also changes for each key
# abaqus_temp_files_path = "{}/Abaqus_Temp_Files".format(current_path)


def abaqus_input_generator(Key):
    current_path = os.getcwd()
    abaqus_temp_files_path = "{}/Abaqus_Temp_Files".format(current_path)
    geom_input_generator(abaqus_temp_files_path)
    geometry_file_path = "{}/geometry_Periodic.inp".format(abaqus_temp_files_path)
    material_file_path = "{}/Material.inp".format(abaqus_temp_files_path)
    orientation_file_path = "{}/Orientation.txt".format(abaqus_temp_files_path)
    keys_path = "{}/Keys".format(current_path)
    os.chdir(keys_path)
    key_path = os.path.abspath(Key)
    key_inputs_path = "{}/inputs".format(key_path)
    files_path = [geometry_file_path, material_file_path, orientation_file_path]
    for file in files_path:
        shutil.copy2(file, key_inputs_path)
    result = []
    for root, dir, files in os.walk(key_inputs_path):
        for filename in files:
            if "remPart" in filename:
                result.append(os.path.join(root, filename))
    load_file_path = result[0]
    load_file_name = os.path.basename(load_file_path)
    geom_file_path = "{}/geometry_Periodic.inp".format(key_inputs_path)
    with open(geom_file_path, "a") as fr:
        load_addition = ['**\n', '*Include, input=' + load_file_name + '\n', '**\n']
        fr.writelines(load_addition)
    fr.close()
    geom_file_name_new = Key + "_Abaqus_Input_File.inp"
    os.chdir(key_inputs_path)
    geom_file_name_new_path = os.path.abspath(geom_file_name_new)
    os.rename(geom_file_path, geom_file_name_new_path)
    os.chdir(current_path)


def openphase_input_generator(load, key, n_grains_per_dir, elements_per_grain, ori_file='Orientation.txt'):
    """
    This function modifies the ProjectInput.opi and the Matchbox.cpp. Currently, loads are changed according to load
    variable, discretization is changed according to n_grains and elments_per_grain.
    :param elements_per_grain:
    :param n_grains_per_dir:
    :param load:
    :param key:
    :return:
    """

    current_path = os.getcwd()
    temp_files_path = "{}/OpenPhase_Temp_Files".format(current_path)
    input_file = "{}/ProjectInput.opi".format(temp_files_path)
    cpp_file = "{}/MatchBox.cpp".format(temp_files_path)
    make_file = "{}/Makefile".format(temp_files_path)


    # Modify ProjectInput.opi
    keys_path = "{}/Keys".format(current_path)
    os.chdir(keys_path)
    key_path = os.path.abspath(key)
    key_inputs_path = "{}/inputs".format(key_path)
    os.chdir(key_inputs_path)
    with open(input_file, 'r') as f:
        lines = f.readlines()
    keywords_bc_types = ['$BCX', '$BCY', '$BCZ', '$BCYZ', '$BCXZ', '$BCXY']
    keywords_bc_values = ['$BCValueX', '$BCValueY', '$BCValueZ', '$BCValueYZ', '$BCValueXZ', '$BCValueXY']
    load_dict = {}
    for idx_comp, component in enumerate(load):
        if component < -1e-5 or component > 1e-5:
            load_dict[idx_comp] = {'type': "AppliedStress", 'value': component}
        else:
            load_dict[idx_comp] = {'type': "FreeBoundaries"}
    with open("{}.opi".format(key), 'w+') as f:
        for line in lines:
            if '$SimTtl' in line:
                f.write('$SimTtl         Simulation Title                  : {}\n'.format(key))
            elif 'Type of boundary conditions:' in line:
                for idx_dir, bc_dict in load_dict.items():
                    f.write('{bckey}	Boundary condition in {dir} direction :  {value}\n'.format(
                        bckey=keywords_bc_types[idx_dir], dir=keywords_bc_types[idx_dir].split('C')[-1],
                        value=bc_dict['type']))

            elif 'Values of boundary conditions:' in line:
                # f.write('Values of boundary conditions: \n')
                for idx_dir, bc_dict in load_dict.items():
                    if 'value' in bc_dict.keys():
                        f.write(
                            '{bckey}    Mixed Value {dir}   : {value}\n'.format(bckey=keywords_bc_values[idx_dir],
                                                                                dir=
                                                                                keywords_bc_types[idx_dir].split(
                                                                                    'C')[-1],
                                                                                value=bc_dict['value']))
            elif '$Nx' in line:
                f.write('$Nx             System Size in X Direction              : {}\n'.format(n_grains_per_dir))
            elif '$Ny' in line:
                f.write('$Ny             System Size in Y Direction              : {}\n'.format(n_grains_per_dir))
            elif '$Nz' in line:
                f.write('$Nz             System Size in Z Direction              : {}\n'.format(n_grains_per_dir))
            else:
                f.write(line)
        f.close()

    # Modify the Matchbox.cpp
    with open(cpp_file, 'r') as f:
        lines = f.readlines()

    with open("MatchBox.cpp".format(key), 'w+') as f:
        for line in lines:
            if 'string OutFile' in line:
                f.write('    string OutFile       = OPSettings.TextDir +"{key}.txt";\n'.format(key=key))
            elif 'Initializations::MatchBox' in line:
                f.write('        	  Initializations::MatchBox(Phi, BC, OPSettings, {epg});\n'.format(
                    epg=int(elements_per_grain**(1/3))))
            elif 'OR.SetGrainOrientationsFromFile' in line:
                f.write('            OR.SetGrainOrientationsFromFile(Phi, "{orifile}");\n'.format(orifile=ori_file))
            else:
                f.write(line)
        f.close()

    # Copy the Makefile and the orientation file
    shutil.copy2(make_file, "Makefile")
    shutil.copy(os.path.join(temp_files_path, ori_file), ori_file)

    os.chdir(current_path)

