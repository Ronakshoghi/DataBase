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
Results_Dict = DH.Read_Database_From_Json("Data_Base.json")
load_cases = "sigdata1.txt"
loads = np.genfromtxt(load_cases)
Source_Path = os.getcwd()
os.chdir('..')
Current_Path = os.getcwd()

"Main Process"

for counter, load in enumerate(loads):
    Key = KG.Key_Generator(load)
    if Key in Results_Dict.keys():
        print("The key is already found in JSON file")
        continue
    else:
        print("The key was not found in JSON file")
        KFC.Create_Sub_Folder(Key)
        scaling_factor = 8
        print ("initial load: {}".format(load))
        scaled_load = load * scaling_factor
        Max_Strain = 0
        itertation = 0
        Lower_Strain_Limit = 0.0001
        Upper_Strain_Limit = 100
        while (Upper_Strain_Limit < Max_Strain or Lower_Strain_Limit > Max_Strain ):
            itertation += 1
            print ("scaling factor {} -> applied load in iteration {}: {}".format(scaling_factor, itertation, scaled_load))
            LC.Load_File_Generator(scaled_load, Key)
            GG.Abaqus_Input_Generator(Key)
            AR.Abaqus_Runner(Key, 8)
            Max_Strain = SRC.Max_Strain_Finder(Key)
            print ("Max Strain: {}".format(Max_Strain))
            if Max_Strain < Lower_Strain_Limit:
                scaling_factor *= 1.05
                scaled_load = load * scaling_factor

            elif Max_Strain > Upper_Strain_Limit:
                scaling_factor *= 0.95
                scaled_load = load * scaling_factor

        #Insert Results to the Data Base
        Results_Dict[Key] = {"Meta_Data": MR.Meta_reader(Key),
                             "Initial_Load": load.tolist(),
                             "Scaling_Factor": scaling_factor,
                             "Applied_Load": scaled_load.tolist(),
                             "Max_Total_Strain": Max_Strain,
                             "Results": RP.Results_Reader(Key)}

    DH.Json_Database_Creator(Results_Dict, "Data_Base_Updated.json")
# "Meta_Data": MR.Meta_reader(Key),
"Post Processing"
# Keys = Data_Base.keys()
# Desired_Keys = KP.Key_Finder(Keys, [1, 1, 1, 0, 0, 0])
# Found_Keys_Name = KP.Found_Keys_Generator(Desired_Keys)
# for Key in Found_Keys_Name:
#     print (Data_Base[Key]["Applied_Load"])

