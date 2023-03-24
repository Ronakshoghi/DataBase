# -*- coding: utf-8 -*-
"""
Author: Ronak Shoghi
Date: 18.04.22
Time: 02:27

"""
import os
import Database_Handler as DH
import json
import numpy as np
import Key_Generator as KG
import Strain_Result_Check as SRC
import Meta_reader as MR
"""
Thia function read all the output files in the result folder and write them in the database. 
"""

def Results_Reader (Key):
    Current_Path = os.getcwd()
    Keys_Path ="{}/Keys".format(Current_Path)
    os.chdir(Keys_Path)
    Key_path = os.path.abspath(Key)
    Results_Path = "{}/results".format(Key_path)
    os.chdir(Results_Path)
    Results_Files_Name = []
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
        for name in files:
            Results_Files_Name.append(name)
    Available_Results = {}
    for Result_File in Results_Files_Name:
        with open("{}/{}".format(Results_Path, Result_File)) as Temp_Result:
            lines = Temp_Result.readlines()
            Values = []
            for line in lines:
                Values.append(float(line.strip('\n')))
            Available_Results[Result_File.strip(".out")] = Values
    os.chdir(Current_Path)
    return Available_Results

def Results_Writer (key, json_file):
    Results = Results_Reader(key)
    with open(json_file, 'w') as output_file:
        Current_Dict = DC.Read_Database_From_Json("Data_Base.json")
        if key in Current_Dict.keys():
            print("The key is already found in JSON file")
            temp_dic = Current_Dict[key]
            for result in Results:
                temp_dic[result] = Results[result]
            Current_Dict.update(temp_dic)
            json.dump(Current_Dict, output_file)

        else:
            print("The key was not found in JSON file")


# "Pre-Processing"
#
# abspath = os.path.abspath(__file__)
# dname = os.path.dirname(abspath)
# os.chdir(dname)
# Results_Dict = DH.Read_Database_From_Json("Data_Base.json")
# load_cases = "sigdata1.txt"
# loads = np.genfromtxt(load_cases)
# Source_Path = os.getcwd()
# os.chdir('..')
# Current_Path = os.getcwd()
#
# "Main Process"
#
# for counter, load in enumerate(loads):
#     print (counter)
#     Key = KG.Key_Generator(load)
#     if Key in Results_Dict.keys():
#         print("The key is already found in JSON file")
#         continue
#     else:
#         print("The key was not found in JSON file")
#         scaling_factor = 80
#         scaled_load = load * scaling_factor
#         Max_Strain = SRC.Max_Strain_Finder(Key)
#         #Insert Results to the Data Base
#         Results_Dict[Key] = {"Meta_Data": MR.Meta_reader(Key),
#                              "Initial_Load": load.tolist(),
#                              "Scaling_Factor": scaling_factor,
#                              "Applied_Load": scaled_load.tolist(),
#                              "Max_Strain": Max_Strain,
#                              "Results": Results_Reader(Key)}
#
#     DH.Json_Database_Creator(Results_Dict, "Data_Base_Updated.json")