#!/bin/bash

### g09nto2mo
### Script to edit an Gaussian09 NTO output file to format which can be read by softwares, like ChemCraft
### Needs both NTO calculation and common TD log files
### Use in TD calculation: gfinput Pop=Full
### Use in NTO calculation: gfinput Pop=Minimal
### Grupo de Espectroscopia Teórica e Modelagem Molecular - GETMM (IQ/UFRJ)
### Author Carlos Eduardo Vieira de Moura : carlosevmoura@iq.ufrj.br

###############################
#### Variables Definitions ####
###############################

## Log complete filename with extension
MOFile=$1
NTOFile=$2

###################
#### Functions ####
###################

## CheckingInputFile function
function CheckingInputFile {
if [ -n "$NTOFile" ]; then
	if [ ! -f "$NTOFile" ]; then
		echo -e "\033[01;31m$1 Gaussian09 log file was not found.\033[00m"
		exit 1
	fi
else
	echo -e "Usage: g09nto2mo [Gaussian09 TD log file] [Gaussian09 NTO log file]"
	exit 1
fi

if grep -q "Normal termination of Gaussian 09" "$MOFile"; then
    if grep -q "Excited State" "$MOFile"; then        
		if grep -q "Normal termination of Gaussian 09" "$NTOFile"; then
		    if grep -q "Natural Transition Orbitals" "$NTOFile"; then       
		        LogName=$(basename "$NTOFile")
		        LogName="${LogName%.*}"
		    fi
		else
		    echo -e "\033[01;31mGaussian09 log aren't from NTO type. End of script execution.\033[00m"
		    exit 1
		fi
    fi
else
	echo -e "\033[01;31mGaussian09 log aren't from TD type. End of script execution.\033[00m"
	exit 1
fi
}



## BuildingNTOfile function
function BuildingNTOfile {
	# Obtaining orbitals line numbers from log files

	NTOStartLine=`grep -n "Alpha spin Natural Transition Orbitals for state" $NTOFile |cut -d ':' -f 1`
	NTOEndLine=`grep -n "Populations using transition density between ground and state" $NTOFile |cut -d ':' -f 1`
	
	MOStartLine=`grep -n "Molecular Orbital Coefficients" $MOFile |cut -d ':' -f 1`
	MOEndLine=`grep -n "Density Matrix" $MOFile |cut -d ':' -f 1`

	# Building Readable log File	
	touch $LogName.nto.log
	
	sed -n "1, $MOStartLine p" $MOFile >> $LogName.nto.log
    sed -n "$NTOStartLine, $(( $NTOEndLine - 3 )) p" $NTOFile >> $LogName.nto.log
    sed -n "$MOEndLine,$ p" $MOFile >> $LogName.nto.log

}

## FinishingScript function
function FinishingScript {
	echo -e "\033[01;32mg09nto2mo was sucesfully executed.\033[00m"	
}

#####################
#### Main Script ####
#####################

## Checking Gaussian09 log file
CheckingInputFile

## Building readable NTO log file
BuildingNTOfile

## Finishing script
FinishingScript
