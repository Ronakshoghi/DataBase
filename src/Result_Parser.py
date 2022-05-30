# -*- coding: utf-8 -*-
"""
Author: Ronak Shoghi
Date: 18.04.22
Time: 02:27

"""
import os
import Database_Handler as DC
import json

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

