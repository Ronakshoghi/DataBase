# -*- coding: utf-8 -*-
"""
Author: Ronak Shoghi
Date: 06.05.22
Time: 13:46


This function reads the system related meta data
"""


import psutil
import platform
from datetime import datetime
import socket
import uuid
import re
import getpass
from datetime import date
import glob, os
import Key_Generator as KG
import Database_Creator as DC
import json
from pathlib import Path
import string
"""
This function reads Meta data in inout folder for each key and writes them in the JSON database
    """
def Meta_reader(Key):
    uname = platform.uname()
    Meta ={
         'Owner':getpass.getuser(),
         'Date': date.today().strftime("%d %B %Y"),
         'System': uname.system,
         'Ip-Address': socket.gethostbyname(socket.gethostname()),
         'Mac-Address': ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        }
    Inputs_Folders = []
    Keys_Path = []
    Source_Path = os.getcwd()
    os.chdir('..')
    Current_Path = os.getcwd()
    Inputs_Path = "{}/inputs".format(Current_Path)
    for root, dirs, files in os.walk(Inputs_Path, topdown=False):
        Keys_Path = os.path.join(Inputs_Path, Key)
        Meta['Input-Paths'] = Keys_Path
        for name in dirs:
            Inputs_Folders.append(name)
    print(Inputs_Folders)
    for Input_Folder in Inputs_Folders:
        if Key == Input_Folder:
            print("Results Found!")
            os.chdir("{}/{}".format(Inputs_Path, Input_Folder))
            Inputs_Files_Name = []
            Desired_Inputs_Files_Name = []
            lines = []
            for root, dirs, files in os.walk(os.getcwd(), topdown=False):
                for name in files:
                    Inputs_Files_Name.append(name)
                    if name.endswith(".inp"):
                        Desired_Inputs_Files_Name.append(name)
    for desired_Input_file in Desired_Inputs_Files_Name:
        if desired_Input_file == 'geometry_Periodic.inp':
            f=open('geometry_Periodic.inp')
            lines = f.readlines()
            Abaqus_Version = (lines[2].split(':'))[1]
            Meta['Abaqus-Version'] = Abaqus_Version
    Meta['Abaqus-input'] = Desired_Inputs_Files_Name
    os.chdir(Source_Path)
    print(Meta)
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

