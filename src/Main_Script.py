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
import Load_Creator as LC
import Key_Folder_Creator as KFC
import Geom_Generator as GG
import os
import json

#load_cases = 'sigdata1.txt'
#Data_Base = DC.Insert_Intital_Load(load_cases)
#DC.Json_Database_Creator(Data_Base, "Data_Base_Updated.json")

#MR.Meta_Writer(KG.Key_Generator([-7.626425197906852, 20.504493245472673, -36.88058941350355, 0.0, 0.0, 0.0]), "Data_Base_Updated.json")

"Pre-Processing"

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
print (os.getcwd())
load_cases = "sigdata1.txt"
loads = np.genfromtxt(load_cases)
Source_Path = os.getcwd()
os.chdir('..')
Current_Path = os.getcwd()

for i, load in enumerate(loads):
    Key = KG.Key_Generator(load)
    KFC.Create_Sub_Folder(Key)
    LC.Load_File_Generator(load, Key)
    GG.Abaqus_Input_Generator(Key)
    if i == 10:
        break

"Main Process"


"Post Processing"
#RP.Results_Writer(KG.Key_Generator([-7.626425197906852, 20.504493245472673, -36.88058941350355, 0.0, 0.0, 0.0]), "Data_Base_Updated.json")

# Keys = Data_Base.keys()
# Desired_Keys = KP.Key_Finder(Keys, [1, 1, 1, 0, 0, 0])
# Found_Keys_Name = KP.Found_Keys_Generator(Desired_Keys)
#
# for Key in Found_Keys_Name:
#     print (Data_Base[Key]["Applied_Load"])
