# -*- coding: utf-8 -*-
"""
Author: Ronak Shoghi
Date: 24.05.22
Time: 15:08

"""
import os
from numpy import genfromtxt


def max_strain_finder(key, cp_code):
    """
    Finds the equivalent strain of the last increment in the result file.
    Parameters
    ----------
    key : str
        BC Key of format Us_A{}B{}C{}D{}E{}F{}_{load_hash}_{n_grains}_{elements_per_grain}_{ori_hash}_Tx_{tx_type}
    cp_code : str
        CP code used. Either abaqus or openphase.

    Returns
    -------
    maximum equivalent total strain.
    """
    current_path = os.getcwd()
    keys_path = "{}/Keys".format(current_path)
    os.chdir(keys_path)
    key_path = os.path.abspath(key)
    key_results_path = "{}/results".format(key_path)
    os.chdir(key_results_path)
    if cp_code == 'abaqus':
        strains = genfromtxt('E.out', delimiter=' ')
    elif cp_code == 'openphase':
        try:
            strains = genfromtxt('{}.txt'.format(key), delimiter=';', skip_header=1)[:, -2]
        except IndexError:
            strains = [genfromtxt('{}.txt'.format(key), delimiter=';', skip_header=1)[-2]]
    else:
        raise ValueError("cp_code {code} not valid. Must be abaqus or openphase.".format(code=cp_code))
    os.chdir(current_path)
    return max(strains)


def count_converged_steps(key):
    current_path = os.getcwd()
    keys_path = "{}/Keys".format(current_path)
    os.chdir(keys_path)
    key_path = os.path.abspath(key)
    key_results_path = "{}/results".format(key_path)
    os.chdir(key_results_path)
    strains = genfromtxt('{}.txt'.format(key), delimiter=';', skip_header=1)
    os.chdir(current_path)
    return len(strains)
