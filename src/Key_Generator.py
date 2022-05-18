# -*- coding: utf-8 -*-
"""
Author: Ronak Shoghi
Date: 07.04.22
Time: 15:22

"""
#It should read sigdata or load case from Abaqus_Temp_files
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
-1 = Negative

"""
import hashlib


def Key_Generator(Load_Case):
    Load_Evaluation = []

    for load in Load_Case:
        if load > 0:
            Load_Evaluation.append(1)
        if load == 0:
            Load_Evaluation.append(0)
        if load < 0:
            Load_Evaluation.append(-1)

    Load_String = ''.join(str(e) for e in Load_Case)
    Load_Hash = hashlib.sha256(Load_String.encode('utf-8')).hexdigest()

    Key = "A,{}_B,{}_C,{}_D,{}_E,{}_F,{}_{}".format(Load_Evaluation[0],Load_Evaluation[1],Load_Evaluation[2],Load_Evaluation[3],Load_Evaluation[4],Load_Evaluation[5],Load_Hash[:5])
    return (Key)


