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


def Key_Writer():
    "Pre-Processing"

    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    load_cases = "sigdata1.txt"
    loads = np.genfromtxt(load_cases)
    os.chdir('..')

    Key_Dict = {}

    "Main Process"
    for counter, load in enumerate(loads):
        Key = KG.Key_Generator(load)
        Key_Dict[counter] = Key

    with open ("System_Key_Translator.json", 'w') as output_file:
        json.dump(Key_Dict, output_file)


def Key_Merger():
    Results_Dict_Main = DH.Read_Database_From_Json("System_Key_Translator_Main.json")
    Results_Dict_Server = DH.Read_Database_From_Json("System_Key_Translator_Server.json")
    Translation_Dict = {}
    for key in Results_Dict_Main:
        Translation_Dict[Results_Dict_Server[key]] = Results_Dict_Main[key]

    with open ("System_Key_Translator.json", 'w') as output_file:
        json.dump(Translation_Dict, output_file)


Key_Merger()