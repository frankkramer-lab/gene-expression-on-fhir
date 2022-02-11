
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

## Run setup

A script for setting up all required software components is provided with `setup.sh`.
Simply run:
```
./setup.sh
```

Firstly, the required data is downloaded from the public servers into the `data` directory.
This can alternatively done with the `data-download.sh` script.

## Docker

https://github.com/hapifhir/hapi-fhir-jpaserver-starter


## Python scripts

This python scripts can be used to manage data on the FHIR server.

Firstly, the python environment has to be activated, so that all required packages are installed:

```
## within data_processing/
source venv/bin/activate
```

Now the script can be run as follows to show the help message:

```python run.py --help```

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

### parse

Just parse the csv files, no data is uploaded!
This requires the files provided by the parameters: `-e`, `-p`, `-g` and `-ge`

### update

Again the data from the csv files is parsed. When the resources do not exist on the server they will be uploaded, otherwise their remote ids will be retrieved and displayed.
This requires the files and the fhir server endpoint specified by the parameters.

### count

Shows the different remote fhir resources and corresponding counts avalable at the server.
Only requires the fhir server endpoint specified.

Note: This does not work directly after upload for some reason. 
An overview of the resources is provided by the http://localhost:8080/fhir/$get-resource-counts endpoint.
For some reason this does not work always.
Maybe the HAPI server need some time to index the resources before beeing available by this parameter.


