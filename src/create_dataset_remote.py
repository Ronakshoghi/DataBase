# -*- coding: utf-8 -*-
"""
Author: Jan Schmidt
Date: 09.10.2023

"""

import sys
src_dir = "/Users/jan/ronak_db/DataBase"
sys.path.append(src_dir)
import numpy as np
import os
import glob
import argparse
import shlex
import subprocess
import json


"""

:return:
"""

# arguments for DoE
parser = argparse.ArgumentParser(description='define simulation runner parameters')
parser.add_argument('-name', '--project_name', help='Name of the Project', required=True)
parser.add_argument('-nt', '--number_textures', help='number of textures to simulate', required=True)
#parser.add_argument('-rp', '--run_path', help='path where simulation runs', required=True)
parser.add_argument('-dbp', '--database_path', help='entry path to data base structure', required=True)
parser.add_argument('-sp', '--scratch_path', help='path where the texture_key folders are created', required=True)

# arguments for Main_Script_OpenPhase
parser.add_argument('-n_gpd', '--number_grains_per_dir', help='number of grains per direction in RVE',
                    required=True)
parser.add_argument('-n_epg', '--number_elements_per_grain', help='number of elments per grain in RVE',
                    required=True)
parser.add_argument('-t_to', '--t_timeout', help='timeout for subprocess running CPFFT simulation', required=True)
args = vars(parser.parse_args())

# settings
overwrite_results = True
bc_per_texture = 30

#debug

# args = {'number_textures': 1,
#         'database_path': "/Users/jan/Documents/Promotion/04_GeorgiaTech/06_DataBase",
#         'scratch_path': "/Users/jan/Documents/Promotion/04_GeorgiaTech/07_RemoteTest",
#         'project_name': "RemoteTest",
#         'number_grains_per_dir': 11,
#         'number_elements_per_grain': 1,
#         't_timeout': 400
# }

# Read soft coded args from parser
n_textures = args['number_textures']
path_db = args['database_path']
path_scratch = args['scratch_path']

# Define the directory structure
project_name = args['project_name']
texture_dir = os.path.join(path_db, "01_TextureFiles/{}".format(project_name))
bc_dir = os.path.join(path_db, "03_BoundaryConditions/{}".format(project_name))

for directory in [texture_dir, bc_dir]:
    if not os.path.exists(directory):
        os.mkdir(directory)
    else:
        print(f"{directory} exists already and will not be recreated.")

# Define the sorted texture and the load file hardwired
texture_keys_sorted = os.path.join(texture_dir, "texture_keys_sorted.txt")
bc_file = os.path.join(bc_dir, "sig_cyl_180.txt")
bc_array = np.genfromtxt(bc_file, delimiter=",")
n_shear = len(bc_array)
n_splits = n_shear / bc_per_texture
if not n_splits.is_integer():
    raise ValueError("n_splits is {}. Must be a whole number!".format(n_splits))


###############################################################
#################### Create Parameter Set  ####################
###############################################################

parameter_set = {}

# Find entry point in sorted texture list
processed_textures = [os.path.basename(directory) for directory in
                      glob.glob(os.path.join(path_scratch, "*"))]
with open(texture_keys_sorted, "r") as f:
    texture_files_list = f.read()
texture_files_list = texture_files_list.split("\n")
found_startpoint = 0
for idx_texture, texture_file in enumerate(texture_files_list):
    print(os.path.basename(texture_file))
    texture_key = os.path.basename(texture_file).split(sep='_')[1]  # e.g. "0dc82"
    if texture_key not in processed_textures:
        found_startpoint = idx_texture
        break

texture_files_to_run = texture_files_list[found_startpoint:found_startpoint + n_textures]

# Fill the parameter_dict with texture_file, and boundary condition start/end indices
for idx_texture, texture_file in enumerate(texture_files_to_run):
    texture_key = os.path.basename(texture_file).split(sep='_')[1]

    # Determine the boundary conditions for this texture (assumes that n_splits is a whole number)
    idx_bc_begin = int(
        (found_startpoint - np.floor((found_startpoint + idx_texture) / n_splits) * n_splits) * bc_per_texture)
    idx_bc_end = int(idx_bc_begin + bc_per_texture)

    parameter_set[texture_key] = {'texture_file': texture_file,
                                  'bc_file': bc_file,
                                  'idx_bc_start': idx_bc_begin,
                                  'idx_bc_end': idx_bc_end}

# Save the parameters as setup.json in the texture_key_di
for texture_key, params_dict in parameter_set.items():
    texture_sub_dir = os.path.join(path_scratch, texture_key)
    os.mkdir(texture_sub_dir)
    with open(os.path.join(texture_sub_dir, "setup.json"), "w") as f:
        json.dump(params_dict, f, indent=4)

    with open(os.path.join(texture_sub_dir,"Data_Base.json"), "w") as f:
        empty_dict = {}
        json.dump(empty_dict, f)

###############################################################
#################### Create and Run SBATCH ####################
###############################################################

SBATCH_template = [
    '#!/bin/bash',
    '',
    '#SBATCH -J job_name',  # 2
    '#SBATCH --account gts-skalidindi7-coda20',
    '#SBATCH -N1 --ntasks=4',  # Number of nodes and cores per node required
    '#SBATCH --mem-per-cpu=8G',  # Memory per core
    '#SBATCH -q embers',
    '#SBATCH -t 03:00:00',
    '#SBATCH -o out/\%j.out',  # 8
    '#SBATCH --mail-type=ALL',
    '#SBATCH --mail-user=jschmidt87@gatech.edu',
    '',
    'cd $SLURM_SUBMIT_DIR',
    'module load anaconda3',
    'conda activate data_generation',
    '',
    'python3 placeholder.py'  # 16
]

# Read soft-coded parser arguments for Main script
n_grains_per_dir = args['number_grains_per_dir']
n_epg = args['number_elements_per_grain']
t_timeout = args['t_timeout']

for texture_key, params_dict in parameter_set.items():
    texture_sub_dir = os.path.join(path_scratch, texture_key)

    # create python command
    py_command = f"python Main_Script_OpenPhase_Remote.py -tp {texture_sub_dir} -tf {params_dict['texture_file']}" \
                 f" -bcp {params_dict['bc_file']} -idx_s {params_dict['idx_bc_start']}" \
                 f" -idx_e {params_dict['idx_bc_end']} -dbp {path_db} -n_gpd {n_grains_per_dir} -n_epg {n_epg}" \
                 f" -t_to {t_timeout} -name {project_name}"

    # edit sbatch
    SBATCH = SBATCH_template.copy()
    SBATCH[16] = py_command
    SBATCH[2] = SBATCH_template[2].replace('job_name', f'Texture {texture_key}')

    # create sbatch
    sbatch_name = os.path.join(texture_sub_dir, f'{texture_key}.sbatch')
    with open(sbatch_name, 'w') as f:
        f.write('\n'.join(SBATCH))

    # run sbatch or py_command
    command_sbatch = shlex.split(f'sbatch {sbatch_name}')
    command_local = shlex.split(f'{py_command}')
    #subprocess.Popen(args, cwd=dump_path)
    try:
        output = subprocess.run(py_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                check=True, shell=True)

    except subprocess.CalledProcessError:
        raise ValueError("Run Error")
