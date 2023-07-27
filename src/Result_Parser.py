# -*- coding: utf-8 -*-
"""
Author: Ronak Shoghi
Date: 18.04.22
Time: 02:27

"""
import os
import warnings

from src import Database_Handler as DH
import json
import numpy as np
from src import Key_Generator as KG
from src import Strain_Result_Check as SRC
from src import Meta_reader as MR
"""
Thia function read all the output files in the result folder and write them in the database. 
"""

def results_reader (key, cp_code='abaqus'):
    current_path = os.getcwd()
    keys_path ="{}/Keys".format(current_path)
    os.chdir(keys_path)
    key_path = os.path.abspath(key)
    results_path = "{}/results".format(key_path)
    os.chdir(results_path)
    results_files_name = []
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
        for name in files:
            results_files_name.append(name)
    available_results = {}

    for result_file in results_files_name:
        if cp_code == 'abaqus':
            with open("{}/{}".format(results_path, result_file)) as Temp_Result:
                lines = Temp_Result.readlines()
                values = []
                for line in lines:
                    values.append(float(line.strip('\n')))
                available_results[result_file.strip(".out")] = values
        elif cp_code == 'openphase':
            if len(results_files_name) > 1:
                warnings.warn("WARNING: More then one OpenPhase results.txt found in folder!\n Might be not wanted!")
            openphase_out = np.genfromtxt(result_file, delimiter=';', skip_header=1)
            stresses_cauchy = openphase_out[:, 0:6] * 1e-6 # convert to MPa
            stresses_vm = openphase_out[:, -1] * 1e-6 # convert to MPa

            strains_green = openphase_out[:, 6:12]
            strains_pl = openphase_out[:, 12:18]
            strains_vm = openphase_out[:, -2]


            # FLIP TO VOIGT
            stresses_cauchy[:, [3, 4]] = stresses_cauchy[:, [4, 3]]
            stresses_cauchy[:, [4, 5]] = stresses_cauchy[:, [5, 4]]
            strains_green[:, [3, 4]] = strains_green[:, [4, 3]]
            strains_green[:, [4, 5]] = strains_green[:, [5, 4]]
            strains_pl[:, [3, 4]] = strains_pl[:, [4, 3]]
            strains_pl[:, [4, 5]] = strains_pl[:, [5, 4]]


            # Assign arrays to available results dict
            keys_stress = ['S11', 'S22', 'S33', 'S32', 'S13', 'S12']
            keys_strain = ['E11', 'E22', 'E33', 'E32', 'E13', 'E12']
            keys_strain_pl = ['Ep11', 'Ep22', 'Ep33', 'Ep32', 'Ep13', 'Ep12']

            for idx_component, key_stress in enumerate(keys_stress):
                available_results[key_stress] = stresses_cauchy[:, idx_component].tolist()
            for idx_component, key_strain in enumerate(keys_strain):
                available_results[key_strain] = strains_green[:, idx_component].tolist()
            for idx_component, key_strain_pl in enumerate(keys_strain_pl):
                available_results[key_strain_pl] = strains_pl[:, idx_component].tolist()

            available_results['S'] = stresses_vm.tolist()
            available_results['E'] = strains_vm.tolist()



        else:
            raise ValueError("cp_code {code} not valid. Must be abaqus or openphase.".format(code=cp_code))

    os.chdir(current_path)
    return available_results

#TODO: When is the writer used? In Main_Script.py, only the reader is used to create the results dict
def results_writer (key, json_file):
    results = results_reader(key, 'abaqus')
    with open(json_file, 'w') as output_file:
        current_dict = DH.read_database_from_json("Data_Base.json")
        if key in current_dict.keys():
            print("The key is already found in JSON file")
            temp_dic = current_dict[key]
            for result in results:
                temp_dic[result] = results[result]
            current_dict.update(temp_dic)
            json.dump(current_dict, output_file)

        else:
            print("The key was not found in JSON file")


# "Pre-Processing"
#
# abspath = os.path.abspath(__file__)
# dname = os.path.dirname(abspath)
# os.chdir(dname)
# results_dict = DH.Read_Database_From_Json("Data_Base.json")
# load_cases = "sigdata1.txt"
# loads = np.genfromtxt(load_cases)
# source_path = os.getcwd()
# os.chdir('..')
# current_path = os.getcwd()
#
# "Main Process"
#
# for counter, load in enumerate(loads):
#     print (counter)
#     key = KG.key_generator(load)
#     if key in results_dict.keys():
#         print("The key is already found in JSON file")
#         continue
#     else:
#         print("The key was not found in JSON file")
#         scaling_factor = 80
#         scaled_load = load * scaling_factor
#         Max_Strain = SRC.max_strain_finder(key)
#         #Insert Results to the Data Base
#         results_dict[key] = {"Meta_Data": MR.meta_reader(key),
#                              "Initial_Load": load.tolist(),
#                              "Scaling_Factor": scaling_factor,
#                              "Applied_Load": scaled_load.tolist(),
#                              "Max_Strain": Max_Strain,
#                              "Results": results_reader(key)}
#
#     DH.json_database_creator(results_dict, "Data_Base_Updated.json")