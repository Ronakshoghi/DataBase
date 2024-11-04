# -*- coding: utf-8 -*-
"""
Author: Jan Schmidt
Date: 09.10.2023

"""
import sys

src_dir = "/storage/home/hcoda1/7/jschmidt87/software/DataBase/"
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
from src import PostProcessingTools
import os
import glob
import time
import argparse
import json


def main(project_name, texture_file, run_dir, path_db, setup, inp_file='ProjectInput.opi', n_grains_per_dir=11,
         elements_per_grain=1, t_timeout=300):
    """

    :param inp_file:
    :return:
    """
    # Settings
    cp_code = 'openphase'
    times_dict = {}
    os.chdir(run_dir)  # This will navigate to the texture subfolder in which the Key structure is created
    current_path = os.getcwd()
    overwrite_results = False

    # Hyperparameters for behavior on non-converged simulation
    steps_required = 101  # number of result steps in load file if converged
    scale_up = 1.05  # scale load up in steps_converged = steps_required
    scale_down = 0.95  # scale down if steps_conveged < steps_required but max_strain > threshold_retry
    threshold_retry = 0.0018

    # Define directories required here
    log_files_dir = os.path.join(path_db, "LogFiles")  # os.path.join(path_db, "04_LogFiles/{}".format(project_name))
    if not os.path.exists(log_files_dir):
        os.mkdir(log_files_dir)
    else:
        print(f"{log_files_dir} exists already and will not be recreated.")
    results_dir = run_dir

    # Read setup that contains loads
    setup_file = os.path.join(current_path, f'{setup}.json')
    with open(setup_file, 'r') as f:
        setup_dict = json.load(f)
        bc_dict = setup_dict['bc_dict']
    bc_array = np.array(list(bc_dict.values()))
    if len(bc_array.shape) == 1:
        loads_simu = bc_array.reshape((1, len(bc_array)))
        print('+++Warning: only one load case in loadfile!+++')
    else:
        loads_simu = bc_array

    "Main Process"
    for counter, load in enumerate(loads_simu):
        # Create Data_Base.json if not exists
        if not os.path.exists(os.path.join(current_path, "Data_Base.json")):
            print(f"No Data_Base.json for {current_path}. I create an empty one.")
            json.dump({}, open(os.path.join(current_path, "Data_Base.json"), 'w'))
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
            reached_yielding = False
            scaled_down = False
            while not reached_yielding:

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
                    break

                # Check if max strain is achieved
                conv_steps = SRC.count_converged_steps(key)
                try:
                    res_dict_inter = RP.results_reader(key, cp_code=cp_code)
                    s_yld = PostProcessingTools.calc_yield_point(res_dict_inter, False)

                    # Insert Results to the Data Base
                    new_dict_for_db = {key: {"Meta_Data": MR.meta_reader(key, cp_code=cp_code, ori_file=texture_file,
                                                                         ori_file_header=False),
                                             "Initial_Load": load.tolist(),
                                             "Scaling_Factor": scaling_factor,
                                             "Applied_Load": scaled_load.tolist(),
                                             "Max_Total_Strain": max_strain,
                                             "Results": res_dict_inter,
                                             "Time": end - start}}

                    results_dict_current = DH.read_database_from_json(os.path.join(results_dir, "Data_Base.json"))
                    combined_dict = dict(results_dict_current, **new_dict_for_db)
                    DH.json_database_creator(combined_dict, os.path.join(results_dir, "Data_Base.json"))

                    reached_yielding = True
                except IndexError:
                    if conv_steps == steps_required and not scaled_down:
                        print(
                            f'Strain is {max_strain} < yield onset and there are {conv_steps} converged steps --> scale up.')
                        scaled_load = scaled_load * scale_up
                    elif conv_steps == steps_required and scaled_down:
                        print(f'Strain is {max_strain} < yield onset and there are {conv_steps} converged steps.'
                              f'I scaled down once without success so I will try next load')
                        break

                    elif conv_steps < steps_required:
                        if max_strain > threshold_retry and not scaled_down:
                            scaled_load = scaled_load * scale_down
                            scaled_down = True
                            print(f'Strain is {max_strain} < yield onset but simulation stopped after'
                                  f' {conv_steps} converged steps. I will try to reduce load.')
                        else:
                            print(f'Strain is {max_strain} < yield onset but simulation stopped after {conv_steps} '
                                  f'converged steps. This is too far from yield onset to scale down and/or scaling down '
                                  f'didnt help.')
                            break


if __name__ == "__main__":
    # Setup argparser arguments
    parser = argparse.ArgumentParser(description='define CPFFT simulation parameters')
    parser.add_argument('-name', '--project_name', help='Name of the Project', required=True)
    parser.add_argument('-tp', '--texture_path', help='texture dir in which keys-subdirs for each bc are created',
                        required=True)
    parser.add_argument('-tf', '--texture_file', help='path texture_file.json that contains orientations',
                        required=True)
    parser.add_argument('-sup', '--setup', help='Name of setup.json that contains load keys', required=True)
    parser.add_argument('-dbp', '--database_path', help='entry path to data base structure', required=True)
    parser.add_argument('-n_gpd', '--number_grains_per_dir', help='number of grains per direction in RVE',
                        required=True)
    parser.add_argument('-n_epg', '--number_elements_per_grain', help='number of elments per grain in RVE',
                        required=True)
    parser.add_argument('-t_to', '--t_timeout', help='timeout for subprocess running CPFFT simulation', required=True)
    parser.add_argument('-opi' , '--opi_file', help='OpenPhase Input File Name', default='ProjectInput.opi')
    args = vars(parser.parse_args())

    # Read in soft-coded argument parser
    texture_file = args['texture_file']
    run_dir = args['texture_path']
    path_db = args['database_path']
    setup = args['setup']
    n_grains_per_dir = int(args['number_grains_per_dir'])
    elements_per_grain = int(args['number_elements_per_grain'])
    t_timeout = float(args['t_timeout'])
    project_name = args['project_name']
    inp_file = args['opi_file']

    print("Starting Data Generation. t_timeout is {}".format(t_timeout))
    print("RVE Size: {}-{}-{} | {} element(s) per grain".format(n_grains_per_dir, n_grains_per_dir, n_grains_per_dir,
                                                                elements_per_grain))

    main(project_name, texture_file, run_dir, path_db, setup, inp_file=inp_file, n_grains_per_dir=n_grains_per_dir,
         elements_per_grain=elements_per_grain, t_timeout=t_timeout)
