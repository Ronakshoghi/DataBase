# -*- coding: utf-8 -*-
"""
Author: Ronak Shoghi
Date: 18.04.22
Time: 02:27

"""
import os
import Database_Creator as DC
import json

def Results_Reader (Key):
    Results_Folders = []
    Source_Path = os.getcwd()
    os.chdir('..')
    Current_Path = os.getcwd()
    Results_Path = "{}/results".format(Current_Path)
    for root, dirs, files in os.walk(Results_Path , topdown=False):
        for name in dirs:
            Results_Folders.append(name)
    for result_folder in Results_Folders:
        if Key == result_folder:
            print ("Results Found!")
            os.chdir("{}/{}".format(Results_Path, result_folder))
            Results_Files_Name = []
            for root, dirs, files in os.walk(os.getcwd(), topdown=False):
                for name in files:
                    Results_Files_Name.append(name)
            Available_Results = {}
            for Result_File in Results_Files_Name:
                with open("{}/{}/{}".format(Results_Path, result_folder, Result_File)) as Temp_Result:
                    lines = Temp_Result.readlines()
                    Values = []
                    for line in lines:
                        Values.append(float(line.strip('\n')))
                    Available_Results[Result_File.strip(".out")] = Values
            os.chdir(Source_Path)
            return Available_Results
        else:
            print ("Results not Found!")
            os.chdir(Source_Path)
            return None


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
