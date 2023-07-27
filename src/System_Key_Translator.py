# -*- coding: utf-8 -*-
"""
Author: Ronak Shoghi
Date: 10.08.22
Time: 19:34

"""

import numpy as np
import Key_Generator as KG
import json
import Database_Handler as DH
import os


def key_writer():
    "Pre-Processing"

    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    load_cases = "sigdata1.txt"
    loads = np.genfromtxt(load_cases)
    os.chdir('..')

    key_dict = {}

    "Main Process"
    for counter, load in enumerate(loads):
        key = KG.key_generator(load)
        key_dict[counter] = key

    with open("System_Key_Translator.json", 'w') as output_file:
        json.dump(key_dict, output_file)


def key_merger():
    results_dict_main = DH.read_database_from_json("System_Key_Translator_Main.json")
    results_dict_server = DH.read_database_from_json("System_Key_Translator_Server.json")
    translation_dict = {}
    for key in results_dict_main:
        translation_dict[results_dict_server[key]] = results_dict_main[key]

    with open("System_Key_Translator.json", 'w') as output_file:
        json.dump(translation_dict, output_file)


key_merger()
