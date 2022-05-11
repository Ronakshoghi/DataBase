# -*- coding: utf-8 -*-
"""
Author: Ronak Shoghi
Date: 07.04.22
Time: 18:17

"""
import numpy as np
import Key_Parser as KP
import Key_Generator as KG
import Database_Creator as DC
import Result_Parser as RP
import Meta_reader as MR

#load_cases = 'sigdata1.txt'
#Data_Base = DC.Insert_Intital_Load(load_cases)
#DC.Json_Database_Creator(Data_Base, "Data_Base_Updated.json")
MR.Meta_Reader(KG.Key_Generator([-7.626425197906852, 20.504493245472673, -36.88058941350355, 0.0, 0.0, 0.0]))
#RP.Results_Writer(KG.Key_Generator([-7.626425197906852, 20.504493245472673, -36.88058941350355, 0.0, 0.0, 0.0]), "Data_Base_Updated.json")

# Keys = Data_Base.keys()
# Desired_Keys = KP.Key_Finder(Keys, [1, 1, 1, 0, 0, 0])
# Found_Keys_Name = KP.Found_Keys_Generator(Desired_Keys)
#
# for Key in Found_Keys_Name:
#     print (Data_Base[Key]["Applied_Load"])
