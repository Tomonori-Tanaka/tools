# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
"""
This script extracts some numerical data from Heusler QE calculations.
"""
from itertools import islice
import sys
import os


def data_extraction(filepath):
    with open(filepath, mode='r', encoding='utf-8') as f:
        latt_const = .0
        volume = .0
        total_energy = .0
        moment_1 = .0
        moment_2 = .0
        moment_3 = .0

        linecount = 0
        for line in f:
            # extract latt_const
            if "lattice parameter (alat)" in line:
                alat = float(line.split()[4])
            if "Begin final coordinates" in line:
                cellparameter_line_num = linecount + 5
                with open(filepath, mode='r', encoding='utf-8') as f_tmp:
                    for line in islice(f_tmp, cellparameter_line_num, cellparameter_line_num + 1):
                        cellparameter = float(line.split()[2])
                        latt_const = alat * cellparameter * 2

            # extract volume
            if "new unit-cell volume =" in line:
                volume = float(line.split()[4])

            # extract total_energy
            if "!    total energy" in line:
                total_energy = float(line.split()[4])

            # extract moment_*
            if "atom:    1" in line:
                moment_1 = float(line.split()[5])
            if "atom:    2" in line:
                moment_2 = float(line.split()[5])
            if "atom:    4" in line:
                moment_3 = float(line.split()[5])

            linecount += 1

    print("{0:.5f}   {1:.5f}   {2:.8f}   {3:.4f}   {4:.4f}   {5:.4f}".format(latt_const,
                                                                             volume,
                                                                             total_energy,
                                                                             moment_1,
                                                                             moment_2,
                                                                             moment_3))

"""
    print(latt_const, "     ",
          volume, "     ",
          total_energy,"     ",
          moment_1, "     ",
          moment_2, "     ",
          moment_3)
"""

if __name__ == '__main__':
    # the path of the current directory
    path = sys.argv[1]
    target_filename = "pw.out"

    for current_dir, dirs, files in os.walk(path):
        current_depth = current_dir.count(os.path.sep)
        if current_depth > 7:
            continue
        if target_filename in files:
            dirname = current_dir.split("/")[-1]
            print(dirname, end="   ")
            data_extraction(os.path.join(current_dir, target_filename))
