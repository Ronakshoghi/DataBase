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
2 = Negative

"""
import hashlib
import os


def Key_Generator(Load_Case):

    Current_Path = os.getcwd()
    Abaqus_Temp_Files_Path = "{}/Abaqus_Temp_Files".format(Current_Path)
    Orientation_File_Path = "{}/Orientation.txt".format(Abaqus_Temp_Files_Path)
    Load_Evaluation = []

    for load in Load_Case:
        if load > 0:
            Load_Evaluation.append(1)
        if load == 0:
            Load_Evaluation.append(0)
        if load < 0:
            Load_Evaluation.append(2)

    Load_String = ''.join(str(e) for e in Load_Case)
    Load_Hash = hashlib.sha256(Load_String.encode('utf-8')).hexdigest()
    Tx="Rnd"
    with open(Orientation_File_Path) as f:
        data = f.read()
        Orientation_Hash = hashlib.sha256(data.encode('utf-8')).hexdigest()
    Key = "Us_A{}B{}C{}D{}E{}F{}_{}_{}_Tx_{}".format(Load_Evaluation[0],Load_Evaluation[1],Load_Evaluation[2],Load_Evaluation[3],Load_Evaluation[4],Load_Evaluation[5],Load_Hash[:5],Orientation_Hash[:5],Tx)
    return (Key)


