import glob
import os
import json
import numpy as np
import hashlib

texture_dir = "/Users/jan/Documents/Promotion/04_GeorgiaTech/06_DataBase/01_TextureFiles/Old"
texture_files_list = glob.glob(os.path.join(texture_dir, "*.json"))
texture_key_translation_dict = {}

# iterate through json files and rename them
for texture_file in texture_files_list:
    with open(texture_file, "r") as f:
        texture_dict = json.load(f)

    # determine Hash
    data_ori = np.array(texture_dict['discrete_orientations'])
    orientation_hash = hashlib.sha256(data_ori).hexdigest()[:5]
    if texture_dict['halfwidth'] < 0.0018:
        tx = 'sc'
    else:
        tx = 'pc'

    filename = "texturefile_{}_{}.json".format(orientation_hash, tx)

    # store key and original file name
    texture_key_translation_dict[orientation_hash] = os.path.basename(texture_file)

    with open(os.path.join(texture_dir, filename), "w") as f:
        json.dump(texture_dict, f, indent=4)

with open(os.path.join(texture_dir, "translation_dict_key_name.json"), "w") as f:
    json.dump(texture_key_translation_dict, f, indent=4)
