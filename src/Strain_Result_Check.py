# -*- coding: utf-8 -*-
"""
Author: Ronak Shoghi
Date: 24.05.22
Time: 15:08

"""
import os
from numpy import genfromtxt


def max_strain_finder(key, cp_code):
    current_path = os.getcwd()
    keys_path = "{}/Keys".format(current_path)
    os.chdir(keys_path)
    key_path = os.path.abspath(key)
    key_results_path = "{}/results".format(key_path)
    os.chdir(key_results_path)
    if cp_code == 'abaqus':
        strains = genfromtxt('E.out', delimiter=' ')
    elif cp_code =='openphase':
        strains = genfromtxt('{}.txt'.format(key), delimiter=';', skip_header=1)[:, -2]
    else:
        raise ValueError("cp_code {code} not valid. Must be abaqus or openphase.".format(code=cp_code))
    os.chdir(current_path)
    return max(strains)
