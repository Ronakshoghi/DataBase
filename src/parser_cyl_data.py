"""
Script reads a Data_Base.json file in legacy format, where CYL results are just stored as a list of dev. stresses.
It determines the correct key, transforms data to full 6D stresses and adds {"cyl_key": "Results": [res_array],
"Initial_Load": [init_array]}

Step 2: It should also add the texture information to the json file by adding a new field.
"""
import glob

import numpy as np
import os
import pylabfea as FE
from src.Key_Generator import key_generator
import json


# Create unit stresses to transform deviatoric to full stresses
sunit = FE.load_cases(number_3d=100, number_6d=0)

#Create list of Data_Base.json files that should be updated
succ_jobs_path = "/Users/jan/pyLabFEA/examples/Texture/TextureFiles/success_jobs.json"
path_textures = "/Users/jan/pyLabFEA/examples/Texture/TextureFiles/"
path_scratch = "/Users/jan/pyLabFEA/examples/Texture/Data_CPFFT"
textures_dict = json.load(open(succ_jobs_path, 'r'))

for texture_key in textures_dict.keys():

    # 2.1) define texture_file and Data_Base.json file
    texture_file = os.path.join(path_textures, f'texturefile_{texture_key}_*.json')
    texture_file = glob.glob(texture_file)
    if len(texture_file) != 1:
        raise ValueError('More than 1 texture file with same name.')
    texture_file = texture_file[0]
    result_path = os.path.join(path_scratch, texture_key)
    res_file = os.path.join(result_path, 'Data_Base.json')
    name = texture_key
    try:
        res_dict = json.load(open(res_file, 'r'))
    except FileNotFoundError:
        print(f"{res_file} not a Data_Base.json file.")
        continue

    # 2.2) Iterate over load_keys in res_dict until CYL is found
    n_bc = len(res_dict.keys())
    for idx_bc, key in enumerate(res_dict.keys()):
        if "CYL" in key:
            keys = []
            new_dict_for_db = {}
            cyl_data = np.array(res_dict[key])
            for load_case in sunit:
                key = key_generator(load_case, n_grains_per_dir=11, elements_per_grain=1, cp_code='openphase',
                                    ori_file=texture_file)
                key += '_cyl'
                keys.append(key)
            for idx_sunit, (cyl_key, sig_dev) in enumerate(
                    zip(keys, cyl_data)):  # cyl_key is the load_key_cyl
                new_dict_for_db[cyl_key] = {}  # create an empty dict here that later gets 'Results', 'Initial Load'
                # Transform from deviatoric to Cauchy by adding the trace:
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

            combined_dict = dict(res_dict, **new_dict_for_db)
            del_key = key


    # 2.3) After updating CYL Data, add texture information on top
    texture_dict = json.load(open(texture_file, 'r'))
    texture_field = {'Texture': texture_dict}
    final_dict = dict(texture_field, **combined_dict)
    del final_dict[del_key]
    with open(res_file, 'w') as f:
        json.dump(final_dict, f, indent=4)
    print(f'Texture {texture_key} Data_Base.json has updated CYL Data.')

