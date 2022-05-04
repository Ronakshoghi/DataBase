# -*- coding: utf-8 -*-
"""
Author: Ronak Shoghi
Date: 07.04.22
Time: 17:36

"""
"""
Thia function get any key as input and returns a list contained the corresponding sigma and hash values.
"""
def Key_Parser(keys):
    Keys_Parsered = []
    for key in keys:
        parameters = key.split('_')
        sig11 = parameters[0].split(',')
        sig22 = parameters[1].split(',')
        sig33 = parameters[2].split(',')
        sig23 = parameters[3].split(',')
        sig13 = parameters[4].split(',')
        sig12 = parameters[5].split(',')
        hash = parameters[6]
        Keys_Parsered.append([int(sig11[1]), int(sig22[1]), int(sig33[1]),
                              int(sig23[1]), int(sig13[1]), int(sig12[1]), hash])
    return (Keys_Parsered)

"""
Thia function finds the desired key based on the required load condition. 
"""

def Key_Finder (keys, Desired_Condition): #Key_Finder(Keys, [1, 1, 1, -1, 1, -1])
    Parsered_Keys = Key_Parser(keys)
    Found_Keys = []
    for key in Parsered_Keys:
        if key[0:6] == Desired_Condition:
            Found_Keys.append(key)

    return Found_Keys


def Found_Keys_Generator(keys):
    Found_Keys_Name = []
    for key in keys:
        Key_Name = "A,{}_B,{}_C,{}_D,{}_E,{}_F,{}_{}".format(key[0], key[1], key[2],
                                                        key[3], key[4], key[5],
                                                        key[6])
        Found_Keys_Name.append(Key_Name)
    return (Found_Keys_Name)