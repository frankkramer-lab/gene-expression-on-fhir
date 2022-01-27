#!/bin/bash
cd data_processing

## Installing virtualenv
python3 -m pip install --user virtualenv
## Creating a virtual environment
python3 -m venv env
source env/bin/activate

## create and upload data
python run.py -e ../data/experiment-design.tsv -p ../data/dummy_patients.csv -g ../data/Homo_sapiens.GRCh38.99.chr.gff3.gz -ge ../data/normalized-expressions.tsv update

## verify remote resources
venv/bin/python run.py count

## return to parent directory
cd ..
