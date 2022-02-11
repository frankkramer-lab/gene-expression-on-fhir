import argparse

from data_models.condition import Condition
from data_models.molecular_sequence import MolecularSequence
from data_models.observation import Observation
from data_models.specimen import Specimen
from data_models.patient import Patient
from server import FHIR_server
from study import Study

##########################################
## Example calls of the program
##########################################

## venv/bin/python data_processing/run.py -e ../data/experiment-design.tsv -p ../data/dummy_patients.csv -g ../data/Homo_sapiens.GRCh38.99.chr.gff3.gz -ge ../data/normalized-expressions.tsv parse
## venv/bin/python data_processing/run.py -e ../data/experiment-design.tsv -p ../data/dummy_patients.csv -g ../data/Homo_sapiens.GRCh38.99.chr.gff3.gz -ge ../data/normalized-expressions.tsv update
## venv/bin/python data_processing/run.py update
## venv/bin/python data_processing/run.py count

##########################################
## Implement Argument Parser
##########################################


parser = argparse.ArgumentParser(description="Gene expression data transformation with FHIR")
parser.add_argument("-s", "--server", action="store", dest="fhir_server_endpoint",
                    type=str, default="http://localhost:8080/fhir/",
                    help="This is the base URL of FHIR server.")
parser.add_argument("-e", "--experiment-design", action="store", dest="experiment_design_file",
                    type=str, default="experiment-design.tsv",
                    help="Experiment design data.")
parser.add_argument("-p", "--patients", action="store", dest="patients_file",
                    type=str, default="dummy_patients.csv",
                    help="Patient information.")
parser.add_argument("-g", "--gff3", action="store", dest="gff3_file",
                    type=str, default="Homo_sapiens.GRCh38.99.chr.gff3.gz",
                    help="Reference genome data in gff3 format.")
parser.add_argument("-ge", "--gene-expression", action="store", dest="gene_expression_file",
                    type=str, default="normalized-expressions.tsv",
                    help="Gene expression data.")

subparsers = parser.add_subparsers(help='sub-command help', dest='command')

## parse
parser_parse = subparsers.add_parser('parse',
                                    help='Just parse the data files.')
parser_parse.add_argument("show_data", type=str, default="all", const='all', nargs='?',
                         choices=['all', 'experiment-design', 'patients', 'gff3', 'gene-expression'],
                         help="Which parsed data should be shown.")

## update
parser_update = subparsers.add_parser('update',
                                     help='Read the data from the csv files, then upload the resources or retrieve their remote ids')
parser_update.add_argument("--print-full", action="store_true", dest="print_full",
                           help="Also print the JSON data of the resource.")

## delete
parser_delete = subparsers.add_parser('delete',
                                      help='Delete all remote resources')

parser_delete.add_argument("resources", type=str, default="all", const='all', nargs='?',
                         choices=['all', 'patients', 'conditions', 'specimens', 'molecularsequences',  'observations'],
                         help="Which resources should be deleted (patients also deletes conditions, specimens and observations; specimens and molecularsequences also deletes observations)")

## count
parser_delete = subparsers.add_parser('count',
                                      help='Count all remote resources')


#############################
## Parse data
#############################

def parse_resources(experiment_design_file,
                    patients_file,
                    gff3_file,
                    gene_expression_file,
                    show_data):
    # server = FHIR_server(fhir_server_endpoint)
    print('Parse files:')
    study = None
    if(show_data == 'all'):
        study = Study(study_design_file=experiment_design_file,
                      ge_file=gene_expression_file,
                      patient_file=patients_file,
                      gff3_file=gff3_file)
        print("Experiment design:")
        print(study.study_raw)
        print("\nPatients:")
        print(study.patients_raw)
        print("\nGFF3:")
        print(study.gff3_raw.head(10))
        print("\nGene expression:")
        print(study.ge_raw.head(10))
    elif (show_data == 'experiment-design'):
        study = Study(study_design_file=experiment_design_file)
        print("Experiment design:")
        print(study.study_raw)
    elif (show_data == 'patients'):
        study = Study(patient_file=patients_file)
        print("\nPatients:")
        print(study.patients_raw)
    elif (show_data == 'gff3'):
        study = Study(gff3_file=gff3_file)
        print("\nGFF3:")
        print(study.gff3_raw.head(10))
    elif (show_data == 'gene-expression'):
        study = Study(ge_file=gene_expression_file)
        print("\nGene expression:")
        print(study.ge_raw.head(10))
    return(study)

#############################
## Process CSVs and upload
#############################

def update_resources(fhir_server_endpoint,
                     experiment_design_file,
                     patients_file,
                     gff3_file,
                     gene_expression_file,
                     print_full):
    server = FHIR_server(fhir_server_endpoint)
    study = parse_resources(experiment_design_file,
                            patients_file,
                            gff3_file,
                            gene_expression_file,
                            'all')

    print("Create Patient resources...", end='')
    study.create_patients()
    print('done')
    study.patients.update(server, print_full)

    print("Create Condition resources:", end='')
    study.create_conditions()
    print('done')
    study.condition.update(server, print_full)

    print("Create Specimen resources:", end='')
    study.create_specimens()
    print('done')
    study.specimens.update(server, print_full)

    print("Create MolecularSequence resources:", end='')
    study.create_molecular_sequence()
    print('done')
    study.molecular_sequences.update(server, print_full)

    print("Create Observation resources:", end='')
    study.create_observation()
    print('done')
    study.observation.update(server, print_full)


#############################
## Delete uploaded data
#############################

def delete_resources(fhir_server_endpoint,
                     resources):
    # server = FHIR_server(fhir_server_endpoint)
    print('Delete all remote resources:')
    server = FHIR_server(fhir_server_endpoint)

    # (patients also deletes conditions, specimens and observations;
    #  specimens and molecularsequences also deletes observations)
    if(resources == 'all'):
        print("Delete Observation resources:")
        Observation.delete_all_remote_resources(server)

        print("Delete Specimen resources:")
        Specimen.delete_all_remote_resources(server)

        print("Delete Condition resources:")
        Condition.delete_all_remote_resources(server)

        print("Delete Patient resources:")
        Patient.delete_all_remote_resources(server)


    elif (resources == 'patients'):
        print("Delete Observation resources:")
        Observation.delete_all_remote_resources(server)

        print("Delete Specimen resources:")
        Specimen.delete_all_remote_resources(server)

        print("Delete Condition resources:")
        Condition.delete_all_remote_resources(server)

        print("Delete Patient resources:")
        Patient.delete_all_remote_resources(server)

        print("Delete MolecularSequence resources:")
        MolecularSequence.delete_all_remote_resources(server)

    elif (resources == 'conditions'):
        print("Delete Condition resources:")
        Condition.delete_all_remote_resources(server)
    elif (resources == 'specimens'):
        print("Delete Observation resources:")
        Observation.delete_all_remote_resources(server)

        print("Delete Specimen resources:")
        Specimen.delete_all_remote_resources(server)
    elif (resources == 'molecularsequences'):
        print("Delete Observation resources:")
        Observation.delete_all_remote_resources(server)

        print("Delete MolecularSequence resources:")
        MolecularSequence.delete_all_remote_resources(server)
    elif (resources == 'observations'):
        print("Delete Observation resources:")
        Observation.delete_all_remote_resources(server)


##########################################
## Parse args
##########################################
args = parser.parse_args()

fhir_server_endpoint = args.fhir_server_endpoint
experiment_design_file = args.experiment_design_file
patients_file = args.patients_file
gff3_file = args.gff3_file
gene_expression_file = args.gene_expression_file

if args.command == 'parse':
    parse_resources(experiment_design_file = args.experiment_design_file,
                    patients_file = args.patients_file,
                    gff3_file = args.gff3_file,
                    gene_expression_file = args.gene_expression_file,
                    show_data = args.show_data)
elif args.command == 'update':
    print('Parse and update resources...')
    update_resources(fhir_server_endpoint=args.fhir_server_endpoint,
                     experiment_design_file=args.experiment_design_file,
                     patients_file=args.patients_file,
                     gff3_file=args.gff3_file,
                     gene_expression_file=args.gene_expression_file,
                     print_full=args.print_full)
elif args.command == 'delete':
    print('Delete remote resources...')
    delete_resources(fhir_server_endpoint=args.fhir_server_endpoint,
                     resources=args.resources)
elif args.command == 'count':
    print('Get remote resources count...', end='')
    server = FHIR_server(fhir_server_endpoint)
    resources = server.get_resource_count()
    print('done:')
    for k, v in resources.items():
        print(f'{k}: {v}')

