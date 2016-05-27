#!/bin/bash

### nxspectrum2csv
### Script to obtain transition energies and intensities from Nuclear Ensemble calculations in Newton-X
### Export data in CSV (Comma-Separated Values)
### Grupo de Espectroscopia Teórica e Modelagem Molecular - GETMM (IQ/UFRJ)
### Author Carlos Eduardo Vieira de Moura : carlosevmoura@iq.ufrj.br

#### Variables Definitions ####
## Default filename of cross-section results
CrossSectionFile="cross-section.dat"

#### Functions ####
## CheckingInputFile function
function CheckingInputFile {
	# Checking if cross-section file exists
	if [ ! -f "$CrossSectionFile" ]; then
		echo -e "Usage (at cross-section.dat containing folder): nxspectrum2csv"
		echo -e "\033[01;31m$1cross-section file was not found.\033[00m"
		exit 1
	fi

	# Checking if cross-section file contains correct data
	if ! grep -q "DE/eV    lambda/nm    sigma/A^2        +/-error/A^2" "$CrossSectionFile"; then
		echo -e "\033[01;31mCross-section file is not from Newton-X. End of script execution.\033[00m"
		exit 1
	fi
}

## BuildingCrossSectionCSV function
function BuildingCrossSectionCSV {
	awk '{print $1}' $CrossSectionFile > .energy.temp
	awk '{print $3}' $CrossSectionFile > .oos.temp
	paste -d "," .energy.temp .oos.temp > cross-section.csv
	rm -f .energy.temp .oos.temp
}

#### Main Script ####
## Checking Newton-X cross-section file
CheckingInputFile

## Building spectrum data from cross-section file
BuildingCrossSectionCSV

## Finishing script
echo -e "\033[01;32mnxspectrum2csv was sucesfully executed.\033[00m"
