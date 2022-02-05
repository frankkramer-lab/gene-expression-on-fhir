#!/bin/bash

## download reference genome in gff3 format
## Genome Reference Consortium Human Build 38 release 99
## Homo sapiens (human)
curl http://ftp.ensembl.org/pub/release-99/gff3/homo_sapiens/Homo_sapiens.GRCh38.99.chr.gff3.gz --output data/Homo_sapiens.GRCh38.99.chr.gff3.gz

## https://www.ebi.ac.uk/arrayexpress/experiments/E-GEOD-10746/
## https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE10746
## donor information
curl https://www.ebi.ac.uk/gxa/experiments-content/E-GEOD-10746/resources/ExperimentDesignFile.Microarray/experiment-design --output data/experiment-design.tsv
## gene expression data set
curl https://www.ebi.ac.uk/gxa/experiments-content/E-GEOD-10746/resources/DifferentialSecondaryDataFiles.Microarray/normalized-expressions --output data/normalized-expressions.tsv

