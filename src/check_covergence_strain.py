import sys
import os
import json
import numpy as np
src_dir = "/storage/home/hcoda1/7/jschmidt87/software/DataBase"
sys.path.append(src_dir)
from src import PostProcessingTools

path_log = "/storage/home/hcoda1/7/jschmidt87/scratch/TestSet/LogFiles/"#"/storage/home/hcoda1/7/jschmidt87/scratch/KDEApproach5deg/LogFiles"
path_scratch = "/storage/home/hcoda1/7/jschmidt87/scratch/TestSet/"
rerun_jobs_file = os.path.join(path_log, "rerun_jobs.json")
success_jobs_file = os.path.join(path_log, "success_jobs.json")
mid_jobs_file = os.path.join(path_log, 'mid_jobs.json')

sub_dirs = next(os.walk(path_scratch))[1]

textures_rerun = {}
textures_success = {}
textures_mid = {}
count_textures = 0
count_bcs = 0
count_rerun = 0
count_mid = 0
count_succ = 0
for texture_key in sub_dirs:
    texture_sub_path = os.path.join(path_scratch, texture_key)
    res_file = os.path.join(texture_sub_path, "Data_Base.json")
    try:
        with open(res_file, "r") as f:
            res_dict = json.load(f)
        count_textures+=1
        for key in res_dict.keys():
            if 'CYL' in key:
                continue
            else:
                count_bcs+=1
                # for check_key in check_keys:
                #     if check_key in key:
                max_strain = np.max(res_dict[key]["Results"]["E"])
                if max_strain < 0.002:
                    if texture_key not in textures_rerun.keys():
                        textures_rerun[texture_key] = {}
                        count_rerun += 1
                    if key not in textures_rerun[texture_key].keys():
                        textures_rerun[texture_key][key] = {}

                    textures_rerun[texture_key][key]['steps_converged'] = len(res_dict[key]["Results"]["E"])
                    textures_rerun[texture_key][key]['max_strain'] = max_strain

                else:
                    try:
                        res_cpfft = res_dict[key]['Results']
                        s_yld = PostProcessingTools.calc_yield_point(res_cpfft, False)
                        if texture_key not in textures_success.keys():
                            textures_success[texture_key] = {}
                            count_succ += 1
                        if key not in textures_success[texture_key].keys():
                            textures_success[texture_key][key] = {}

                        textures_success[texture_key][key]['steps_converged'] = len(res_dict[key]["Results"]["E"])
                        textures_success[texture_key][key]['max_strain'] = max_strain

                    except IndexError:
                        print(f'Texture {texture_key}, BC {key} above 0.2 % max strain but still too small for yield point.')
                        if texture_key not in textures_mid.keys():
                            textures_mid[texture_key] = {}
                            count_mid+=1
                        if key not in textures_mid[texture_key].keys():
                            textures_mid[texture_key][key] = {}
                        textures_mid[texture_key][key]['steps_converged'] = len(res_dict[key]["Results"]["E"])
                        textures_mid[texture_key][key]['max_strain'] = max_strain

    except FileNotFoundError:
        print(f"No Data_Base.json in dir {texture_sub_path}")
        continue

with open(rerun_jobs_file, "w") as f:
    json.dump(textures_rerun, f, indent=4)

with open(success_jobs_file, "w") as f:
    json.dump(textures_success, f, indent=4)

with open(mid_jobs_file, "w") as f:
    json.dump(textures_mid, f, indent=4)

print(f'Number of total boundary conditions: {count_bcs}')
print(f'Number of total textures: {count_textures}')
print(f'Number of success textures: {count_succ}')
print(f'Number of textures > 0.2 % max strain but too small to determine intersection: {count_mid}')
print(f'Number of textures < 0.2 % max strain: {count_rerun}')
