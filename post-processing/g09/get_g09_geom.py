#!/usr/bin/env python3

####################################################################################################
#                                                                                                  #
#                                          get_g09_geom.py                                         #
#           Python script to obtain geometries from a Gaussian09 Optimization Log File             #
#                                                                                                  #
####################################################################################################
### Author: Carlos E. V. de Moura, Ph.D. (https://github.com/carlosevmoura)                      ###
### From CompChemTools repository (https://github.com/carlosevmoura/CompChemTools)               ###
####################################################################################################
#                                                                                                  #
# Usage: get_g09_geom.py <LOG-FILE> -n <CYCLE> -f <ORIENTATION>                                    #
#                                                                                                  #
# Cycle options:                                                                                   #
#               . 'N':   Get geometry from cycle number N (positive integer number)                #
#               . 'opt': Get the optimized geometry (default)                                      #
#               . '-1':  Get the geometry of last optimization cycle                               #
#                                                                                                  #
# Orientation options:                                                                             #
#               . 'input' (default)                                                                #
#               . 'standard'                                                                       #
#               . 'zmat'                                                                           #
####################################################################################################

#################################################
###              Loading modules              ###
#################################################
##      Operating System Interfaces Module     ##
from os import path
##   System-specific parameters and functions  ##
import sys
##       Parser for command-line options       ##
import argparse
#################################################

## Function to print colored terminal messages
def print_script_output(_text, _type):
    if _type == 'error':
        print('\033[91m' + _text + '\033[m')
    elif _type == 'job_done':
        print('\033[92m' + _text + '\033[m')

## Function to obtaing the arguments from terminal
def get_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('g09_log_file',
                        type=str,
                        help='Gaussian Output File (usually .log extension)')

    parser.add_argument('-n', dest='cycle',
                        type=str,
                        default='opt',
                        help='Number of the Optimization Cycle')

    parser.add_argument('-f', dest='format',
                        type=str,
                        default='input',
                        choices=['input', 'standard', 'zmat'],
                        help='Coordinates input format')

    args = parser.parse_args()

    # Convert the number of cycles to integers
    if args.cycle.lower() != 'opt':
        args.cycle = int(args.cycle)

    return args

## Function to read g09 Log File
def open_g09_file(_arguments):
    if path.isfile(_arguments.g09_log_file):
        with open(_arguments.g09_log_file, 'rt') as file:
            g09_log = file.readlines()
            return g09_log
    else:
        print_script_output(
            '> Gaussian09 output file {} was not found.'.format(_arguments.g09_log_file),
            'error')
        sys.exit()

## Function to obtaining g09 selected geometry
def get_g09_geometry(_arguments, _g09_log):
    format_start_string = {
        'input': 'Input orientation:',
        'standard': 'Standard orientation:',
        'zmat': 'Z-Matrix orientation:'
    }

    for line in range(len(_g09_log)):
        if 'NAtoms' in _g09_log[line]:
            atoms_number = _g09_log[line].strip().split()[1]
            atoms_number = int(atoms_number)
            break

    if 'atoms_number' not in locals():
        print_script_output(
            '> Number of atoms was not found in {} Gaussian09 output.'
                .format(_arguments.g09_log_file),
            'error')
        sys.exit()

    if _arguments.cycle == 'opt':
        for line in range(len(_g09_log)):
            if 'Stationary point found' in _g09_log[line]:
                stationary_line = line
                break

        if 'stationary_line' not in locals():
            print_script_output(
                '> Stationary point was not found in {} Gaussian09 output.'
                    .format(_arguments.g09_log_file),
                'error')
            sys.exit()

        for line in range(stationary_line, len(_g09_log)):
            if format_start_string[_arguments.format] in _g09_log[line]:
                start_line = line + 5

    elif _arguments.cycle >= 0:
        cycle_count = 0
        for line in range(len(_g09_log)):
            if format_start_string[_arguments.format] in _g09_log[line]:
                cycle_count += 1

            if cycle_count > _arguments.cycle:
                start_line = line + 5
                break

        if 'start_line' not in locals():
            print_script_output(
                '> Cycle {} was not found in {} Gaussian09 output.'
                    .format(_arguments.cycle, _arguments.g09_log_file),
                'error')
            sys.exit()

    elif _arguments.cycle < 0:
        for line in reversed(range(len(_g09_log))):
            if 'Step number' in _g09_log[line]:
                total_cycles = int(_g09_log[line].strip().split()[2])
                break

        if _arguments.cycle + total_cycles < 0:
            print_script_output(
                '> Cycle {} was not found in {} cycles of {} Gaussian09 output.'
                    .format(_arguments.cycle + total_cycles, total_cycles, _arguments.g09_log_file),
                'error')
            sys.exit()

        cycle_count = 0
        for line in range(len(_g09_log)):
            if format_start_string[_arguments.format] in _g09_log[line]:
                cycle_count += 1

            if cycle_count > _arguments.cycle + total_cycles:
                start_line = line + 5
                break

    return _g09_log[start_line: start_line + atoms_number]

# Function to format g09 geometry
def format_g09_geometry(_arguments, _g09_raw_geometry):
    atom = {}
    geometry = []

    for line in range(len(_g09_raw_geometry)):
        (atom['center'], atom['atomic_number'], atom['atomic_type'],
            atom['x'], atom['y'], atom['z']) = _g09_raw_geometry[line].strip().split()
        geometry.append(atom.copy())

    return geometry

# Function to write the '.xyz' file
def write_xyz_geometry(_arguments, _g09_geometry):

    ## Defining dictionary from Atomic Numbers to Atomic Symbols
    atomic_numbers_dictionary = {
        '1': 'H',  '2': 'He',	'3': 'Li',	'4': 'Be',	'5': 'B',	'6': 'C',
        '7': 'N',	'8': 'O',	'9': 'F',	'10': 'Ne',	'11': 'Na',	'12': 'Mg',
        '13': 'Al',	'14': 'Si',	'15': 'P',	'16': 'S',	'17': 'Cl',	'18': 'Ar',
        '19': 'K',	'20': 'Ca',	'21': 'Sc',	'22': 'Ti',	'23': 'V',	'24': 'Cr',
        '25': 'Mn',	'26': 'Fe',	'27': 'Co',	'28': 'Ni',	'29': 'Cu',	'30': 'Zn',
        '31': 'Ga',	'32': 'Ge',	'33': 'As',	'34': 'Se',	'35': 'Br',	'36': 'Kr',
        '37': 'Rb',	'38': 'Sr',	'39': 'Y',	'40': 'Zr',	'41': 'Nb',	'42': 'Mo',
        '43': 'Tc',	'44': 'Ru',	'45': 'Rh',	'46': 'Pd',	'47': 'Ag',	'48': 'Cd',
        '49': 'In',	'50': 'Sn',	'51': 'Sb',	'52': 'Te',	'53': 'I',	'54': 'Xe',
        '55': 'Cs',	'56': 'Ba',	'57': 'La',	'58': 'Ce',	'59': 'Pr',	'60': 'Nd',
        '61': 'Pm',	'62': 'Sm',	'63': 'Eu',	'64': 'Gd',	'65': 'Tb',	'66': 'Dy',
        '67': 'Ho',	'68': 'Er',	'69': 'Tm',	'70': 'Yb',	'71': 'Lu',	'72': 'Hf',
        '73': 'Ta',	'74': 'W',	'75': 'Re',	'76': 'Os',	'77': 'Ir',	'78': 'Pt',
        '79': 'Au',	'80': 'Hg',	'81': 'Tl',	'82': 'Pb',	'83': 'Bi',	'84': 'Po',
        '85': 'At',	'86': 'Rn',	'87': 'Fe',	'88': 'Ra',	'89': 'Ac',	'90': 'Th',
        '91': 'Pa',	'92': 'U',	'93': 'Np',	'94': 'Pu',	'95': 'Am',	'96': 'Cm',
        '97': 'Bk',	'98': 'Cf',	'99': 'Es',	'100': 'Fm', '101': 'Md', '102': 'No',
        '103': 'Lr', '104': 'Rf', '105': 'Db', '106': 'Sg', '107': 'Bh', '108': 'Hs',
        '109': 'Mt', '110': 'Ds', '111': 'Rg', '112': 'Cn', '113': 'Uut', '114': 'Fl',
        '115': 'Uup', '116': 'Lv', '117': 'Uus', '118': 'Uuo',  '-1': 'X', '-2': 'Tv' }

    geometry_filename = _arguments.g09_log_file
    geometry_filename = geometry_filename.split('.')[0:-1][0] + '.' + str(_arguments.cycle) + '.xyz'

    with open(geometry_filename, 'w') as geometry_file:
        geometry_file.write('{}\n\n'.format(len(_g09_geometry)))

        for atom in _g09_geometry:
            geometry_file.write('{:}\t{:>10}\t{:>10}\t{:>10}\n'
                            .format(atomic_numbers_dictionary[atom['atomic_number']],
                                    atom['x'], atom['y'], atom['z']))

# Main program
if __name__ == '__main__':

    # Obtaining arguments from terminal
    arguments = get_arguments()

    # Reading g09 Log File
    g09_log = open_g09_file(arguments)

    # Obtaining g09 selected geometry
    g09_raw_geometry = get_g09_geometry(arguments, g09_log)

    # Formatting g09 geometry to output format
    g09_geometry = format_g09_geometry(arguments, g09_raw_geometry)

    # Writing the '.xyz' file
    write_xyz_geometry(arguments, g09_geometry)

    # End of get_g09_geom.py execution
    print_script_output(
        '> Geometry from {} sucessfully exported to XYZ file!'.format(arguments.g09_log_file),
        'job_done')
