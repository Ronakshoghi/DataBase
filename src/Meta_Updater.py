# -*- coding: utf-8 -*-
"""
Author: Ronak Shoghi
Date: 17.01.24
Time: 10:07

"""
"Pre-Processing"
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
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
Results_Dict = DH.Read_Database_From_Json("Data_Base.json")
Source_Path = os.getcwd()
os.chdir('..')
Current_Path = os.getcwd()

"Main Process"
keys_folder_path = os.path.join(Current_Path, 'Keys')
Keys = os.listdir(keys_folder_path)
for Key in Keys:
    print(Key)
    Results_Dict[Key] = {"Meta_Data": {
                            **MR.Meta_reader(Key),
                            "Scaling_Factor": 80,
                             # "Initial_Load": load.tolist(),
                             # "Applied_Load": scaled_load.tolist(),
                                },
                             "Results": RP.Results_Reader(Key)}

    DH.Json_Database_Creator(Results_Dict, "Data_Base_Updated.json")
