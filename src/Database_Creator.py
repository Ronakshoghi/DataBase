# -*- coding: utf-8 -*-
"""
Author: Ronak Shoghi
Date: 07.04.22
Time: 18:20

"""


import numpy as np
import Key_Parser as KP
import Key_Generator as KG
import json

"""
Thia function insert the loads from a file into database. 
"""
def Insert_Intital_Load(file):
    Main_Dict = {}
    loads = np.genfromtxt(file)
    for load in loads:
        Main_Dict[KG.Key_Generator(load)] = {"Applied_Load": load}

    return Main_Dict

def Read_Database_From_Json(json_file):
    with open(json_file, 'r') as input_file:
        return json.load(input_file)

def Json_Database_Creator(dict, json_file):
    with open (json_file, 'w') as output_file:
        temp_dic = {}
        Current_Dict = Read_Database_From_Json("Data_Base.json")
        for key in dict:
            if key in Current_Dict.keys():
                print ("The key is already found in JSON file")
                continue
            else:
                print ("The key was not found in JSON file")
                temp_dic[key] = {"Applied_Load": dict[key]["Applied_Load"].tolist()}
        Current_Dict.update(temp_dic)
        json.dump(Current_Dict, output_file)