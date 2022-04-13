#!/usr/bin/env python3

####################################################################################################
#                                                                                                  #
#                                 get_molden_active_space.py                                       #
#    Python script to molden's file containing only Active Space Orbitals in CAS calculations      #
#                                                                                                  #
####################################################################################################
### Author: Carlos E. V. de Moura, Ph.D. (https://github.com/carlosevmoura)                      ###
### From CompChemTools repository (https://github.com/carlosevmoura/CompChemTools)               ###
####################################################################################################
#                                                                                                  #
# Usage: get_molden_active_space.py <MOLDEN-FILE>                                                           #
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

    parser.add_argument('molden_filename',
                        type=str,
                        help='Molden CAS filename (usually .molden extension)')

    args = parser.parse_args()

    return args

def open_molden_file(_arguments):
    """Function to read Molden File
    Arguments:
        _arguments {obj} -- arguments given by user
    Returns:
        list:molden_file -- list containing Molden File as strings in lines
    """
    if path.isfile(_arguments.molden_filename):
        with open(_arguments.molden_filename, 'rt') as file:
            molden_file = file.readlines()
            return molden_file
    else:
        print_script_output(
            '> Molden file {} was not found.'.format(_arguments.molden_filename),
            'error')
        sys.exit()

def format_molden_file(_raw_file):
    """Function to format CAS Molden File removing unoccupied and full-occupied orbitals
    Arguments:
        _arguments {obj} -- arguments given by user
        _raw_file {list} -- Molden File lines
    Returns:
        list:molden_header -- list containing Molden file header in lines
        list:cas_data -- list containing active space orbitals
    """

    # Obtaining Molden file header
    for line_number, line in enumerate(_raw_file):
        if "[MO]" in line:
            molden_header_end_line = line_number

    molden_header = _raw_file[:molden_header_end_line+1].copy()

    # Obtaining NTOs
    mo_start_lines_number = []
    for line_number, line in enumerate(_raw_file):
        if "Sym=" in line:
            mo_start_lines_number.append(line_number)

    cas_mos_data = []
    for mo_start_line_number, mo_end_line_number in zip(mo_start_lines_number, mo_start_lines_number[1:]):
        mo_raw_data = _raw_file[mo_start_line_number:mo_end_line_number].copy()
        for line_number, line in enumerate(mo_raw_data):
            if "Occup=" in line:
                mo_occup = float(line.strip().split()[1])
                if (mo_occup < 2.000000) and (mo_occup > 0.000001):
                    cas_mos_data.extend(mo_raw_data)

    return molden_header, cas_mos_data

def write_molden(_arguments, _molden_header, _molden_data):
    """_summary_

    Args:
        _arguments {obj} -- arguments given by user
        _molden_header (list): Header of original Molden file
        _molden_data (list): Active space orbitals selected
    """

    molden_output_filename = "cas."+_arguments.molden_filename

    with open(molden_output_filename, 'w') as file:
        for line in _molden_header:
            file.write(line)
        for line in _molden_data:
            file.write(line)

# Main program
if __name__ == '__main__':

    # Obtaining arguments from terminal
    arguments = get_arguments()

    # Reading Molden File
    molden_raw_file = open_molden_file(arguments)

    # Formatting Molden File removing unoccupied and full-occupied MOs
    molden_header, molden_cas_data = format_molden_file(molden_raw_file)

    # Writing Molden File
    write_molden(arguments, molden_header, molden_cas_data)

    # End of get_molden_active_space.py execution
    print_script_output(
        '> Molden File from {} sucessfully processed!'.format(arguments.molden_filename),
        'job_done')