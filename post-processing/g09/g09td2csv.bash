#!/bin/bash

### g09td2csv
### Script to obtain transition energies and intensities from Gaussian09 TD calculation
### Export data in CSV (Comma-Separated Values)
### Grupo de Espectroscopia Teórica e Modelagem Molecular - GETMM (IQ/UFRJ)
### Author Carlos Eduardo Vieira de Moura : carlosevmoura@iq.ufrj.br

###############################
#### Variables Definitions ####
###############################

## Log complete filename with extension
LogFile=$1

###################
#### Functions ####
###################

## CheckingInputFile function
function CheckingInputFile {
if [ -n "$LogFile" ]; then
	if [ ! -f "$LogFile" ]; then
		echo -e "\033[01;31m$1 Gaussian09 log file was not found.\033[00m"
		exit 1
	fi
else
	echo -e "Usage: g09td2csv [Gaussian09 log file]"
	exit 1
fi

if grep -q "Normal termination of Gaussian 09" "$LogFile"; then
    if grep -q "Excited State" "$LogFile"; then		
		LogName=$(basename "$LogFile")
		LogName="${LogName%.*}"
    fi
else
	echo -e "\033[01;31mGaussian09 log aren't from TD type. End of script execution.\033[00m"
	exit 1
fi
}

## BuildingCSVfile function
function BuildingCSVfile {
	# Obtaining TD data from log file
	grep "Excited State" $LogFile |awk '{print $5}' > .energy.temp
	grep "Excited State" $LogFile |awk '{print $9}'|cut -f 2 -d '=' > .oos.temp
	
	# Building CSV File
	touch $LogName.td.csv
	echo "Transition Energy (eV),Oscillator Strength" > $LogName.td.csv
	paste -d "," .energy.temp .oos.temp >> $LogName.td.csv

	# Removing temporary files
	rm -f .energy.temp .oos.temp
}

## FinishingScript function
function FinishingScript {
	echo -e "\033[01;32m$LogName.td.csv preview:\033[00m"
	cat $LogName.td.csv
	echo -e "\033[01;32mg09td2csv was sucesfully executed.\033[00m"	
}

#####################
#### Main Script ####
#####################

## Checking Gaussian09 log file
CheckingInputFile

## Building CSV file
BuildingCSVfile

## Finishing script
FinishingScript
