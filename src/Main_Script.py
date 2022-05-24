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
import Abaqus_Runner as AR
import Strain_Result_Check as SRC
import os
import json




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

"Main Process"

for i, load in enumerate(loads):
    Key = KG.Key_Generator(load)
    KFC.Create_Sub_Folder(Key)
    scaling_factor = 40
    print ("initial load: {}".format(load))
    scaled_load = load * scaling_factor
    Max_Strain = 0
    itertation = 0
    Lower_Strain_Limit = 0.027
    Upper_Strain_Limit = 0.033
    while (Upper_Strain_Limit < Max_Strain or Lower_Strain_Limit > Max_Strain ):
        itertation += 1
        print ("scaling factor {} applied load in iteration {}: {}".format(scaling_factor, itertation, scaled_load))
        LC.Load_File_Generator(scaled_load, Key)
        GG.Abaqus_Input_Generator(Key)
        AR.Abaqus_Runner(Key, 4)
        Max_Strain = SRC.Max_Strain_Finder(Key)
        print ("Max Strain {}".format(Max_Strain))
        if Max_Strain < Lower_Strain_Limit:
            scaling_factor *= 1.05
            scaled_load = load * scaling_factor

        elif Max_Strain > Upper_Strain_Limit:
            scaling_factor *= 0.95
            scaled_load = load * scaling_factor

    break


"Post Processing"
#load_cases = 'sigdata1.txt'
#Data_Base = DC.Insert_Intital_Load(load_cases)
#DC.Json_Database_Creator(Data_Base, "Data_Base_Updated.json")

#MR.Meta_Writer(KG.Key_Generator([-7.626425197906852, 20.504493245472673, -36.88058941350355, 0.0, 0.0, 0.0]), "Data_Base_Updated.json")
#RP.Results_Writer(KG.Key_Generator([-7.626425197906852, 20.504493245472673, -36.88058941350355, 0.0, 0.0, 0.0]), "Data_Base_Updated.json")

# Keys = Data_Base.keys()
# Desired_Keys = KP.Key_Finder(Keys, [1, 1, 1, 0, 0, 0])
# Found_Keys_Name = KP.Found_Keys_Generator(Desired_Keys)
#
# for Key in Found_Keys_Name:
#     print (Data_Base[Key]["Applied_Load"])
