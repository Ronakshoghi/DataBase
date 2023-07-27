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


def read_database_from_json(json_file):
    with open(json_file, 'r') as input_file:
        return json.load(input_file)


def json_database_creator(results_dict, json_file):
    with open(json_file, 'w') as output_file:
        json.dump(results_dict, output_file)
