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
from src import Database_Handler as DC
import json

"""
This function reads Meta data in inout folder for each key and writes them in the JSON database
"""


# TODO: What kind of information do we want to include in the database? MS Descriptors, Barlat Coefficients, MTEX version

def meta_reader(key, cp_code='abaqus', ori_file='Orientation.txt', ori_file_header=True):
    uname = platform.uname()
    meta_dict = {
        'Owner': getpass.getuser(),
        'Date': date.today().strftime("%d %B %Y"),
        'System': uname.system,
        'Ip-Address': socket.gethostbyname(socket.gethostname()),
        'Mac-Address': ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    }
    current_path = os.getcwd()
    keys_path = "{}/Keys".format(current_path)
    os.chdir(keys_path)
    key_path = os.path.abspath(key)
    if cp_code == 'abaqus':
        key_input_path = "{}/inputs".format(key_path)
        key_results_path = "{}/results".format(key_path)
    elif cp_code == 'openphase':
        key_input_path = key_path
        key_results_path = "{}/results".format(key_path)
    else:
        raise ValueError("cp_code {code} not valid. Must be abaqus or openphase.".format(code=cp_code))

    meta_dict['Inputs-Path'] = key_input_path
    meta_dict['Results-Path'] = key_results_path
    os.chdir(key_input_path)
    if cp_code == 'abaqus':
        input_file = open('{}_Abaqus_Input_File.inp'.format(key))
        lines = input_file.readlines()
        abaqus_version = (lines[2].split(':'))[1]
        meta_dict['CP_Code-Version'] = abaqus_version
    elif cp_code == 'openphase':
        with open('{}.opi'.format(key), 'r') as f:
            lines = f.readlines()
            openphase_version = lines[1].split(': ')[-1]
            meta_dict['CP_Code-Version'] = openphase_version
    else:
        raise ValueError("cp_code {code} not valid. Must be abaqus or openphase.".format(code=cp_code))

    orientation_file = open(ori_file)
    phi1 = []
    phi2 = []
    phi3 = []
    orientation = {}
    if ori_file_header:
        lines = orientation_file.readlines()[1:]
    else:
        lines = orientation_file.readlines()
    if cp_code == 'abaqus':
        x = int(len(lines) / 9)  # Why by nine?
        sep = '  '
    elif cp_code == 'openphase':
        x = int(len(lines) ** (1 / 3))
        sep = ','
    else:
        raise ValueError("cp_code {code} not valid. Must be abaqus or openphase.".format(code=cp_code))

    for line in lines:
        phi1.append(float(line.split(sep)[0]))
        phi2.append(float(line.split(sep)[1]))
        phi3.append(float(line.split(sep)[2]))
    orientation['phi1'] = phi1
    orientation['phi2'] = phi2
    orientation['phi3'] = phi3
    meta_dict['Orientation'] = orientation
    RVE_Size = "{}*{}*{}".format(x, x, x)
    meta_dict['RVE_Size'] = RVE_Size
    os.chdir(current_path)
    return meta_dict


def meta_writer(key, json_file):
    meta_dict = meta_reader(key)
    with open(json_file, 'w') as output_file:
        current_dict = DC.read_database_from_json("Data_Base.json")
        print(current_dict)
        if key in current_dict.keys():
            print("The key is already found in JSON file")
            temp_dic = current_dict[key]
            for meta in meta_dict:
                temp_dic[meta] = meta_dict[meta]
            current_dict.update(temp_dic)
            json.dump(current_dict, output_file)
        else:
            print("The key was not found in JSON file")
