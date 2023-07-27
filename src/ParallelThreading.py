# -*- coding: utf-8 -*-
"""
Author: Ronak Shoghi
Date: 12.07.22
Time: 12:02

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
import CP_Runner as AR
import Strain_Result_Check as SRC
import os
import multiprocessing
from multiprocessing import Pool

def Main(sig):
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    Results_Dict = DH.read_database_from_json("Data_Base.json")
    load_cases = sig
    loads = np.genfromtxt(load_cases)
    Source_Path = os.getcwd()
    os.chdir('..')
    Current_Path = os.getcwd()
    for counter, load in enumerate(loads):
        Key = KG.key_generator(load)
        if Key in Results_Dict.keys():
            continue
        else:
            KFC.create_sub_folder(Key)
            scaling_factor = 90
            scaled_load = load * scaling_factor
            LC.load_file_generator(scaled_load, Key)
            GG.abaqus_input_generator(Key)
            AR.Abaqus_Runner(Key, 4)
            Max_Strain = SRC.max_strain_finder(Key, 'abaqus')
            # Insert Results to the Data Base
            Results_Dict[Key] = {"Meta_Data": MR.meta_reader(Key),
                                 "Initial_Load": load.tolist(),
                                 "Scaling_Factor": scaling_factor,
                                 "Applied_Load": scaled_load.tolist(),
                                 "Max_Strain": Max_Strain,
                                 "Results": RP.results_reader(Key, 'abaqus')}

        DH.json_database_creator(Results_Dict, "Data_Base_Updated.json")


if __name__ == '__main__':
    with Pool(5) as p:
        print(p.map(Main, ["sig1.txt", "sig2.txt", "sig3.txt3"]))


