# -*- coding: utf-8 -*-
"""
Author: Jan Schmidt
Date: 28.04.2024

Main Script to run OpenPhase CPFFT simulations from Python.
The src_dir points to the directory where the source code of this package lies.
"""
import sys

src_dir = "/Users/jan/ronak_db/DataBase/"
sys.path.append(src_dir)
import numpy as np
from src import Key_Generator as KG
from src import Database_Handler as DH
from src import Result_Parser as RP
from src import Meta_reader as MR
from src import PostProcessingTools
from src import Key_Folder_Creator as KFC
from src import Geom_Generator as GG
from src import CP_Runner as CP
from src import Strain_Result_Check as SRC
import os
import glob
import time
import argparse
import json


def main(texture_file, rve_dir, path_db, setup, inp_file='ProjectInput.opi', n_grains_per_dir=11,
         elements_per_grain=1, t_timeout=300):
    """
    Main Function to execute OpenPhase workflow:
    1) Read the BCs from setup
    2) Create a sub-directory in {rve_dir}/Keys/ (will be the OpenPhase run directory)
    3) Modify the ProjectInput.opi, Matchbox.cpp to the current BC and RVE and copy to run directory.
    4) Make & Run the OpenPhase simulation

    Concept: I am using the {rve_dir} as the central directory. Inside this central directory, a Keys sub-directory is
    created. This sub-directory will be filled with additional sub-dirs for each BC. The names of these sub_dirs are
    following the logic: Us_A{}B{}C{}D{}E{}F{}_{load_hash}_{n_grains}_{elements_per_grain}_{ori_hash}_Tx_{tx_type}.
    This unique key will help to manage the data and store them in a large data_base e.g. Data_Base.json

    All BCs in {setup} will be executed serially. For each, a different sub-dir is created.

    Note: There is one more level of hierarchy: The {rve_dir} lies inside the {path_db}. In that way, path_db is the
    directory that contains different rve_dirs (each e.g. of different texture). Inside each rve_dir, the BC_keys are
    placed

    |-path_db
    |-LogFiles
    |--|--rve_dir_1
    |--|--|--Keys
    |--|--|--|--bc_key_1 (run_dir)
    |--|--|--|--|--orientations.csv
    |--|--|--|--|--ProjectInput.opi
    |--|--|--|--|--Matchbox.cpp
    |--|--|--|--|--Makefile
    |--|--|--|--bc_key_2
    |--|--|--|--|--...
    |--|--|--|--...
    |--|--|--|--...
    |--|--|--|--bc_key_n
    |--|--rve_dir_2...
    |--|--|--|--|--bc_key_1
    |--|--|--|--...

    Parameters
    ----------

    texture_file : str
        path to texture_file that is used to assign the orientations to the RVE.
    rve_dir : str
        path to the main directory in which the sub-directories for each BC will be reated.
    path_db : str
        path to the parent directory of rve_dir.
    setup
    inp_file
    n_grains_per_dir
    elements_per_grain
    t_timeout

    Returns
    -------

    """
    # 0 Settings
    cp_code = 'openphase'
    os.chdir(rve_dir)  # This will navigate to the RVE directory in which the different BC sub-directories are placed
    current_path = os.getcwd()
    overwrite_results = True
    times_dict = {}

    # 0.1 Define Log File directory for OpenPhase Simulation
    log_files_dir = os.path.join(path_db, "LogFiles")
    if not os.path.exists(log_files_dir):
        os.mkdir(log_files_dir)
    else:
        print(f"{log_files_dir} exists already and will not be recreated.")

    # 1 Preprocessing
    # 1.1 Read setup that contains loads
    setup_file = os.path.join(current_path, setup)
    bc_format = setup.split(sep='.')[-1]
    if bc_format == 'txt':
        print(f'Setup File {setup_file} is a txt file\n. '
              f'Read BC in Legacy format: \n each row = 1 stress bc in Voigt notation.\n'
              f'stress components seperated by ",",')
        loads_simu = np.genfromtxt(setup_file, delimiter=",")
        if len(loads_simu.shape) == 1:
            loads_simu = loads_simu.reshape((1, len(loads_simu)))
            print('+++Warning: only one load case in loadfile!+++')

    elif bc_format == 'json':
        print(f'Setup File {setup_file} is a json file\n. '
              f'Format: \n dict with key(s)=bc_key(s): val=[stress bc in Voigt notation]')
        with open(setup_file, 'r') as f:
            setup_dict = json.load(f)
            bc_dict = setup_dict['bc_dict']
        bc_array = np.array(list(bc_dict.values()))
        if len(bc_array.shape) == 1:
            loads_simu = bc_array.reshape((1, len(bc_array)))
            print('+++Warning: only one load case in loadfile!+++')
        else:
            loads_simu = bc_array
    else:
        raise ValueError(f"Setup file has format {bc_format}. Must be txt or json")

    # Main Process will be executed for each boundary condition (BC) given in the setup_file
    # NOTE: The logic here is that every BC is a new OpenPhase simulation on the same RVE.
    #       The different BCs are executed sequentially here. I decided to do this because the data-
    #       parallelism in my work is performed over different RVEs (due to different textures). So for my work,
    #       I execute this main script several times for different textures (parallel), while the BCs for
    #       each texture are run sequentially.

    "Main Process"
    for counter, load in enumerate(loads_simu):

        # 1.2 Create the result JSON file for this RVE "Data_Base.json" if not exists
        if not os.path.exists(os.path.join(current_path, "Data_Base.json")):
            print(f"No Data_Base.json for {current_path}. I create an empty one.")
            json.dump({}, open(os.path.join(current_path, "Data_Base.json"), 'w'))
        results_dict = DH.read_database_from_json(os.path.join(current_path, "Data_Base.json"))

        # 1.3 Generate unique texture_load key to identify RVE & BC
        key = KG.key_generator(load, n_grains_per_dir=n_grains_per_dir, elements_per_grain=elements_per_grain,
                               cp_code=cp_code, ori_file=texture_file)

        # 1.4 Check if the JSON file for this RVE already has results for the current BC or a LogFile exists
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

            # 1.5 Create a sub-directory in the RVE directory for the current BC in which the OpenPhase simulation will
            #     be executed
            KFC.create_sub_folder(key, cp_code=cp_code, ori_file=texture_file)

            # 1.6 Scale-up the BC (assumes given BC in setup file is a unit stress with S_J2 = 1 Pa )
            scaling_factor = 58.6e6  # 50e6 In OpenPhase we can scale here directly to J2 equiv. stress in Pa!
            print("initial load: {}".format(load))
            scaled_load = load * scaling_factor

            print("scaling factor {} -> applied load in iteration {}: {}".format(scaling_factor, 0,
                                                                                 scaled_load))

            if cp_code == 'openphase':
                # 1.7 Generate input files: Project_Input.opi, Orientations.csv, MatchBox.cpp, Makefile
                GG.openphase_input_generator(load=scaled_load, key=key, n_grains_per_dir=n_grains_per_dir,
                                             elements_per_grain=elements_per_grain, src_dir=src_dir, opi_file=inp_file)
                start = time.time()

                # 2. Run Simulation
                return_val = CP.openphase_runner(key, t_timeout=t_timeout, log_files_dir=log_files_dir)
                end = time.time()
                print("Runtime of simulation is: %f seconds" % (end - start))
                times_dict[key] = end - start
            else:
                raise ValueError("cp_code {code} not valid. Must be abaqus or openphase.".format(code=cp_code))

            # 3. Post-Processing
            # 3.1 Check maximum equivalent strain
            try:
                max_strain = SRC.max_strain_finder(key, cp_code='openphase')
                print("Max Strain: {}".format(max_strain))
            except IndexError:
                # Need to change back to main directory here because exception raised in max_strain_finder
                os.chdir(current_path)
                print("Result file contains not enough lines to find max strain!\n"
                      "Simulation did not converged!")
                continue

            # 3.2 Check if yield onset can be calculated
            try:
                res_dict_inter = RP.results_reader(key, cp_code=cp_code)
                s_yld = PostProcessingTools.calc_yield_point(res_dict_inter, False)
                # 3.3 Insert Results into the Data_Base.json file
                new_dict_for_db = {key: {"Meta_Data": MR.meta_reader(key, cp_code=cp_code, ori_file=texture_file,
                                                                     ori_file_header=False),
                                         "Initial_Load": load.tolist(),
                                         "Scaling_Factor": scaling_factor,
                                         "Applied_Load": scaled_load.tolist(),
                                         "Max_Total_Strain": max_strain,
                                         "Results": RP.results_reader(key, cp_code=cp_code),
                                         "Time": end - start}}

                results_dict_current = DH.read_database_from_json(os.path.join(rve_dir, "Data_Base.json"))
                combined_dict = dict(results_dict_current, **new_dict_for_db)
                DH.json_database_creator(combined_dict, os.path.join(rve_dir, "Data_Base.json"))
            except IndexError:
                print(
                    f'Total strain is {max_strain} < yield onset.\n'
                    f'Increase the scaling factor or check why simulation has not reached 0.2 % of plastic strain.')

if __name__ == "__main__":
    # Setup argparser arguments
    parser = argparse.ArgumentParser(description='define CPFFT simulation parameters')
    parser.add_argument('-rve', '--rve_path', help='directory in which the subdirectories for each bc are created',
                        required=True)
    parser.add_argument('-tf', '--texture_file', help='path texture_file.json that contains orientations',
                        required=True)
    parser.add_argument('-sup', '--setup', help='name of setup.json that contains load keys',
                        required=True)
    parser.add_argument('-dbp', '--database_path', help='path to directory that contains the different RVE sub-'
                                                        'directories', required=True)
    parser.add_argument('-n_gpd', '--number_grains_per_dir', help='number of grains per direction in RVE',
                        required=True)
    parser.add_argument('-n_epg', '--number_elements_per_grain', help='number of elments per grain in RVE',
                        required=True)
    parser.add_argument('-t_to', '--t_timeout', help='timeout for subprocess running CPFFT simulation', required=True)
    parser.add_argument('-opi' , '--opi_file', help='OpenPhase Input File Name', default='ProjectInput.opi')
    args = vars(parser.parse_args())

    # Read insoft-coded argument parser
    texture_file = args['texture_file']
    rve_dir = args['rve_path']
    path_db = args['database_path']
    setup = args['setup']
    n_grains_per_dir = int(args['number_grains_per_dir'])
    elements_per_grain = int(args['number_elements_per_grain'])
    t_timeout = float(args['t_timeout'])
    inp_file = args['opi_file']

    print("Starting Data Generation. t_timeout is {}".format(t_timeout))
    print("RVE Size: {}-{}-{} | {} element(s) per grain".format(n_grains_per_dir, n_grains_per_dir, n_grains_per_dir,
                                                                elements_per_grain))

    main(texture_file=texture_file, rve_dir=rve_dir, path_db=path_db, setup=setup, inp_file=inp_file,  n_grains_per_dir=n_grains_per_dir,
         elements_per_grain=elements_per_grain, t_timeout=t_timeout)

