import sys

src_dir = "/storage/home/hcoda1/7/jschmidt87/software/DataBase/src"
sys.path.append(src_dir)
import numpy as np
import os
import pylabfea as FE
import json
from src.spacefilling import greedy_thinning
from matplotlib import pyplot as plt

"""
This file will be used to distribute the load cases in a cross-design fashion along the valid textures. It reads the 
valid texture file, chunks it into blocks of 5 Textures and assigns 40 BC to each Texture.
"""

texture_keys_sorted = '/Users/jan/Desktop/Phoenix_Code_Temp/texture_keys_sorted.txt'
bc_file = '/Users/jan/ronak_db/DataBase/src/sig_3d_0_6d_200.json'
texture_keys_success = '/Users/jan/Desktop/Phoenix_Code_Temp/textures_success.json'

bc_per_texture = 200
tx_interval = 1  # Every 25th texture should be assigned the same BCs (only for special case where bc_per_texture == n_bc_total)
with open(texture_keys_sorted, "r") as f:
    texture_files_list = f.read()
    texture_files_list = texture_files_list.split("\n")
    texture_files_list = texture_files_list[:-1]
    n_textures = len(texture_files_list)

with open(bc_file, 'r') as f:
    bc_dict = json.load(f)
    n_bc_total = len(bc_dict)

with open(texture_keys_success, 'r') as f:
    textures_success = json.load(f)

assert n_bc_total % bc_per_texture == 0, f'Number of total BCs is {n_bc_total}. Must be a integer multiple of bc per dir' \
                                       f' {bc_per_texture}'

n_chunks = n_bc_total // bc_per_texture
bc_texture_dict = {}

# # For plotting
# r = 0.05
# u, v = np.mgrid[0:2 * np.pi:30j, 0:np.pi:20j]
# x = np.cos(u) * np.sin(v)
# y = np.sin(u) * np.sin(v)
# z = np.cos(v)

for idx_texture_start in range(0, 5, n_chunks): # 0, len(texture_files_list), n_chunks):
    # # Plotting
    # fig, axs = plt.subplots(2, 3, dpi=300, subplot_kw={'projection': '3d'}, figsize=(15, 10))
    # plt.subplots_adjust(wspace=0.2, hspace=0.2)
    # axs[1, 2].plot_wireframe(x, y, z, linewidth=0.5, color='gray', alpha=0.7)
    # axs[1, 2].set_title('Distribution after 5 Textures', y=1)
    # colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple']

    # For each start index, restore the bcs and the load keys
    # bcs = FE.training.uniform_hypersphere(3, 200, method='brentq')

    bcs = np.array(list(bc_dict.values()))
    load_keys = list(bc_dict.keys())
    print("=================================================================")
    print(f"Starting with starting texture {idx_texture_start}")
    for idx_sub, idx_texture in enumerate(range(idx_texture_start, idx_texture_start+n_chunks)):
        texture_key = os.path.basename(texture_files_list[idx_texture]).split('_')[1]
        print(f'Chunk {idx_sub}, Texture {texture_key}')
        print(f'Stats:')
        print(f'        n_bcs remain: {len(bcs)}')

        if bc_per_texture != n_bc_total:
            # Determine the indices of the bc_per_textures (default=40) bcs for this texture
            idx_bc_sub = greedy_thinning(bcs, bc_per_texture)
            idx_next = [idx for idx in np.arange(0, len(bcs)) if idx not in idx_bc_sub]
            bcs_red = bcs[idx_bc_sub, :]
            bcs = bcs[idx_next, :]

            # Determine the load keys and reduce set for next iteration
            load_keys_red = [load_keys[idx] for idx in idx_bc_sub]
            load_keys = [load_keys[idx] for idx in idx_next]

            if texture_key not in bc_texture_dict.keys():
                print(f'Create new entry for {texture_key}')
                bc_texture_dict[texture_key] = {}
            if any(load_keys in load_keys_red for load_keys in bc_texture_dict[texture_key].keys()):
                raise KeyError(f'Load Keys are already present in this texture {texture_key}')
            else:
                print(f'Adding {len(load_keys_red)} bcs to {texture_key}')
                for key, value in zip(load_keys_red, bcs_red):
                    bc_texture_dict[texture_key][key] = value.tolist()
                    # print(f'Added bc {key} with {value} to Texture {texture_key}')
        else:
            # Special case where all bcs should be assigned to each texture
            if idx_texture % tx_interval == 0:
                if texture_key not in bc_texture_dict.keys():
                    print(f'Create new entry for {texture_key}')
                    bc_texture_dict[texture_key] = {}
                if any(load_keys in load_keys_red for load_keys in bc_texture_dict[texture_key].keys()):
                    raise KeyError(f'Load Keys are already present in this texture {texture_key}')
                else:
                    print(f'Adding {len(load_keys)} bcs to {texture_key}')
                    for key, value in zip(load_keys, bcs):
                        bc_texture_dict[texture_key][key] = value.tolist()

        print("-----------------------------------------------------------------")
        # if idx_sub < 3:
        #     column = idx_sub
        #     row = 0
        # else:
        #     column = idx_sub - 3
        #     row = 1
        # axs[row, column].plot_wireframe(x, y, z, linewidth=0.5, color='gray', alpha=0.7)
        # axs[row, column].scatter(bcs_red[:, 0], bcs_red[:, 1], bcs_red[:, 2], color=colors[idx_sub])
        # axs[row, column].set_title(f'Texture {idx_sub}', y=1)
        #
        # axs[1, 2].scatter(bcs_red[:, 0], bcs_red[:, 1], bcs_red[:, 2], label=f'Texture {idx_sub}',
        #                   color=colors[idx_sub])
    #
    # plt.show()

# Save as json file
bc_texture_file = 'sig_3d_0_6d_200_every25texture.json'
with open(bc_texture_file, 'w') as f:
    json.dump(bc_texture_dict, f, indent=4)