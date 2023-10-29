"""
This file can be used to order the texture files. Ordering follows nearest neighbor approach.
Starting with an initial texture file, the next file is chosen based on its nearest neighbor.
The closer to the end of the list, the larger the gaps may be because between one file to the next.
Texture files are ordered to allow the distribution of the 200 shear load cases on similar textures.
I hope that by that procedure, a non-factorial DoE can be applied in which not every texture requires
every load case and correlation between texture space and stress space can be used.
"""

import numpy as np
import os
import glob
import json
from sklearn.neighbors import NearestNeighbors

texture_dir = "/Users/jan/Documents/Promotion/04_GeorgiaTech/06_DataBase/01_TextureFiles/Old"
similarity_key = 'gsh_coeff_reconstructed' # 'gsh_coeff_original' #
texture_files_list = glob.glob(os.path.join(texture_dir, "*.json"))
texture_keys_list = [os.path.basename(file) for file in glob.glob(os.path.join(texture_dir, "*"))]
texture_list_sorted = []
gsh_dict = {}
start_point = 0

for texture_file in texture_files_list:
    texture_key = os.path.basename(texture_file).split(sep='_')[-1].split(sep='.')[0]
    with open(texture_file, "r") as f:
        texture_dict = json.load(f)
    gsh_dict[texture_file] = texture_dict[similarity_key]

# fit nearest neighbor to find closest point to every microstructure
neigh = NearestNeighbors(n_neighbors=2)
neigh.fit([ms for ms in gsh_dict.values()], list(gsh_dict.keys()))

# start the ordering
texture_file = texture_files_list[start_point]
while len(texture_files_list) > 0:
    texture_key = os.path.basename(texture_file).split(sep='_')[-1].split(sep='.')[0]
    with open(texture_file, "r") as f:
        texture_dict = json.load(f)
    texture_list_sorted.append(texture_file)
    print(80 * '_')
    print('Adding ', texture_file)
    print(80 * '-')

    # Calculate next texture_file based on nearest neighbor
    if len(texture_files_list) > 1:
        nearest_neighbor_idx = neigh.kneighbors([gsh_dict[texture_file]], return_distance=False)[-1, 1]

    # Remove texture_files that have already been parametrized and define next
    old_file = texture_file
    if len(texture_files_list) > 1:
        texture_file = list(gsh_dict.keys())[nearest_neighbor_idx]
    texture_files_list.remove(old_file)
    print(80 * '-')
    print('Removed File: ', old_file)

    # Remove texture_meta_files_list from kNN lists and refit kNN
    del gsh_dict[old_file]
    if len(texture_files_list) > 1:
        neigh.fit([ms for ms in gsh_dict.values()], list(gsh_dict.keys()))

    print(80 * '-')
    print('Removed current files from lists:')
    print('files_list: ', len(texture_files_list))
    print('address_vector_list:', len(list(gsh_dict.values())))
    print(80 * '-')
    print('Next Texture_file: ', texture_file)
    print(80 * '_')

with open(os.path.join(texture_dir, 'texture_keys_sorted.txt'), 'w') as f:
    for line in texture_list_sorted:
        f.write(f"{line}\n")