from data_models.patient import Patient
from data_models.condition import Condition
from data_models.specimen import Specimen
from data_models.observation import Observation
from data_models.molecular_sequence import MolecularSequence

import pandas as pd

class Bundle:
    resource_type = None
    resources = None

    def __init__(self, resource_type, data, data_type='csv', patients=None, specimens=None, molecularSequences=None):
        self.resource_type = resource_type
        if data_type == 'csv':
            self.parse_csv(resource_type, data, patients, specimens, molecularSequences)
        else:
            self.parse_csv(data)

    def parse_csv(self, resource_type, data, patients=None, specimens=None, molecularSequences=None):
        self.resources = {}
        if resource_type == 'Patient':
            for index, row in data.iterrows():
                self.resources[row["Id"]] = Patient(row, 'csv')
        elif resource_type == 'Condition':
            disease = data[data['disease'] != 'normal']
            for index, row in disease.iterrows():
                self.resources[row["individual"]] = Condition(row, 'csv', patients)
        elif resource_type == 'Specimen':
            for index, row in data.iterrows():
                self.resources[row["sample"]] = Specimen(row, 'csv', patients)
        elif resource_type == 'MolecularSequence':
            for index, row in data.iterrows():
                self.resources[row["gene_id"]] = MolecularSequence(row, 'csv')
        elif resource_type == 'Observation':
            for index, row in data.iterrows():
                for sk, sv in specimens.resources.items():
                    self.resources[sk + ':' + row['Gene ID']] = Observation(row, 'csv',
                                                                            patients = patients,
                                                                            specimens = specimens,
                                                                            specimenId = sk,
                                                                            molecularSequences = molecularSequences)

    def upload(self, server):
        for res in self.resources.values():
            res.upload(server)

    def update(self, server, print_json=False):
        for res in self.resources.values():
            res.print_json = print_json
            res.update(server)

    def print(self, print_json=False):
        print(f'Bundle of: {self.resource_type}')
        for r in self.resources.values():
            r.print_json = print_json
            print(r)
