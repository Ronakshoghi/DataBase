# -*- coding: utf-8 -*-
"""
Author: Ronak Shoghi
Date: 07.04.22
Time: 18:20

"""

import json

"""
Thia function insert the loads from a file into database. 
"""

def Read_Database_From_Json(json_file):
    with open(json_file, 'r') as input_file:
        return json.load(input_file)

def Json_Database_Creator(Results_Dict, json_file):
    with open (json_file, 'w') as output_file:
        json.dump(Results_Dict, output_file)