# -*- coding: utf-8 -*-
"""
Author: Ronak Shoghi
Date: 24.03.23
Time: 09:26

"""
import math


# Function to convert radians to degrees
def radians_to_degrees(radians):
    return radians * (180 / math.pi)


# Function to convert degrees to radians
def degrees_to_radians(degrees):
    return degrees * (math.pi / 180)


# Read input file
with open('Orientation.txt', 'r') as infile:
    lines = infile.readlines()

# Process input and write output
with open('Orientation_Radian', 'w') as outfile:
    for index, line in enumerate(lines):
        # If it's the header line, copy it directly
        if index == 0:
            outfile.write(line)
            continue

        # Split the line into columns
        columns = line.strip().split()

        # Convert degrees to radians for each column
        radians_columns = [degrees_to_radians(float(deg)) for deg in columns]

        # Format the output line with 2 spaces between components in scientific notation
        output_line = '{:.5f}  {:.5f}  {:.5f}\n'.format(*radians_columns)
        # Write the output line to the output file
        outfile.write(output_line)