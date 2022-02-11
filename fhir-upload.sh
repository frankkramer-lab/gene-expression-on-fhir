#!/bin/bash

echo "Process and upload data to FHIR server:"
cd data_processing

## Installing virtualenv
echo "Install python virtual environment..." 
/usr/bin/python3 -m pip install --user virtualenv

## Creating a virtual environment
echo "Init virtual environment..."
/usr/bin/python3 -m venv venv
source venv/bin/activate

## Install fhir.resources
echo "Install python packages..."
python -m pip install pandas numpy fhir.resources

## create and upload data
echo "Create and upload data..."
python run.py -e ../data/experiment-design.tsv -p ../data/dummy_patients.csv -g ../data/Homo_sapiens.GRCh38.99.chr.gff3.gz -ge ../data/normalized-expressions.tsv update

## verify remote resources
## does not work directly after upload
#echo "Verify remote resources..."
#python run.py count

## return to parent directory
cd ..
