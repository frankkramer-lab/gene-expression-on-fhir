# Gene Expression on FHIR

This repository contains an implementation of gene expression profiles from biopsy samples for several patients in Fast Healthcare Interoperability Resources (FHIR).
It demonstrates how this kind of molecular genetic data can be encoded in FHIR resources and subsequently worked with using the a FHIR server as source for displaying the data in a web application.

## Gene expression data

The data set examines a dose-limiting side effect in patients diagnosed with acute myeloid leukemia (AML) that are treated with chemotherapy. 
In particular mucositis, a DNA damage within the oral mucosa caused by the chemotherapy is investigated based on the derived gene expression profiles. 
The samples are collected from punch buccal biopsies from five AML patients pre- and post-chemotherapy, and three healthy controls for comparison.

> J.-L. C. Mougeot, F. K. Bahrani-Mougeot, P. B. Lockhart, and M. T. Brennan, “Microarray analyses of oral punch biopsies from acute myeloid leukemia (AML) patients treated with chemotherapy,” Oral Surgery, Oral Medicine, Oral Pathology, Oral Radiology, and Endodontology, vol. 112, no. 4, pp. 446–452, Oct. 2011, https://doi.org/10.1016/j.tripleo.2011.05.009.

The authors made the data available at the EBI Expression Atlas portal by the ID [E-GEOD-10746](https://www.ebi.ac.uk/arrayexpress/experiments/E-GEOD-10746/).

We chose this gene expression data set because the conducted analysis represents a typical bioinformatics workflow resulting in several gene expression profiles from the same and different individuals that enable disease classification and patient stratification into risk groups.

## Reference genome

Microarray analysis was performed using [Human Genome U133 Plus 2.0 Array](https://www.thermofisher.com/order/catalog/product/900466) with [GRCh38.p13 (Genome Reference Consortium Human Build 38, Ensembl release 99)](https://www.ncbi.nlm.nih.gov/assembly/GCF_000001405.26/) as reference, followed by a Robust Multichip Average (RMA) normalization of the raw data. 
Subsequently Linear Models for Microarray data (LIMMA) and Significance Analysis of Microarrays (SAM) was applied to identified genes potentially affected by the presence of AML, or predictive of oral mucositis after chemotherapy.

## Patient data

Detailed information about the sample donors was not included in the original data set to preserve anonymity of the participants, instead we used artificially generated data using [Synthea<sup>TM</sup>](https://github.com/synthetichealth/synthea) to create Patient resources as reference.

# Components
## FHIR server
This project contains a dockerized version of the [HAPI FHIR server](https://github.com/hapifhir/hapi-fhir-jpaserver-starter) which serves as a repository for the created FHIR resources.
The HAPI FHIR server is a free and open source Java implementation of the [HL7 FHIR](http://hl7.org/fhir/) standard.
It includes a RESTful API to access and manage the resources, as well as validation of the submitted data.

The FHIR server wasn't modified to demonstrate the usage of FHIR resources for handling gene expression data on the plane standard definition.
The sources for the customization can be found in the `HAPI-FHIR-server` directory and the `docker-init.sh` script can be used to setup the docker container for the FHIR server.

## Data download

The `data` directory only contains synthetically generated patient data required for generating FHIR *Patient* reference resources.
Additional data can be downloaded from the official repositories:
- Homo sapiens (human) reference genome used in the gene expression analysis and for creating *MolecularSequence* resources
  http://ftp.ensembl.org/pub/release-99/gff3/homo_sapiens/Homo_sapiens.GRCh38.99.chr.gff3.gz
- Sample donor information about patient status and the moment the sample was taken, which is the used to create *Condition* and *Specimen* resources
  https://www.ebi.ac.uk/gxa/experiments-content/E-GEOD-10746/resources/ExperimentDesignFile.Microarray/experiment-design
- Normalized gene expression table used to create the single *Observations*
  https://www.ebi.ac.uk/gxa/experiments-content/E-GEOD-10746/resources/DifferentialSecondaryDataFiles.Microarray/normalized-expressions
  
 Alternatively the provided `data-download.sh` script can be used to download all necessary data.
 
## Python scripts

This python scripts can be used to parse the downloaded source data and upload the generated resources the FHIR server.
The source data is parced using the packages `numpy` and `pandas`, and create the FHIR resources using the [fhir.resources](https://pypi.org/project/fhir.resources/) package.
The source code can be found in the `data_processing` directory.

The script can be run as follows to show the help message:

```
python run.py --help

>usage: run.py [-h] [-s FHIR_SERVER_ENDPOINT] [-e EXPERIMENT_DESIGN_FILE] [-p PATIENTS_FILE] [-g GFF3_FILE] [-ge GENE_EXPRESSION_FILE] {parse,update,delete,count} ...
>
>Gene expression data transformation with FHIR
>
>positional arguments:
>  {parse,update,delete,count}
>                        sub-command help
>    parse               Just parse the data files.
>    update              Read the data from the csv files, then upload the resources or retrieve their remote ids
>    delete              Delete all remote resources
>    count               Count all remote resources
>
>optional arguments:
>  -h, --help            show this help message and exit
>  -s FHIR_SERVER_ENDPOINT, --server FHIR_SERVER_ENDPOINT
>                        This is the base URL of FHIR server.
>  -e EXPERIMENT_DESIGN_FILE, --experiment-design EXPERIMENT_DESIGN_FILE
>                        Experiment design data.
>  -p PATIENTS_FILE, --patients PATIENTS_FILE
>                        Patient information.
>  -g GFF3_FILE, --gff3 GFF3_FILE
>                        Reference genome data in gff3 format.
>  -ge GENE_EXPRESSION_FILE, --gene-expression GENE_EXPRESSION_FILE
>                        Gene expression data.
```

### parse

Just parse the csv files: For testing if the data can be processed, no data is uploaded yet!
This requires the files provided by the parameters: `-e`, `-p`, `-g` and `-ge`

### update

Again the data from the csv files is parsed. 
When the resources do not exist on the server they will be uploaded.
Otherwise if the resources already exist on the FHIR server (i.e. they match by the `identifier` property) their remote ids will be retrieved and displayed.
This requires the files and the fhir server endpoint specified by the parameters.

### count

Shows the different remote fhir resources and corresponding counts avalable at the server.
Only requires the fhir server endpoint specified.

**Note:** This does not work directly after upload for some reason. 
Maybe the HAPI server need some time to index the resources before beeing available by this parameter.
An overview of the resources is provided by the `http://localhost:8080/fhir/$get-resource-counts` endpoint.

### delete

Delete all, or just certain resources on the server.
This can help to resolve issues if there occured some errors while data upload, and resetting the server therefore is necessary.
This requires only the fhir server endpoint, and optionally the resources to delete, i.e. `all`, `patients`, `conditions`, `specimens`, `molecularsequences`, or  `observations`.

## Web application
The web application uses the FHIR resources directly from the FHIR server.
Its source code can be found in the `web-app` directory.
It is implemented using the [Angular](https://angular.io/) framework and [Bootstrap 4.6](https://getbootstrap.com/) for decoration.
For demonstration purposes some sample data is included, so that the web application also works without a connection to a FHIR server.
This sample data only consists of an excerpt of the total resources, therefore the functionality is limited.

There are two compiled versions of the web application within this repository:
### Local setup
In the `web-app/dist/GEonFHIRlocal/` directory is compiled version for the usage in a local setup.
The website can be hosted either using a simple web server, or python:

```
## within web-app/dist/GEonFHIRlocal/
python -m http.server 8081
```
or using docker:

```
docker run -dit \
	-p 8081:80 \
	--name ge-on-fhir-http \
	httpd:2.4

docker cp web-app/dist/GEonFHIRlocal/. ge-on-fhir-http:/usr/local/apache2/htdocs/
```
Alternatively, the provided script `docker-ttpd.sh` can be used to setup the web application in a docker container.

### Github Pages
Within the `dist` directory a compiled version of the web application can be found, which is used for hosting on Githup Pages.
It can be tried at https://frankkramer-lab.github.io/gene-expression-on-fhir/

# Setup
## Requirements

The setup requires some software to be installed:
### Docker
The container management software Docker (https://www.docker.com/) needs to be installed.
For the installation see https://docs.docker.com/engine/install/

To run the provided scripts it is also necessary to be able to run `docker` as user.
Otherwise the single steps have to be performed one by one using the `docker-init-with-sudo.sh` (or run `sudo ./setup.sh` which is not recomended).

### Python
To run the fhir upload scripts it is required to have python 3 installed (tested with python 3.8).
Also the module for virtual environments needs to be installed.
Both can be installed with

```
sudo apt install python3.8 python3.8-venv
```

The scripts also need the packages `pandas`, `numpy` and `fhir.resources` to be installed.
Generally it is a good way to install the packages within a virtual environment.
To create a virtual environment use the following:
```
python3 -m venv venv
```
Before usage, the python environment has to be activated:

```
## within data_processing/
source venv/bin/activate
```
Afterwards the script can be run.

### Angular (optional)
To work with angular to modify the web application Angular needs to be installed.
How to install Angular can be found here: https://angular.io/guide/setup-local

Afterwards the web application can be compiled using:
```
ng build --configuration production
```

## Run setup

A script for setting up all required software components is provided with `setup.sh`.
It runs the single above mentioned scripts to setup everything at once. 
Simply run:
```
./setup.sh
```








