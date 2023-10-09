# -*- coding: utf-8 -*-
"""
Author: Ronak Shoghi
Date: 07.04.22
Time: 15:22

"""
# It should read sigdata or load case from Abaqus_Temp_files
import json
import numpy as np

"""
This function creates a unique key for each load case which then will be used to identify and select any desired load case in the database. 
Symbol Guidline:
A = sigma 11
B = sigma 22
C = sigma 33
D = sigma 23
E = sigma 13
F = sigma 12

1 = Positive
0 = Zero
2 = Negative

"""
import hashlib
import os
import warnings


def key_generator(load_case, n_grains_per_dir=11, elements_per_grain=8, cp_code='abaqus', ori_file='Orientation.txt'):
    current_path = os.getcwd()
    if cp_code == 'abaqus':
        temp_files_path = "{}/Abaqus_Temp_Files".format(current_path)
        orientation_file_path = "{}/{}".format(temp_files_path, ori_file)
    elif cp_code == 'openphase':
        print("OpenPhase takes texturefiles.json given as absolute path.")
    else:
        raise ValueError("cp_code {code} not valid. Must be abaqus or openphase.".format(code=cp_code))

    load_evaluation = []

    for load in load_case:
        if load > 0:
            load_evaluation.append(1)
        if load == 0:
            load_evaluation.append(0)
        if load < 0:
            load_evaluation.append(2)

    load_string = ''.join(str(e) for e in load_case)
    load_hash = hashlib.sha256(load_string.encode('utf-8')).hexdigest()

    if cp_code == 'abaqus':
        with open(orientation_file_path, 'r') as f:
            data_csv = np.genfromtxt(f, delimiter=',')
        orientation_hash = hashlib.sha256(data_csv).hexdigest()[:5]
        tx = 'abq_csv'

    else:
        with open(ori_file, 'r') as f:
            data_json = json.load(f)
        data_ori = np.array(data_json['discrete_orientations'])
        orientation_hash = hashlib.sha256(data_ori).hexdigest()[:5]
        if data_json['halfwidth'] < 0.0018:
            tx = 'sc'
        else:
            tx = 'pc'
    # if ori_file != 'Orientations.txt':
    #     try:
    #         # e.g. orientations_ori-hash.txt
    #         ori_hash = ori_file.split('_')[1].split('.')[0]
    #     except ValueError:
    #         print('ori_file {} not in standard format orientations_ori-hash.txt'.format(ori_file))
    #
    #     if ori_hash != orientation_hash[:5]:
    #         # TODO warning string is not  working with formating.
    #         warnings.warn('Orientation file %s was given. Hash in Filename %s is NOT consistent with '
    #                           'generated hash for key %s.' % (ori_file, ori_hash, orientation_hash))

    key = "Us_A{}B{}C{}D{}E{}F{}_{}_{}_{}_{}_Tx_{}".format(load_evaluation[0], load_evaluation[1], load_evaluation[2],
                                                           load_evaluation[3], load_evaluation[4], load_evaluation[5],
                                                           load_hash[:5], n_grains_per_dir ** 3, elements_per_grain,
                                                           orientation_hash, tx)
    return key
