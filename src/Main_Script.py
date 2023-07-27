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
import CP_Runner as CP
import Strain_Result_Check as SRC
import os




"Pre-Processing"
cp_code = 'openphase'
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
results_dict = DH.read_database_from_json("Data_Base.json")
load_cases = "sigdata1.txt"
ori_file = "orientations_random_1331.csv"
loads = np.genfromtxt(load_cases)
source_path = os.getcwd()
os.chdir('..')
current_path = os.getcwd()

# TODO: What's the smartest way to specify geometry conditions (n_grains, elemnts_per_grain)? Could be done here and
#  then given to the functions that modify the temp files in the while loop.

n_grains_per_dir = 11
elements_per_grain = 8

"Main Process"

for counter, load in enumerate(loads):
    key = KG.key_generator(load, n_grains_per_dir=n_grains_per_dir, elements_per_grain=elements_per_grain,
                           cp_code=cp_code)
    if key in results_dict.keys():
        print("The key is already found in JSON file")
        continue
    else:
        print("The key was not found in JSON file")
        # For this key, a new folder is created that contains the subfolder inputs and results
        KFC.create_sub_folder(key, cp_code=cp_code)
        scaling_factor = 50e6 # In OpenPhase we can scale here directly to J2 equiv. stress in Pa!
        print ("initial load: {}".format(load))
        scaled_load = load * scaling_factor
        max_strain = 0
        itertation = 0
        lower_strain_limit = 0.0001
        upper_strain_limit = 100
        while (upper_strain_limit < max_strain or lower_strain_limit > max_strain):
            itertation += 1
            print ("scaling factor {} -> applied load in iteration {}: {}".format(scaling_factor, itertation,
                                                                                  scaled_load))
            if cp_code == 'abaqus':
                LC.load_file_generator(scaled_load, key)
                GG.abaqus_input_generator(key)
                CP.Abaqus_Runner(key, 8)
            elif cp_code == 'openphase':
                #TODO: I dont need the loop. If looping, only ProjectInput.opi needs to be recreated, not the cpp file.
                GG.openphase_input_generator(load=load, key=key, n_grains_per_dir=n_grains_per_dir,
                                             elements_per_grain=elements_per_grain)
                CP.openphase_runner(key)

            max_strain = SRC.max_strain_finder(key, cp_code='openphase')
            print ("Max Strain: {}".format(max_strain))
            if max_strain < lower_strain_limit:
                scaling_factor *= 1.05
                scaled_load = load * scaling_factor

            elif max_strain > upper_strain_limit:
                scaling_factor *= 0.95
                scaled_load = load * scaling_factor

        #Insert Results to the Data Base
        results_dict[key] = {"Meta_Data": MR.meta_reader(key),
                             "Initial_Load": load.tolist(),
                             "Scaling_Factor": scaling_factor,
                             "Applied_Load": scaled_load.tolist(),
                             "Max_Total_Strain": max_strain,
                             "Results": RP.results_reader(key, 'abaqus')}

    DH.json_database_creator(results_dict, "Data_Base_Updated.json")
# "Meta_Data": MR.meta_reader(key),
"Post Processing"
# Keys = Data_Base.keys()
# Desired_Keys = KP.Key_Finder(Keys, [1, 1, 1, 0, 0, 0])
# Found_Keys_Name = KP.Found_Keys_Generator(Desired_Keys)
# for key in Found_Keys_Name:
#     print (Data_Base[key]["Applied_Load"])

