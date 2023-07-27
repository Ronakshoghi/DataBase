# -*- coding: utf-8 -*-
"""
Author: Ronak Shoghi
Date: 23.05.22
Time: 11:23

Abaqus runner scrip for each key using the prepared input files
"""

import os
import shutil
import subprocess


def Abaqus_Runner(Key, ncpu):
    print(Key)
    Current_Path = os.getcwd()
    print(Current_Path)
    Keys_Path = "{}/Keys".format(Current_Path)
    print(Keys_Path)
    os.chdir(Keys_Path)
    Key_path = os.path.abspath(Key)
    Key_Inputs_Path = "{}/inputs".format(Key_path)
    print(Key_Inputs_Path)
    os.chdir(Key_Inputs_Path)
    print('abaqus job=' + Key + '_Abaqus_Input_File.inp user=umat.f cpus=' + str(ncpu) + ' int')
    os.system('abaqus job=' + Key + '_Abaqus_Input_File.inp user=umat.f cpus=' + str(ncpu) + ' int')
    os.system('abaqus python Abaqus_Post_Processing.py')
    os.chdir(Current_Path)


def openphase_runner(key, t_timeout=300):
    print(key)
    current_path = os.getcwd() # home
    simu_path = os.path.join(current_path, "Keys/{}".format(key))
    command_make = "make SETTINGS=static"
    command_run = "./Matchbox {inputfile}".format(inputfile=key + ".opi")

    # Make
    try:
        output = subprocess.run(command_make, cwd=simu_path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                check=True, shell=True)
        print("Make successfull :))")

    except subprocess.CalledProcessError:
        raise ValueError("Make Error")

    # Run
    try:
        output = subprocess.run(command_run, cwd=simu_path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                check=True, shell=True, timeout=t_timeout)
    except subprocess.TimeoutExpired:
        print("{loadcase} NOT CONVERGED".format(loadcase=key))


