# -*- coding: utf-8 -*-
"""
Author: Jan Schmidt
Date: 09.10.2023

"""
import numpy as np
from src import Key_Parser as KP
from src import Key_Generator as KG
from src import Database_Handler as DH
from src import Result_Parser as RP
from src import Meta_reader as MR
from src import Load_Creator as LC
from src import Key_Folder_Creator as KFC
from src import Geom_Generator as GG
from src import CP_Runner as CP
from src import Strain_Result_Check as SRC
import os
import sys
import glob
import time


def main(n_grains_per_dir, elements_per_grain):
    """

    :return:
    """

    "Preprocessing"
    cp_code = 'openphase'
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    # Define the directory structure
    project_dir = "/Users/jan/ronak_db/DataBase"
    src_dir = os.path.join(project_dir, "src")
    texture_dir = "/Users/jan/Documents/Promotion/04_GeorgiaTech/06_DataBase/01_TextureFiles"
    results_dir = "/Users/jan/Documents/Promotion/04_GeorgiaTech/06_DataBase/02_ResultsCPFFT" # contains the json db
    bc_dir = "/Users/jan/Documents/Promotion/04_GeorgiaTech/06_DataBase/03_BoundaryConditions"

    results_dict = DH.read_database_from_json(os.path.join(results_dir, "Data_Base.json"))
    times_dict = {}
    texture_files_list = glob.glob(os.path.join(texture_dir, "*"))  # takes all textures in the texture directory
    load_cases = os.path.join(bc_dir, "sig_abqopp.txt")
    loads = np.genfromtxt(load_cases)

    #os.chdir('..')
    current_path = os.getcwd() #This will be cluster/scratch


    # TODO: In the current version this code assumes that this main script is executed within the src directory on the
    #  computing node. I think the logic should be go to /scratch on the computing node, have the texture and sig files in a
    #  project/texture_dependent_yc/data_base directory. The main script should be executed on scratch and access the code in the
    #  src directory. For that the chdirs here need to be adapted. Create an absolute path to the project dir and extend it with
    #  src, data_base,... On scratch the keys directory will be created. Lockfiles need to be written  to  the project directory.
    #  Results after converged  simulation as well

    # TODO: Write a loop that iterates of all texturefiles presented in the directory

    # Initialize n_grains_per direction and elements_per grain from main input arguments
    # n_grains_per_dir = n
    # elements_per_grain = sys.argv[-1]


    "Main Process"
    for idx_texture, texture_file in enumerate(texture_files_list):
        for counter, load in enumerate(loads):
            key = KG.key_generator(load, n_grains_per_dir=n_grains_per_dir, elements_per_grain=elements_per_grain,
                                   cp_code=cp_code, ori_file=texture_file)
            if key in results_dict.keys():
                print("The key is already found in JSON file")
                continue
            else:
                print("The key was not found in JSON file")
                # For this key, a new folder is created that contains the subfolder inputs and results
                KFC.create_sub_folder(key, cp_code=cp_code, ori_file=texture_file)
                scaling_factor = 58.6e6  # 50e6 In OpenPhase we can scale here directly to J2 equiv. stress in Pa!
                print("initial load: {}".format(load))
                scaled_load = load * scaling_factor
                max_strain = 0
                itertation = 0

                itertation += 1
                print("scaling factor {} -> applied load in iteration {}: {}".format(scaling_factor, itertation,
                                                                                     scaled_load))
                if cp_code == 'abaqus':
                    LC.load_file_generator(scaled_load, key)
                    GG.abaqus_input_generator(key)
                    CP.Abaqus_Runner(key, 8)
                elif cp_code == 'openphase':
                    GG.openphase_input_generator(load=scaled_load, key=key, n_grains_per_dir=n_grains_per_dir,
                                                 elements_per_grain=elements_per_grain)
                    start = time.time()
                    return_val = CP.openphase_runner(key, t_timeout=300)
                    end = time.time()
                    print("Runtime of simulation is: %f seconds" % (end - start))
                    times_dict[key] = end - start

                try:
                    max_strain = SRC.max_strain_finder(key, cp_code='openphase')
                    print("Max Strain: {}".format(max_strain))
                except IndexError:
                    # Need to change back to main directory here because exception raised in max_strain_finder
                    os.chdir(current_path)
                    print("Result file contains not enough lines to find max strain!")
                    continue

                # Insert Results to the Data Base
                results_dict[key] = {"Meta_Data": MR.meta_reader(key, cp_code=cp_code, ori_file=texture_file,
                                                                 ori_file_header=False),
                                     "Initial_Load": load.tolist(),
                                     "Scaling_Factor": scaling_factor,
                                     "Applied_Load": scaled_load.tolist(),
                                     "Max_Total_Strain": max_strain,
                                     "Results": RP.results_reader(key, cp_code=cp_code)}

            DH.json_database_creator(results_dict, "Data_Base_Updated.json")
        # "Meta_Data": MR.meta_reader(key),
        "Post Processing"
        # Keys = Data_Base.keys()
        # Desired_Keys = KP.Key_Finder(Keys, [1, 1, 1, 0, 0, 0])
        # Found_Keys_Name = KP.Found_Keys_Generator(Desired_Keys)
        # for key in Found_Keys_Name:
        #     print (Data_Base[key]["Applied_Load"])


if __name__ == "__main__":
    n_grains_dir = sys.argv[-2] #number of grains per direction
    epg = sys.argv[-1] #number of elements per grain (1,8,27,...)
    main(n_grains_dir, epg)
