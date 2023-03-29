# -*- coding: utf-8 -*-
"""
Author: Ronak Shoghi
Date: 18.05.22
Time: 10:34


A Function to create materials.inp file based on the generated geometry_Periodic.inp file and an orientation file
provided in the Abaqus_temp_Files folder. The orienttaion file should be saved as Orientaion.txt in
Abaqus_Temp_Files_Path
"""

import os
import numpy as np


def Material_Orientation_Generator(Abaqus_Temp_Files_Path):

    Orientation_File_Path = "{}/Orientation.txt".format(Abaqus_Temp_Files_Path)
    material_ID = 2
    with open(Orientation_File_Path, 'r') as f:
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

Current_Path = os.getcwd()
Abaqus_Temp_Files_Path = "{}/Abaqus_Temp_Files".format(Current_Path)
Material_Orientation_Generator(Abaqus_Temp_Files_Path)
