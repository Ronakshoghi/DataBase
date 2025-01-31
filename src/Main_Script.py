# -*- coding: utf-8 -*-
"""
Author: Ronak Shoghi
Date: 07.04.22
Time: 18:17

"""
import numpy as np
import Key_Parser as KP
import Key_Generator as KG
import Database_Handler as DH
import Result_Parser as RP
import Meta_reader as MR
import Load_Creator as LC
import Key_Folder_Creator as KFC
import Geom_Generator as GG
import Abaqus_Runner as AR
import Strain_Result_Check as SRC
import os


"Pre-Processing"

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
os.chdir('..')
Current_Path = os.getcwd()
Source_Path = os.getcwd()
Abaqus_Temp_Files_Path = "{}/Abaqus_Temp_Files".format(Current_Path)
Abaqus_Constant_Files_Path = "{}/Abaqus_Constant_Files".format(Current_Path)
Results_Dict = DH.Read_Database_From_Json("Data_Base.json")
os.chdir(Abaqus_Temp_Files_Path)
load_cases = "sigdata1.txt"
loads = np.genfromtxt(load_cases)
os.chdir(Current_Path)

"Main Process"

for counter, load in enumerate(loads):
    Key = KG.Key_Generator(load)
    if Key in Results_Dict.keys():
        print("The key is already found in JSON file")
        continue
    else:
        print("The key was not found in JSON file")
        KFC.Create_Sub_Folder(Key)
        scaling_factor = 60
        print ("initial load: {}".format(load))
        scaled_load = load * scaling_factor
        LC.Load_File_Generator(scaled_load, Key)
        GG.Abaqus_Input_Generator(Key)
        AR.Abaqus_Runner(Key, 2)
        Results_Dict[Key] = {**MR.Meta_reader(Key), **RP.Results_Reader(Key)}
    DH.Json_Database_Creator(Results_Dict, "Data_Base_Updated.json")


