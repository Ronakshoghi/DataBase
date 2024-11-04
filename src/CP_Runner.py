# -*- coding: utf-8 -*-
"""
Author: Ronak Shoghi
Date: 23.05.22
Time: 11:23

Modified: Jan Schmidt
Date: 04.11.24

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


def openphase_runner(key, t_timeout=300, log_files_dir=None):
    """
    Runs the OpenPhase simulation by using the subprocess package.
    First, the updated C++ file is compiled via make command. Afterwards, the executable is run.

    Parameters
    ----------
    key : str
        BC Key of format Us_A{}B{}C{}D{}E{}F{}_{load_hash}_{n_grains}_{elements_per_grain}_{ori_hash}_Tx_{tx_type}
    t_timeout : double
        Seconds after which the subprocess that triggers OpenPhase simulation is timed-out.
    log_files_dir : str
        Directory to the LogFiles.txt.

    Returns
    -------

    """
    print(key)
    if not log_files_dir:
        log_files_dir = os.getcwd()
    current_path = os.getcwd()  # /{your_RVE_dict}
    simu_path = os.path.join(current_path, "Keys/{}".format(key)) #sub-dir in which the OpenPhase simulation will run
    command_make = "make SETTINGS=static" # static make. Might be changed if dynamic libraries are compiled.
    command_run = "./MatchBox {inputfile}".format(inputfile=key + ".opi")

    # Make
    try:
        output = subprocess.run(command_make, cwd=simu_path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                check=True, shell=True)
        print("Make successfull :))")

    except subprocess.CalledProcessError:
        raise ValueError("Make Error")

    try:
        filename = os.path.join(log_files_dir, "{}.log".format(key))
        print(filename)
        #with open(filename, "w") as f:
        output = subprocess.run(command_run, cwd=simu_path, stdout=open(filename, 'w'), stderr=subprocess.STDOUT,
                                    check=True, shell=True, timeout=t_timeout, text=True)

        #    for line in output.stdout:
        #        f.write(line)
        # Remove log file if simulation converges
        os.remove(filename)

        # Remove VTK and RawData dirs
        os.removedirs(os.path.join(simu_path, "VTK"))
        os.removedirs(os.path.join(simu_path, "RawData"))
    except subprocess.TimeoutExpired:
        print("{loadcase} NOT CONVERGED".format(loadcase=key))
        os.removedirs(os.path.join(simu_path, "VTK"))
        os.removedirs(os.path.join(simu_path, "RawData"))
