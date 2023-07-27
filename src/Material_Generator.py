# -*- coding: utf-8 -*-
"""
Author: Ronak Shoghi
Date: 18.05.22
Time: 10:34


A Function to create materials.inp file based on the generated geometry_Periodic.inp file and an orientation file
provided in the Abaqus_temp_Files folder. The orienttaion file should be saved as Orientaion.txt in
abaqus_temp_files_path
"""

import os
import numpy as np


def material_orientation_generator(Abaqus_Temp_Files_Path):
    orientation_file_path = "{}/Orientation.txt".format(Abaqus_Temp_Files_Path)
    material_ID = 2
    with open(orientation_file_path, 'r') as f:
        orientations = np.genfromtxt(f, skip_header=1)
    file = "Material.inp"
    with open(os.path.join(Abaqus_Temp_Files_Path, file), 'w') as mr:
        headers = ['**\n', '** MATERIALS\n', '**\n']
        mr.writelines(headers)
        for i, orientation in enumerate(orientations):
            orientation_str = str(orientation[0]) + ',' + str(orientation[1]) + ',' + str(orientation[2])
            content = ['*Material, name=Material-' + str(i + 1) + '\n', '*Depvar\n', '    200,\n',
                       '*User Material, constants=4\n', str(material_ID) + ',' + orientation_str + '\n']
            mr.writelines(content)
        mr.write('**')
        mr.close()
        return None


current_path = os.getcwd()
Abaqus_Temp_Files_Path = "{}/Abaqus_Temp_Files".format(current_path)
material_orientation_generator(Abaqus_Temp_Files_Path)
