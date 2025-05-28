import sys
import json
import os
import argparse
import pylabfea as FE
src_dir = "/storage/home/hcoda1/7/jschmidt87/software/DataBase/"
sys.path.append(src_dir)
from src.Key_Generator import key_generator
from src.PostProcessingTools import calc_yield_point
import numpy as np
"""
This file reads the Data_Base.json objects in the texture_key subdirs and write them in a single Data_Base_xxxx.json 
file. The purpose of this is to preprocess the CP results from multiple textures in to one file that can then be read
by the pylabfea data.py script.
"""
parser = argparse.ArgumentParser(description='Define the Data_Base_xxxx.json parameters')
parser.add_argument('-n', '--name', help='Name added to Data_Base_xxxx.json', required=True)
parser.add_argument('-tl', '--texture_list', help='txt file containing the textures to be read', required=True)
parser.add_argument('-ps', '--path_scratch', help='Path to scratch directory that contains texture_key subdirs',
                    required=True)
parser.add_argument('-pd', '--path_db', help='Path to which the Data_Base_xxx.json should be written',
                    required=True)

args = vars(parser.parse_args())
name = args['name']
texture_list = args['texture_list']
path_scratch = args['path_scratch']
path_texturefiles = os.path.join(path_scratch, 'TextureFiles')
path_db_final = args['path_db']
data_base_dict = {}
endpoint = 5 # 7225

# Read the ordered texture files (this is the way I do this until I got all results. I dont wanna mess things up while
# CPFFT simulations are still running

with open(texture_list, "r") as f:
    texture_files_list = f.read()
texture_files_list = texture_files_list.split("\n")
texture_files_list = texture_files_list[:-1]

texture_keys_success = os.path.join(path_scratch, "TextureFiles/success_jobs.json") #textures_ssuccesss.json
# Clean up texture_files list to contain only success textures from the CYL 3d study
# with open(texture_keys_success, 'r') as f:
#     texture_succ_dir = json.load(f)
#
# texture_files_list = [texture_file for texture_file in texture_files_list if
#                       any(key in texture_file for key in texture_succ_dir.keys())]

texture_keys_list = [os.path.basename(texture_path).split(sep='_')[-2] for texture_path in texture_files_list]

# Create the keys and unit stresses for the CTL loadcases
n_grains_per_dir = 11
sunit = FE.load_cases(number_3d=100, number_6d=0)

# Iterate through the texture sub dictionaries in path_scratch and read Data_Base.json
n_textures = len(texture_files_list)
for texture_key, texture_file in zip(texture_keys_list[:endpoint], texture_files_list[:endpoint]):
    # Modify texture file to be independent on directory
    filename = os.path.basename(texture_file)
    texture_file = os.path.join(path_texturefiles, filename)

    sub_dir = os.path.join(path_scratch, texture_key)
    db_path = os.path.join(sub_dir, 'Data_Base.json')
    if texture_key in data_base_dict.keys():
        raise KeyError(f'{texture_key} already exist in Data_Base_dict.')
    else:
        data_base_dict[texture_key] = {}
        db_dict = json.load(open(db_path, 'r'))
        n_bcs = len(db_dict.values())
        n_succ = 0
        for load_key, value_dict in db_dict.items():
            assert load_key not in data_base_dict[texture_key].keys()
            if 'CYL' in load_key:
                # Create keys for each of the 100 cyl loading directions
                keys = []
                for load_case in sunit:
                    key = key_generator(load_case, n_grains_per_dir=11, elements_per_grain=1, cp_code='openphase',
                                        ori_file=texture_file)
                    key += '_cyl'
                    keys.append(key)
                for idx_sunit, (cyl_key, values) in enumerate(zip(keys, value_dict)):
                    data_base_dict[texture_key][cyl_key] = {}
                    # Transform from deviatoric to Cauchy by adding the trace:
                    sig_dev = np.array(values)
                    s_unit = sunit[idx_sunit]
                    s_unit_dev = FE.sig_dev(s_unit)

                    # Set small values to 0
                    sig_dev[np.abs(sig_dev) < 1e-4] = 0
                    s_unit[np.abs(s_unit) < 1e-4] = 0
                    s_unit_dev[np.abs(s_unit_dev) < 1e-4] = 0

                    # Calculate scaled hydrostatic pressure to reconstruct 6d stress
                    p = np.nan_to_num(sig_dev[:3]/s_unit_dev[:3] * np.sum(sunit[idx_sunit][:3]))
                    #print(f'pressure: {p}, with std {np.std(p)}')
                    nonzeros = p[np.abs(p) > 1e-6]
                    assert np.std(nonzeros) / np.mean(nonzeros) < 1e-3

                    # pressure should be the same for all commponents
                    #print(f'original deviatoric: {sig_dev}')
                    sig_cauchy = sig_dev + 1/3*np.append(p, [0, 0, 0])
                    sig_cauchy[np.abs(sig_cauchy) < 1e-4] = 0
                    #print(f'final 6d stress {sig_cauchy}')
                    #print(f'initial stress {s_unit}')

                    # Check if components are scaled up by same factor w.r.t unit stress
                    sig_check = np.nan_to_num(sig_cauchy / s_unit)
                    #print(f'6d stree / unit stress {sig_check}')
                    nonzeros = sig_check[np.abs(sig_check) > 1e-6]
                    #print(f'Check sunit to final: {np.std(nonzeros)}')
                    assert np.std(nonzeros) / np.mean(nonzeros) < 1e-3

                    data_base_dict[texture_key][cyl_key]['Results'] = sig_cauchy.tolist()
                    data_base_dict[texture_key][cyl_key]['Initial_Load'] = sunit[idx_sunit].tolist()
                    n_succ +=1
            else:
                data_base_dict[texture_key][load_key] = {}
                #data_base_dict[texture_key][load_key]['Results'] = value_dict['Results']
                try:
                    data_base_dict[texture_key][load_key]['Results'] = calc_yield_point(value_dict['Results']).tolist()
                    data_base_dict[texture_key][load_key]['Strain_pl'] = calc_yield_point(value_dict['Results'],
                                                                                          write_strains=True).tolist()
                    data_base_dict[texture_key][load_key]['Initial_Load'] = value_dict['Initial_Load']
                    n_succ += 1
                except IndexError:
                    max_strain = value_dict["Results"]["E"][-1]
                    print('Max Strain is too low', max_strain)
                    continue
        texture_dict = json.load(open(texture_file, 'r'))
        data_base_dict[texture_key]['texture_descriptors'] = {}
        for key in ['address_vector_16', 'address_vector_111', 'address_vector_1232', 'address_vector_1737', 'gsh_coeff_reconstructed_random']:
            data_base_dict[texture_key]['texture_descriptors'][key] = texture_dict[key]
        print(f'For texture {texture_key}: {n_succ}/{n_textures} succesfull results')
with open(os.path.join(path_db_final, f'Data_Base_{name}.json'), 'w') as f:
    json.dump(data_base_dict, f, indent=4)
