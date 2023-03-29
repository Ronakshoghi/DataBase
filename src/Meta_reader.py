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
    uname = platform.uname()
    Meta = {
         'Owner':getpass.getuser(),
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
    Meta['Inputs-Path'] = Key_Input_Path
    Meta['Results-Path'] = Key_Results_Path
    os.chdir(Key_Input_Path)
    Input_File=open('{}_Abaqus_Input_File.inp'.format(Key))
    lines = Input_File.readlines()
    Abaqus_Version = (lines[2].split(':'))[1]
    Meta['Abaqus-Version'] = Abaqus_Version
    Orientation_File = open('Orientation.txt')
    phi1 = []
    phi2 = []
    phi3 = []
    Orientation = {}
    lines = Orientation_File.readlines()[1:]
    x = int(len(lines)/9)
    for line in lines:
        phi1.append(float(line.split('  ')[0]))
        phi2.append(float(line.split('  ')[1]))
        phi3.append(float(line.split('  ')[2]))
    Orientation['phi1'] = phi1
    Orientation['phi2'] = phi2
    Orientation['phi3'] = phi3
    Meta['Orientation'] = Orientation
    RVE_Size = "{}*{}*{}".format(x, x, x)
    Meta['RVE_Size'] = RVE_Size
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

