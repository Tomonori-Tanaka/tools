"""
This script extract jij values from kkrph verion of Akaikkr.
"""
import pandas as pd
from itertools import islice

# global variables
lattice_factor_keyword="brvtyp="
jij_detect_keyword_begin="index   site    comp"
jij_detect_keyword_end="Tc (in mean field approximation)"

def data_extraction(filepath):
    with open(filepath, mode='r', encoding='utf-8') as f:
        linecount = 0
        for line in f:
            # extract lattice factor (a)
            if lattice_factor_keyword in line:
                lattice_factor = float(line.split()[2])

            # extract jij values and store them to jij_dict
            if jij_detect_keyword_begin in line:
                jij_start_line = linecount + 1
            if jij_detect_keyword_end in line:
                jij_end_line = linecount - 1
            linecount += 1
    jij_dict = {}
    with open(filepath, mode='r', encoding='utf-8') as f:
        for line in islice(f, jij_start_line, jij_end_line):
            distance = float(line.split()[8])
            jij_value = float(line.split()[9])
            if distance in jij_dict:
                continue
            else:
                jij_dict[distance] = [jij_value]


