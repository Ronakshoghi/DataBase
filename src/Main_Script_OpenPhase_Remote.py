# -*- coding: utf-8 -*-
"""
Author: Jan Schmidt
Date: 09.10.2023

"""
import sys

src_dir = "/Users/jan/ronak_db/DataBase"
sys.path.append(src_dir)
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
import glob
import time
import argparse


def main(project_name, texture_file, run_dir, path_db, bc_file, idx_bc_start, idx_bc_end, n_grains_per_dir=11,
         elements_per_grain=1, t_timeout=300):
    """

    :return:
    """
    # Settings
    cp_code = 'openphase'
    times_dict = {}
    os.chdir(run_dir)  # This will navigate to the texture subfolder in which the Key structure is created
    current_path = os.getcwd()
    overwrite_results = True

    # Define directories required here
    log_files_dir = os.path.join(path_db, "04_LogFiles/{}".format(project_name))
    if not os.path.exists(log_files_dir):
        os.mkdir(log_files_dir)
    else:
        print(f"{log_files_dir} exists already and will not be recreated.")
    results_dir = run_dir

    # Read required lines from load file
    bc_array = np.genfromtxt(bc_file, delimiter=",")
    loads_simu = [[1, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0],
                  [0.66666667, -0.33333333, -0.33333333, 0, 0, 0], [0, 0.86603, -0.86603, 0, 0, 0]]
    loads_simu = np.array(loads_simu)
    loads_simu = np.vstack((loads_simu, bc_array[idx_bc_start:idx_bc_end, :]))

    "Main Process"
    for counter, load in enumerate(loads_simu):
        results_dict = DH.read_database_from_json(os.path.join(current_path, "Data_Base.json"))
        key = KG.key_generator(load, n_grains_per_dir=n_grains_per_dir, elements_per_grain=elements_per_grain,
                               cp_code=cp_code, ori_file=texture_file)
        if key in results_dict.keys() and not overwrite_results:
            print("The key is already found in JSON file")
            print("Overwrite is False. I will go to next Load.")
            continue

        elif "{}.log".format(key) in glob.glob(os.path.join(log_files_dir)):
            print("For key {} a log file exists in {}. This can be caused by a parallel worker working on the same"
                  "data point or non-converged results".format(key, log_files_dir))
        else:
            if key in results_dict.keys():
                print("The key is already found in JSON file")
                print("Overwrite is True. I will overwrite the Dat_Base.json.")
            else:
                print("The key was not found in JSON file and no log file exists")
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
                start = time.time()
                CP.Abaqus_Runner(key, 8)
                end = time.time()
            elif cp_code == 'openphase':
                GG.openphase_input_generator(load=scaled_load, key=key, n_grains_per_dir=n_grains_per_dir,
                                             elements_per_grain=elements_per_grain, src_dir=src_dir)
                start = time.time()
                return_val = CP.openphase_runner(key, t_timeout=t_timeout, log_files_dir=log_files_dir)
                end = time.time()
                print("Runtime of simulation is: %f seconds" % (end - start))
                times_dict[key] = end - start
            else:
                raise ValueError("cp_code {code} not valid. Must be abaqus or openphase.".format(code=cp_code))
            try:
                max_strain = SRC.max_strain_finder(key, cp_code='openphase')
                print("Max Strain: {}".format(max_strain))
            except IndexError:
                # Need to change back to main directory here because exception raised in max_strain_finder
                os.chdir(current_path)
                print("Result file contains not enough lines to find max strain!")
                continue

            # TODO: I need a mechanism that increases stress if max strain is below a threshold
            # Insert Results to the Data Base
            new_dict_for_db = {key: {"Meta_Data": MR.meta_reader(key, cp_code=cp_code, ori_file=texture_file,
                                                                 ori_file_header=False),
                                     "Initial_Load": load.tolist(),
                                     "Scaling_Factor": scaling_factor,
                                     "Applied_Load": scaled_load.tolist(),
                                     "Max_Total_Strain": max_strain,
                                     "Results": RP.results_reader(key, cp_code=cp_code),
                                     "Time": end - start}}

            results_dict_current = DH.read_database_from_json(os.path.join(results_dir, "Data_Base.json"))
            combined_dict = dict(results_dict_current, **new_dict_for_db)
            DH.json_database_creator(combined_dict, os.path.join(results_dir, "Data_Base.json"))


if __name__ == "__main__":
    # Setup argparser arguments
    parser = argparse.ArgumentParser(description='define CPFFT simulation parameters')
    parser.add_argument('-name', '--project_name', help='Name of the Project', required=True)
    parser.add_argument('-tp', '--texture_path', help='texture dir in which keys-subdirs for each bc are created',
                        required=True)
    parser.add_argument('-tf', '--texture_file', help='path texture_file.json that contains orientations',
                        required=True)
    parser.add_argument('-bcp', '--boundary_condition_path', help='path sig.txt that contains boundary conditions',
                        required=True)
    parser.add_argument('-idx_s', '--idx_bc_start', help='line in sig.txt that contains first load case for texture',
                        required=True)
    parser.add_argument('-idx_e', '--idx_bc_end', help='line in sig.txt that contains last load case for texture',
                        required=True)
    parser.add_argument('-dbp', '--database_path', help='entry path to data base structure', required=True)
    parser.add_argument('-n_gpd', '--number_grains_per_dir', help='number of grains per direction in RVE',
                        required=True)
    parser.add_argument('-n_epg', '--number_elements_per_grain', help='number of elments per grain in RVE',
                        required=True)
    parser.add_argument('-t_to', '--t_timeout', help='timeout for subprocess running CPFFT simulation', required=True)
    args = vars(parser.parse_args())

    # Read insoft-coded argument parser
    texture_file = args['texture_file']
    run_dir = args['texture_path']
    path_db = args['database_path']
    bc_file = args['boundary_condition_path']
    idx_bc_start = int(args['idx_bc_start'])
    idx_bc_end = int(args['idx_bc_end'])
    n_grains_per_dir = int(args['number_grains_per_dir'])
    elements_per_grain = int(args['number_elements_per_grain'])
    t_timeout = float(args['t_timeout'])
    project_name = args['project_name']

    print("Starting Data Generation. t_timeout is {}".format(t_timeout))
    print("RVE Size: {}-{}-{} | {} element(s) per grain".format(n_grains_per_dir, n_grains_per_dir, n_grains_per_dir,
                                                                elements_per_grain))

    main(project_name, texture_file, run_dir, path_db, bc_file, idx_bc_start, idx_bc_end, n_grains_per_dir,
         elements_per_grain, t_timeout)
