import glob
import os.path
import sys
import pylabfea as FE
src_dir = "/storage/home/hcoda1/7/jschmidt87/software/DataBase/"
sys.path.append(src_dir)
import json
import matlab
from matlab import engine
from src import PostProcessingTools
from src.Key_Generator import key_generator
import numpy as np
import argparse
import os

"""
Run this for all valid texture subdirs with more than two converged loadcases. It calcultes the CYL yield onset for
the 100 unit stress direction (given in  /src/angles_cyl_100.csv). The results will be appended to the Data_Base.json
of each of the texture sub-directories. It will calculate for n_textuers from the textures in the success_textures.json
file starting at idx_start. 

Inputs:
See parser ojects below

Outputs:
Updated Data_Base.json files for each texture in the list. 
"""

parser = argparse.ArgumentParser(description='define simulation runner parameters')
parser.add_argument('-start', '--idx_start', help='Start index of subdict_list ', required=True)
parser.add_argument('-n', '--n_textures', help='Number of textures to be analyzed with CYL', required=True)
parser.add_argument('-st', '--succ_textures', help='json file that contains the succesfull texture keys', required=True)
parser.add_argument('-pm', '--path_mtex', help='Path to MTEX', required=True)
parser.add_argument('-ps', '--path_scratch', help='Path to scratch dir that contains texture_key subdirs',
                    required=True)
parser.add_argument('-pt', '--path_textures', help='Path to directory that stores textures', required=True)
parser.add_argument('-rj', '--recreate_json', help='Json file with texture keys and recreate bc_keys', required=False,
                    default=None)
args = vars(parser.parse_args())

# args = {"path_results": "/Users/jan/Documents/Promotion/04_GeorgiaTech/06_DataBase/02_ResultsCPFFT/KDEApproach_5deg/002c21c/Data_Base.json",
#         "path_textures": "/storage/home/hcoda1/7/jschmidt87/scratch/KDEApproach5deg/TextureFiles",
#         "path_mtex": "/Users/jan/mtex-5.8.0/",
#         "path_angles": "/Users/jan/ronak_db/DataBase/src/angles_cyl_100.csv",
#         "name": "Test"
# }

src_dir = os.path.join(src_dir, "src")
idx_start = int(args['idx_start'])
path_mtex = args['path_mtex']
n_textures = int(args['n_textures'])
succ_textures = args['succ_textures']
path_scratch = args['path_scratch']
path_textures = args['path_textures']
recreate_json = args['recreate_json']
angle_path = os.path.join(src_dir, "angles_cyl_100.csv")
taylor_factor_file = os.path.join(src_dir, "taylorFacData.mat")

# Start Matlab Enginge
eng = engine.start_matlab()
eng.addpath(path_mtex, nargout=0)
eng.startup_mtex(nargout=0)
eng.cd(src_dir)

# Define the Load Keys to be looked for in the Texture's Data Base
load_0 = 'Us_A1B2C2D0E0F0_3333e'
load_30 = 'Us_A1B0C2D0E0F0_69b89'
load_60 = 'Us_A1B1C2D0E0F0_782c2'
load_90 = 'Us_A0B1C2D0E0F0_16a1c'
load_90_2 = 'Us_A0B1C2D0E0F0_6511c'
load_120 = 'Us_A2B1C2D0E0F0_b195c'
load_150 = 'Us_A2B1C0D0E0F0_d8b76'

load_6090 = [load_60, load_90]
load_6090_2 = [load_60, load_90_2]
load_090 = [load_0, load_90]
load_090_2 = [load_0, load_90_2]
load_0120 = [load_0, load_120]
load_30120 = [load_30, load_120]
load_60150 = [load_60, load_150]
load_3060 = [load_30, load_60]
load_060 = [load_0, load_60]
load_90120 = [load_90, load_120]
load_90120_2 = [load_90_2, load_120]
load_030 = [load_0, load_30]
load_3090 = [load_30, load_90]
load_3090_2 = [load_30, load_90_2]
load_90150 = [load_90, load_150]
load_90150_2 = [load_90_2, load_150]
load_30150 = [load_30, load_150]
load_60120 = [load_60, load_120]
load_120150 = [load_120, load_150]


load_order = [load_6090, load_6090_2, load_090, load_090_2, load_0120, load_30120, load_60150, load_3060, load_060,
              load_90120, load_90120_2, load_030, load_3090, load_3090_2, load_90150, load_90150_2, load_30150,
              load_60120, load_120150]
# load_order = [load_090, load_090_2, load_6090, load_6090_2, load_0120, load_30120, load_60150, load_3060,
#               load_90120, load_90120_2, load_030, load_3090, load_3090_2, load_90150, load_90150_2, load_30150,
#               load_60120, load_120150]
overwrite = True
with open(succ_textures, 'r') as f:
    textures_success = json.load(f)

if recreate_json:
    tx_bc_dict = json.load(open(recreate_json, "r"))
    # Hardcoded file that contains already parametrized CYL filess
    if os.path.exists(recreate_json):
        with open('/storage/home/hcoda1/7/jschmidt87/scratch/KDEApproach5deg/CYL/cyl_textures_failed.json', 'r') as f:
            cyl_failed = json.load(f)
    else:
        print(f"Note: recreate_json from argparse is: {recreate_json}. Not a file!")

# Create unit stresses to transform deviatoric to full stresses
sunit = FE.load_cases(number_3d=100, number_6d=0)

count = 0
# Modified this to cyl_failed.keys in order  to re-run failed cyl jobs
for texture_key in list(textures_success.keys())[idx_start:idx_start+n_textures]:#list(textures_success.keys())[idx_start:idx_start+n_textures]:
    # added that one for textures with only one converged bc
    if texture_key in ['1f62ffa', '4d5b2e8', 'd918e4b']:
        continue
    # made this change to compare CPFFT ssucc keys to laready parametrized CYL textures, nach if-clause einrücken
    # if texture_key not in cyl_success.keys():
    texture_file = os.path.join(path_textures, f'texturefile_{texture_key}_*.json')
    texture_file = glob.glob(texture_file)
    if len(texture_file) != 1:
        raise ValueError('More than 1 texture file with same name.')
    texture_file = texture_file[0]
    result_path = os.path.join(path_scratch, texture_key)
    res_file = os.path.join(result_path, 'Data_Base.json')
    name = texture_key

    # Read the CPFFT scacling stress states from json Database
    with open(res_file, "r") as f:
        res_dict = json.load(f)

    # Check if Cyl is in res_dict
    found_cyl = False
    for key in res_dict.keys():
        if "CYL" in key:
            found_cyl = True
            continue
    if found_cyl and not overwrite:
        print("This texture contains CYL results. Will go to next one.")
        continue

    yield_points_cpfft = []
    tried_yet = False
    if recreate_json:
        # Insert dummy at the beinnig of load_pair list
        load_order.insert(0, 'dummy')
    for idx_pair, bc_pair in enumerate(load_order):
        if recreate_json and not tried_yet:
            tried_yet = True
            try:
                bc_pair = tx_bc_dict[texture_key]
            except KeyError:
                print(f'New Texture {texture_key} not available in Old Set.')
        keys_succ = textures_success[texture_key]
        res_keys = ['_'.join(key.split('_')[:3]) for key in keys_succ]
        tex_key = ['_'.join(key.split('_')[3:]) for key in res_dict.keys()][0]
        if all(elem in res_keys for elem in bc_pair):
            for bc_key in bc_pair:
                load_key = f'{bc_key}_{tex_key}'
                cpfft_res = res_dict[load_key]['Results']
                try:
                    s_yld = PostProcessingTools.calc_yield_point(cpfft_res, False)
                except IndexError:
                    print('Strain > 0.002 but still too low')
                    continue
                s_cyl = FE.s_cyl(s_yld).tolist()
                # The CYL takes stresses with angle, seq, p!!!
                s_cyl[0], s_cyl[1] = s_cyl[1], s_cyl[0]
                yield_points_cpfft.append(s_cyl)
            if len(yield_points_cpfft) != 2:
                print(f'Found only {len(yield_points_cpfft)} for that bc pair. I will try next pair')
                yield_points_cpfft = []
            else:
                break

    if len(yield_points_cpfft) != 2:
        error_msg = f'The number of CPFFT loadcases in {texture_key} DataBase is {len(yield_points_cpfft)}. Must be 2!'
        raise ValueError(error_msg)

    # Read the orienations file
    with open(texture_file, "r") as f:
        texture_dict = json.load(f)

    cyl_data = eng.cyl_taylor(name, "432", matlab.double(texture_dict['discrete_orientations_random']),
                              matlab.double(yield_points_cpfft), taylor_factor_file, result_path, angle_path, nargout=1)

    cyl_data = np.array(cyl_data) # Deviatoric Stresses + angle [S11, S22, S33, S12, S13, S23, theta]
    cyl_key = '_'.join(["Us_CYL", tex_key])
    cyl_dict = {cyl_key: cyl_data[:, :-1].tolist()}

    keys = []
    new_dict_for_db = {}
    for load_case in sunit:
        key = key_generator(load_case, n_grains_per_dir=11, elements_per_grain=1, cp_code='openphase',
                            ori_file=texture_file)
        key += '_cyl'
        keys.append(key)
    for idx_sunit, (cyl_key, values) in enumerate(zip(keys, cyl_data[:, :-1].tolist())): #cyl_key is the load_key_cyl
        new_dict_for_db[cyl_key] = {} # create an empty dict here that later gets 'Results', 'Initial Load'
        # Transform from deviatoric to Cauchy by adding the trace:
        sig_dev = np.array(values)
        s_unit = sunit[idx_sunit]
        s_unit_dev = FE.sig_dev(s_unit)

        # Set small values to 0
        sig_dev[np.abs(sig_dev) < 1e-4] = 0
        s_unit[np.abs(s_unit) < 1e-4] = 0
        s_unit_dev[np.abs(s_unit_dev) < 1e-4] = 0

        # Calculate scaled hydrostatic pressure to reconstruct 6d stress
        p = np.nan_to_num(sig_dev[:3] / s_unit_dev[:3] * np.sum(sunit[idx_sunit][:3]))
        # print(f'pressure: {p}, with std {np.std(p)}')
        nonzeros = p[np.abs(p) > 1e-6]
        assert np.std(nonzeros) / np.mean(nonzeros) < 1e-3

        # pressure should be the same for all commponents
        # print(f'original deviatoric: {sig_dev}')
        sig_cauchy = sig_dev + 1 / 3 * np.append(p, [0, 0, 0])
        sig_cauchy[np.abs(sig_cauchy) < 1e-4] = 0
        # print(f'final 6d stress {sig_cauchy}')
        # print(f'initial stress {s_unit}')

        # Check if components are scaled up by same factor w.r.t unit stress
        sig_check = np.nan_to_num(sig_cauchy / s_unit)
        # print(f'6d stree / unit stress {sig_check}')
        nonzeros = sig_check[np.abs(sig_check) > 1e-6]
        # print(f'Check sunit to final: {np.std(nonzeros)}')
        assert np.std(nonzeros) / np.mean(nonzeros) < 1e-3

        new_dict_for_db[cyl_key]['Initial_Load'] = sunit[idx_sunit].tolist()
        new_dict_for_db[cyl_key]['Results'] = sig_cauchy.tolist()


    if cyl_key in res_dict.keys() and not overwrite:
        print(f'Texture {tex_key} alread has CYL Data. Will NOT overwrite it')
    else:
        ## Old way: Adding yield onsets as list
        # res_dict[cyl_key] = cyl_data[:, :-1].tolist()
        # with open(res_file, 'w') as f:
        #     json.dump(res_dict, f, indent=4)
        # print(f'Texture {tex_key} Data_Base.json has now CYL Data:) .')
        combined_dict = dict(res_dict, **new_dict_for_db)
        with open(res_file, 'w') as f:
            json.dump(combined_dict, f, indent=4)
        print(f'Texture {tex_key} Data_Base.json has now CYL Data:) .')

    count += 1
    print(f'Calculated CYL yieldonsets for {count} textures in this run of the script.')
    if count == n_textures:
        print(f"Reached {n_textures} textures. Finished :))")
        break
# Save the unit stresses as load cases for CYLvsCPFFT comparison
# cyl_data = np.array(cyl_data)[:, :-1]
# cyl_data_unit = cyl_data/FE.seq_J2(cyl_data)[:,None]
# np.savetxt(os.path.join(result_path, f"sig_180_{name}.txt"), cyl_data_unit, delimiter=',')
