# -*- coding: utf-8 -*-
"""
Author: Ronak Shoghi
Date: 04.07.22
Time: 15:13

"""


import os
import Database_Handler as DC
import json
import matplotlib.pyplot as plt
import numpy as np

def SE_Plot (json_file ):
    """

    Parameters
    ----------
    json_file

    Returns
    -------

    """

    data = json.load(open(json_file))
    print(len(data.keys()))
    SE_data = {}
    for key in data:
        Stress = [data[key]["Results"]["S"]]
        Strain = [data[key]["Results"]["E"]]
        SE_data[key] = {"Stress": Stress, "Strain": Strain}
        plt.scatter(SE_data[key]["Strain"], SE_data[key]["Stress"], s=1)
        plt.tick_params(axis='both', which='major', labelsize=12)
        plt.xlabel("Strain", fontsize=16)
        plt.ylabel("Stress", fontsize=16)
    plt.show()


SE_Plot("Data_Base_Updated.json")

