import pylabfea as FE
import numpy as np
import json
import os
import hashlib

"""
This file generates the 6d unit load cases (200 per default) and creates the bc_name.json
"""


def generate_bckey(load_case):
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
    key = "Us_A{}B{}C{}D{}E{}F{}_{}".format(load_evaluation[0], load_evaluation[1], load_evaluation[2],
                                            load_evaluation[3], load_evaluation[4], load_evaluation[5],
                                            load_hash[:5])

    return key

bc_dict = {}
n_6d = 0
n_3d = 100
r_vals = True

if r_vals:
    # generate bc for r-values at [0, 15, 30, ..., 90] degree to x-direction
    json_file = 'sig_r-values.json'
    sig_6d = []
    for ang in np.arange(0, 91, 15):
        ang = np.deg2rad(ang)
        sig = np.array([np.cos(ang)**2, np.sin(ang)**2, 0, 0, 0, -1*np.sin(ang)*np.cos(ang)])

        sig /= FE.sig_eq_j2(sig)
        sig_6d.append(sig)
    sig_6d = np.array(sig_6d)
else:
    # generate a list of stress boundary conditions in Voigt notation
    json_file = f'sig_3d_{n_3d}_6d_{n_6d}.json'
    sig_6d = FE.training.load_cases(number_3d=n_3d, number_6d=n_6d)

for bc in sig_6d:
    bc_key = generate_bckey(bc)
    if bc_key in bc_dict.keys():
        raise KeyError('Two bcs have same key!')
    else:
        bc_dict[bc_key] = bc.tolist()

with open(json_file, 'w') as f:
    json.dump(bc_dict, f, indent=4)