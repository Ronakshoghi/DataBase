# -*- coding: utf-8 -*-
"""
Author: Ronak Shoghi
Date: 06.05.22
Time: 13:46


This function reads the system related meta data
"""

import platform
import socket
import uuid
import re
import getpass
from datetime import date
import os
import Database_Handler as DC
import json


"""
This function reads Meta data in inout folder for each key and writes them in the JSON database
"""

def Meta_reader(Key):
    parameters = Key.split('_')
    Key_Parsed = {"Stress_Type": parameters[0], "Load_Descriptor": parameters[1], "Hash_Load": parameters[2],
                   "Hash_Orientation": parameters[3], "Texture_Type": parameters[4]}
    uname = platform.uname()
    Meta = {
         'Owner':getpass.getuser(),
          "Institution" : "ICAMS, Ruhr University Bochum, Germany",
         'Date': date.today().strftime("%d %B %Y"),
         'System': uname.system,
         'Ip-Address': socket.gethostbyname(socket.gethostname()),
         'Mac-Address': ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        }
    Current_Path = os.getcwd()
    Keys_Path ="{}/Keys".format(Current_Path)
    os.chdir(Keys_Path)
    Key_path = os.path.abspath(Key)
    Key_Input_Path = "{}/inputs".format(Key_path)
    Key_Results_Path = "{}/results".format(Key_path)
    # Meta['Inputs-Path'] = Key_Input_Path
    # Meta['Results-Path'] = Key_Results_Path
    os.chdir(Key_Input_Path)
    Input_File=open('{}_Abaqus_Input_File.inp'.format(Key))
    lines = Input_File.readlines()
    Abaqus_Version = (lines[2].split(':'))[1]
    Meta['Abaqus-Version'] = Abaqus_Version
    Element_Number = None
    for i, line in enumerate(lines):
        if "*Nset" in line:
            previous_line = lines[i - 1]
            Element_Number = int(previous_line.split(',')[0].strip())
            break
    Orientation_File = open('Orientation.txt')
    phi1 = []
    phi2 = []
    phi3 = []
    Orientation = {}
    lines = Orientation_File.readlines()[1:]
    for line in lines:
        phi1.append(float(line.split('  ')[0]))
        phi2.append(float(line.split('  ')[1]))
        phi3.append(float(line.split('  ')[2]))
    Orientation['phi1'] = phi1
    Orientation['phi2'] = phi2
    Orientation['phi3'] = phi3
    Orientation['Hash_Orientation'] = Key_Parsed["Hash_Orientation"]
    Orientation["Texture_Type"] = Key_Parsed["Texture_Type"]
    Meta['Orientation'] = Orientation
    Grain_Number = len(lines)
    Meta["Element_Number"] = Element_Number
    Meta["Grain_Number"] = Grain_Number
    x = round((Grain_Number ** (1/3)) * 0.095, 4)
    RVE_Size = (x, x, x)
    Meta['RVE_Size'] = RVE_Size
    Material_File = open('Material.inp')
    lines = Material_File.readlines()[1:]
    Material = {}
    try:
        for i, line in enumerate(lines):
            if "*User Material" in line and (i + 1) < len(lines):
                material_identifier = int(lines[i + 1].split(',')[0])
                break
        Material["Material_Identifier"] = material_identifier
        fortran_file_path = os.path.join(Key_Input_Path, 'mod_alloys.f')
        material_parameters = extract_material_parameters_from_fortran(fortran_file_path, material_identifier)
        Material["Material_Parameters"] = material_parameters
        Meta['Material'] = Material
    except:
        Material["Material_Number"] = "Unknown"
        Material["Material_Parameters"] = "Unknown"
        Meta['Material'] = Material
    Load_File = open('{}_remPart_file.inp'.format(Key))
    lines = Load_File.readlines()[1:]
    Load_Type = "Monotonic"  # Default to Monotonic
    Amplitude = "NA"
    for line in lines:
        if "*Amplitude" in line:
            Load_Type = "Cyclic"
            Amplitude = []  # Reset Amplitude to an empty list
            j = i + 1
            while not lines[j].startswith("**") and not lines[j].startswith("*"):
                values = lines[j].split(',')
                for value in values:
                    try:
                        integer_part = int(float(value.strip()))
                        Amplitude.append(integer_part)
                    except ValueError:
                        # Continue if there's any non-numeric value
                        continue
                j += 1
            break

    Meta["Load_Type"] = Load_Type
    Meta["Amplitude"] = Amplitude
    Meta["Stress_Type"] = Key_Parsed["Stress_Type"]
    Meta["Load_Descriptor"] = Key_Parsed["Load_Descriptor"]
    Meta["Hash_Load"] = Key_Parsed["Hash_Load"]
    Meta["Units"] = {"Stress": "MPa", "Strain": "None", "RVE_Size": "mm", "Orientation":"Radian"}
    os.chdir(Current_Path)
    return (Meta)
def Meta_Writer (key, json_file):
    Meta = Meta_reader(key)
    with open(json_file, 'w') as output_file:
        Current_Dict = DC.Read_Database_From_Json("Data_Base.json")
        print(Current_Dict)
        if key in Current_Dict.keys():
            print("The key is already found in JSON file")
            temp_dic = Current_Dict[key]
            for meta in Meta:
                temp_dic[meta] = Meta[meta]
            Current_Dict.update(temp_dic)
            json.dump(Current_Dict, output_file)
        else:
            print("The key was not found in JSON file")

def extract_material_parameters_from_fortran(file_path, target_material_number):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    extracting = False
    parameters = {}
    for line in lines:
        # Find material section
        if 'c +   Material library:' in line:
            material_number = int(line.split('#')[1].split('==>')[0])
            if material_number == target_material_number:
                extracting = True
            else:
                extracting = False
        # Extract parameters within the target material module
        if extracting and line.strip().startswith("real(8),parameter::"):
            parts = line.strip().split('=')
            param_name = parts[0].split()[-1].strip()
            param_value = parts[1].strip()
            parameters[param_name] = param_value
    return parameters