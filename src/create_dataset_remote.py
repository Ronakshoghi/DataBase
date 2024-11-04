# -*- coding: utf-8 -*-
"""
Author: Jan Schmidt
Date: 09.10.2023
This script triggers nt batch jobs. Nt is the number of textures. Each texture will get its own batch script.
So if only a few loadcaes should be simulated, the time in sbatch can be reduced to e.g. 15 mins (two loadccases)
"""
import pathlib
import sys

src_dir = "/storage/home/hcoda1/7/jschmidt87/software/DataBase/src"
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
parser.add_argument('-ids', '--idx_start', help='starting index in texture order')
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
overwrite_results = False
bc_per_texture = 40  # 30
setup = 'setup_6d_iteration_1'# reconstsruciton 'setup_6d_iteration_1'

# Read soft coded args from parser
n_textures = int(args['number_textures'])
idx_start = int(args['idx_start'])
path_db = args['database_path']
path_scratch = args['scratch_path']

# Define the directory structure
project_name = args['project_name']
texture_dir = os.path.join(path_scratch,
                           "TextureFiles")  # os.path.join(path_db, "TextureFiles/{}".format(project_name))
bc_dir = os.path.join(path_scratch,
                      "BoundaryConditions")  # os.path.join(path_db, "BoundaryConditions/{}".format(project_name))

for directory in [texture_dir, bc_dir]:
    if not os.path.exists(directory):
        os.mkdir(directory)
    else:
        print(f"{directory} exists already and will not be recreated.")

# Define the sorted texture and the load file hardwired
texture_keys_sorted = os.path.join(texture_dir, "texture_keys_sorted.txt")
texture_keys_success = os.path.join(texture_dir, "textures_success.json")
bc_file = os.path.join(bc_dir, 'sig_3d_0_6d_200_texture_order.json')
#bc_file = os.path.join(bc_dir, 'sig_all.json')
with open(bc_file, 'r') as f:
    bc_dict = json.load(f)

###############################################################
#################### Create Parameter Set  ####################
###############################################################

parameter_set = {}

with open(texture_keys_sorted, "r") as f:
    texture_files_list = f.read()
texture_files_list = texture_files_list.split("\n")
texture_files_list = texture_files_list[:-1]

# Clean up texture_files list to contain only success textures from the CYL 3d study Note: Commented out for reconstruction
with open(texture_keys_success, 'r') as f:
    texture_succ_dir = json.load(f)

texture_files_list = [texture_file for texture_file in texture_files_list if
                      any(key in texture_file for key in texture_succ_dir.keys())]


texture_files_to_run = texture_files_list[idx_start:idx_start + n_textures]
print(len(texture_files_to_run))

# Fill the parameter_dict with texture_file, and boundary condition start/end indices
for idx_texture, texture_file in enumerate(texture_files_to_run):
    # print(texture_file)
    texture_key = os.path.basename(texture_file).split(sep='_')[1]
    # Create texture directory if not present in scratch
    pathlib.Path(os.path.join(path_scratch, texture_key)).mkdir(exist_ok=True)

    parameter_set[texture_key] = {'texture_file': texture_file,
                                  'bc_file': bc_file,
                                  'bc_dict': bc_dict[texture_key]} # commented out for reconstruction [texture_key]}

# Save the parameters as setup.json in the texture_key_dir
for texture_key, params_dict in parameter_set.items():
    texture_sub_dir = os.path.join(path_scratch, texture_key)
    with open(os.path.join(texture_sub_dir, f"{setup}.json"), "w") as f:
        json.dump(params_dict, f, indent=4)

###############################################################
#################### Create and Run SBATCH ####################
###############################################################

SBATCH_template = [
    '#!/bin/bash',
    '',
    '#SBATCH --job-nam=job_name',  # 2
    '#SBATCH --account=gts-skalidindi7-coda20',
    '#SBATCH -N1 --ntasks=8',  # Number of nodes and cores per node required
    '#SBATCH --mem-per-cpu=8G',  # Memory per core
    '#SBATCH -qinferno', #qinferno
    '#SBATCH -t05:00:00', #6
    '#SBATCH -oReport-%j.out',  # 8
    '#SBATCH --mail-type=FAIL',
    '#SBATCH --mail-user=jschmidt87@gatech.edu',
    '',
    'cd $SLURM_SUBMIT_DIR',
    'module load anaconda3',
    'conda activate data_generation',
    'module load fftw',
    '',
    'python3 placeholder.py'  # 17
]

# Read soft-coded parser arguments for Main script
n_grains_per_dir = args['number_grains_per_dir']
n_epg = args['number_elements_per_grain']
t_timeout = args['t_timeout']

for texture_key, params_dict in parameter_set.items():
    texture_sub_dir = os.path.join(path_scratch, texture_key)

    # create python command
    py_command = f"python {src_dir}/Main_Script_OpenPhase_Remote.py -tp {texture_sub_dir} -tf {params_dict['texture_file']}" \
                 f" -sup {setup} -dbp {path_db} -n_gpd {n_grains_per_dir} -n_epg {n_epg} -t_to {t_timeout}" \
                 f" -name {project_name}"

    # edit sbatch
    SBATCH = SBATCH_template.copy()
    SBATCH[17] = py_command
    SBATCH[2] = SBATCH_template[2].replace('job_name', f'Tex{texture_key}')

    # create sbatch
    sbatch_name = os.path.join(texture_sub_dir, f'{texture_key}.sbatch')
    with open(sbatch_name, 'w') as f:
        f.write('\n'.join(SBATCH))

    # run sbatch or py_command
    # command_sbatch = shlex.split(f'sbatch {sbatch_name}')
    command_sbatch = f'sbatch {sbatch_name}'
    command_local = shlex.split(f'{py_command}')
    # subprocess.Popen(args, cwd=dump_path)
    try:
        output = subprocess.run(command_sbatch, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                check=True, shell=True, cwd=texture_sub_dir)

    except subprocess.CalledProcessError:
        raise ValueError("Run Error")
