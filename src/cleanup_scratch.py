import os
import shutil
import numpy as np
import argparse
"""
I noticed that the scratch is restricted to 1 Mil files. This file goes through the keys subdirs and removes the 
Makefile, the binary and the results folder.
"""

files_to_remove = ['Makefile', 'MatchBox', 'MatchBox.cpp', 'orientations.csv']
dirs_to_remove = ['results']

parser = argparse.ArgumentParser(description='define dir to be cleaned')
parser.add_argument('-pt', '--path_scratch', help='Name of the folder that holds all textures to be cleared',
                    required=True)
args = vars(parser.parse_args())

path_scratch = args['path_scratch']
sub_dirs = next(os.walk(path_scratch))[1]
for texture in sub_dirs:
    path_texture = os.path.join(path_scratch, texture)
    path_loads = os.path.join(path_texture, 'Keys')
    if os.path.exists(path_loads):
        load_dirs = next(os.walk(path_loads))[1]
        for load_dir in load_dirs:
            load_path = os.path.join(path_loads, load_dir)
            print(load_path)
            for file in files_to_remove:
                if file == 'orientations.csv':
                    file = '_'.join([load_dir, file])
                try:
                    os.remove(os.path.join(load_path, file))
                except FileNotFoundError:
                    print(f'{file} does not exist')
                    continue
            for file in dirs_to_remove:
                try:
                    shutil.rmtree(os.path.join(load_path, file))
                except FileNotFoundError:
                    print(f'no result dir for this loadcase {file}')
                    continue
    else:
        continue
