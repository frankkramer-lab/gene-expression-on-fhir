import json

import pandas as pd
import numpy as np

from data_models.patient import Patient
from data_models.bundle import Bundle
from gff3 import gff3

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option('display.width', None)
np.set_printoptions(linewidth = None)

class Study():
    study_columns = {'Assay': 'sample',
                    'Sample Characteristic[individual]': 'individual',
                     'Sample Characteristic[disease]': 'disease',
                     'Sample Characteristic[clinical treatment]': 'treatment'}

    def __init__(self, study_design_file=None, ge_file=None, patient_file=None, gff3_file=None):
        ## Patients
        if patient_file is not None:
            print(f'Reading patient information file ( {study_design_file} )...', end='')
            patients_type = {'Id': str,
                             'BIRTHDATE': str,
                             'PHONE': str,
                             'PREFIX': str,
                             'FIRST': str,
                             'LAST': str,
                             'MAIDEN': str,
                             'MARITAL': str,
                             'RACE': str,
                             'ETHNICITY': str,
                             'GENDER': str,
                             'ADDRESS': str,
                             'CITY': str,
                             'STATE': str,
                             'COUNTY': str,
                             'ZIP': str,
                             'HEALTHCARE_EXPENSES': float,
            }
            self.patients_raw = pd.read_csv(patient_file, dtype=patients_type, parse_dates=['BIRTHDATE'])
            print('done')

        ## Study
        if study_design_file is not None:
            print(f'Reading experiment design file ( {study_design_file} )...', end='')
            self.study_raw = pd.read_csv(study_design_file, sep='\t', encoding_errors='ignore')
            self.study_raw = self.study_raw[self.study_columns.keys()]
            self.study_raw.rename(columns=self.study_columns, inplace=True)
            self.study_raw['individual'] = self.study_raw['individual'].map(
                lambda i: 'Control ' + i[5:6] if i.startswith("BRENC") else 'Patient ' + i[4:5])
            print('done')

        ## Gene Expression
        if ge_file is not None:
            print(f'Reading gene expression file ( {study_design_file} )...', end='')
            self.ge_raw = pd.read_csv(ge_file, sep='\t', encoding_errors='ignore')
            print('done')

        ## gff3
        if gff3_file is not None:
            self.gff3_raw = gff3(gff3_file).data

    ## create a bundle of Patients
    def create_patients(self):
        self.patients = Bundle('Patient', self.patients_raw)

    ## create a bundle of Conditions
    def create_conditions(self):
        self.condition = Bundle('Condition', self.study_raw, patients=self.patients)

    ## create a bundle of Specimen
    def create_specimens(self):
        self.specimens = Bundle('Specimen', self.study_raw, patients=self.patients)

    ## create a bundle of gff3s
    def create_molecular_sequence(self):
        geids = self.ge_raw['Gene ID'].dropna()
        gff3_genes = self.gff3_raw[self.gff3_raw['gene_id'].isin(geids)]
        self.molecular_sequences = Bundle('MolecularSequence', gff3_genes)

    ## create a bundle of gff3s
    def create_observation(self):
        self.observation = Bundle('Observation', self.ge_raw,
                                  patients = self.patients,
                                  specimens=self.specimens,
                                  molecularSequences=self.molecular_sequences)

    def get_patient_resources(self):
        patients = {}
        for index, row in self.patients.iterrows():
            patients[row["Id"]] = Patient(row, data_type="csv")
        return patients


# STUDY = '../data/experiment-design.tsv'
# GE = '../data/normalized-expressions.tsv'
# PATIENT = '../data/dummy_patients.csv'
# s = Study(STUDY, GE, PATIENT)
#
# print("Study:")
# print(s.study)
# print("\nPatients:")
# print(s.patients)
# for p in s.get_patient_resources().values():
#     data = p.resource.dict()
#     data = json.dumps(data).encode('utf8')
#     print(data)
#
# print("\nGene expression:")
# print(s.ge.head(10))
