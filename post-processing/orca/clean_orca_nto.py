#!/usr/bin/env python3

####################################################################################################
#                                                                                                  #
#                                       clean_orca_nto.py                                          #
#       Python script to clean ORCA molden's files containing Natural Transition Orbitals          #
#                                                                                                  #
####################################################################################################
### Author: Carlos E. V. de Moura, Ph.D. (https://github.com/carlosevmoura)                      ###
### From CompChemTools repository (https://github.com/carlosevmoura/CompChemTools)               ###
####################################################################################################
#                                                                                                  #
# Usage: clean_orca_nto.py <MOLDEN-FILE>                                                           #
#                                                                                                  #
# Step options:                                                                                    #
#               . 'occ': NTO Occupation Threshold (default: 0.01)                                  #
#                                                                                                  #
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

def print_script_output(_text, _type):
    """Function to print colored terminal messages
    Arguments:
        _text {str} -- Text to be printed
        _type {str} -- Type of message
    """
    if _type == 'error':
        print('\033[91m' + _text + '\033[m')
    elif _type == 'job_done':
        print('\033[92m' + _text + '\033[m')

def get_arguments():
    """Function to obtaing the arguments from Terminal
    Returns:
        obj:args -- arguments given by user
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('molden_nto_file',
                        type=str,
                        help='Molden NTO filename (usually .molden.input extension)')

    parser.add_argument('-occ', dest='occupation_threshold',
                        type=str,
                        default=0.01,
                        help='NTO occupation threshold')

    args = parser.parse_args()

    # Convert occupation threshold to float
    args.occupation_threshold = float(args.occupation_threshold)

    return args

def open_ntos_molden_file(_arguments):
    """Function to read NTO Molden File
    Arguments:
        _arguments {obj} -- arguments given by user
    Returns:
        list:nto_file -- list containing NTO Molden File as strings in lines
    """
    if path.isfile(_arguments.molden_nto_file):
        with open(_arguments.molden_nto_file, 'rt') as file:
            nto_file = file.readlines()
            return nto_file
    else:
        print_script_output(
            '> Orca Molden NTO file {} was not found.'.format(_arguments.molden_nto_file),
            'error')
        sys.exit()

def format_nto_molden_file(_arguments, _nto_raw_file):
    """Function to format NTO Molden File removing unoccupied orbitals
    Arguments:
        _arguments {obj} -- arguments given by user
        _nto_raw_file {list} -- NTO Molden File lines
    Returns:
        list:molden_header -- list containing Molden file header in lines
        list:ntos_data -- list containing NTOs according to occupation threshold in lines
    """

    # Obtaining Molden file header
    for line_number, line in enumerate(_nto_raw_file):
        if "[MO]" in line:
            molden_header_end_line = line_number

    molden_header = _nto_raw_file[:molden_header_end_line+1].copy()

    # Obtaining NTOs
    nto_start_lines_number = []
    for line_number, line in enumerate(_nto_raw_file):
        if "Sym=" in line:
            nto_start_lines_number.append(line_number)

    ntos_data = []
    for mo_start_line_number, mo_end_line_number in zip(nto_start_lines_number, nto_start_lines_number[1:]):
        ntos_raw_data = _nto_raw_file[mo_start_line_number:mo_end_line_number].copy()
        for line_number, line in enumerate(ntos_raw_data):
            if "Occup=" in line:
                nto_occup = float(line.strip().split()[1])
                if nto_occup > _arguments.occupation_threshold:
                    ntos_data.extend(ntos_raw_data)

    return molden_header, ntos_data

def write_nto_molden(_arguments, _molden_header, _molden_ntos_data):
    """_summary_

    Args:
        _arguments {obj} -- arguments given by user
        _molden_header (list): Header of original Molden file
        _molden_ntos_data (list): NTOs selected accordint to occupation threshold
    """

    molden_output_filename = "nto."+_arguments.molden_nto_file

    with open(molden_output_filename, 'w') as file:
        for line in _molden_header:
            file.write(line)
        for line in _molden_ntos_data:
            file.write(line)

# Main program
if __name__ == '__main__':

    # Obtaining arguments from terminal
    arguments = get_arguments()

    # Reading Molden File
    ntos_molden_raw_file = open_ntos_molden_file(arguments)

    # Formatting Molden File removing non-occupied NTOs
    molden_header, molden_ntos_data = format_nto_molden_file(arguments, ntos_molden_raw_file)

    # Writing the '.xyz' file
    write_nto_molden(arguments, molden_header, molden_ntos_data)

    # End of clean_orca_nto.py execution
    print_script_output(
        '> NTO Molden File from {} sucessfully cleaned!'.format(arguments.molden_nto_file),
        'job_done')