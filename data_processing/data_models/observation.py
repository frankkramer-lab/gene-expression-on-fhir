from fhir.resources.reference import Reference
from fhir.resources.patient import Patient as FHIRPatient
from fhir.resources.observation import Observation as FHIRObservation
from fhir.resources.molecularsequence import MolecularSequence as FHIRMolecularSequence
from fhir.resources.molecularsequence import MolecularSequenceVariant as FHIRMolecularSequenceVariant
from fhir.resources.molecularsequence import MolecularSequenceReferenceSeq as FHIRMolecularSequenceReferenceSeq
from fhir.resources.identifier import Identifier
from fhir.resources.reference import Reference as FHIRReference
import pandas as pd

#############################
## Observation class
#############################
class Observation:
    id_system = 'study_internal_id'
    remote_id = None
    resource = None
    print_json = False

    def __init__(self, data, data_type, patients=None, specimens=None, specimenId=None, molecularSequences=None):
        if data_type == "csv":
            self.parse_csv(data, patients, specimens, specimenId, molecularSequences)
        else:
            self.parse_json(data)

    def parse_json(self, data):
        self.resource = FHIRObservation.parse_obj(data)
        self.remote_id = data["id"]

    def parse_csv(self, data, patients, specimens, specimenId, molecularSequences):
        # df2 = pd.read_csv("data/gene_names_with_codes.csv")
        # gene_name = data["Gene_Name"]
        # value = data[f"{patientKey}"]
        # if not df2[df2["Gene_Name"] == f"{gene_name}"].empty:
        #     hgnc_code = df2[df2["Gene_Name"] == f"{gene_name}"].iloc[0]["Gene_Code"]
        #     extension_coding = [
        #         {
        #             "url": "http://hl7.org/fhir/StructureDefinition/observation-geneticsGene",
        #             "valueCodeableConcept": {
        #                 "coding": [
        #                         {
        #                             "system": "https://www.genenames.org",
        #                             "code": f"{hgnc_code}",
        #                             "display": f"{gene_name}"
        #                         }
        #                 ],
        #                 "text": f"{gene_name}"
        #             }
        #         }
        #     ]
        # else:
        #     extension_coding = [
        #         {
        #             "url": "http://hl7.org/fhir/StructureDefinition/observation-geneticsGene",
        #             "valueCodeableConcept": {
        #                 "coding": [],
        #                 "text": f"{gene_name}"
        #             }
        #         }
        #     ]
        # obs_json = {
        #         "resourceType": "Observation",
        #         "extension": extension_coding,
        #         "status": "final",
        #         "code": {
        #             "text": f"normalized value for {gene_name}"
        #         },
        #         "subject": {
        #             "reference": f"Patient/{patientRef.remote_id}",
        #             "display": f"Patient: {patientKey}"
        #         },
        #         "derivedFrom": [{
        #             "reference": f"MolecularSequence/{molSeqRef}",
        #             "type": "MolecularSequence"
        #         }],
        #         "valueString": f"{value}"
        #
        # }
        # print(data)
        observation = {'status': 'final',
                       'extension': [{
                           "url": "http://hl7.org/fhir/StructureDefinition/observation-geneticsGene",
                           "valueCodeableConcept": {
                               "coding": [{
                                   "system": "https://www.genenames.org",
                                   "code": data['Gene Name'],
                                   "display": data['Gene Name']}]
                           }}],
                       'code': {
                           'coding': [{
                               'system': "http://hl7.org/fhir/ValueSet/observation-codes",
                               'code': '48018-6',
                               'display': 'Gene studied'}]}
                       }
        self.resource = FHIRObservation.parse_obj(observation)

        self.resource.identifier = [Identifier(system=self.id_system,
                                             value=specimenId+':'+data['Gene ID'])]

        self.resource.subject = FHIRReference()
        self.resource.subject.reference = specimens.resources[specimenId].resource.subject.reference

        self.resource.specimen = FHIRReference()
        self.resource.specimen.reference = 'Specimen/'+str(specimens.resources[specimenId].remote_id)

        derived = FHIRReference()
        derived.reference = 'MolecularSequence/'+str(molecularSequences.resources[data['Gene ID']].remote_id)
        self.resource.derivedFrom = [derived]
        ## 8.04957732029089
        ## x*10E6
        self.resource.valueInteger = round(data[specimenId]*1000000)

    def get_id(self):
        id = None
        for i in self.resource.identifier:
            if i.system == self.id_system:
                id = i.value
        return id

    ## Upload a Organization to the FHIR server
    def upload(self, server):
        server.upload(self)

    ## Update with remote resource
    def update(self, server):
        id = self.get_id()
        remote_resource = server.get_by_id('Observation', self.id_system, id)
        if remote_resource is None:
            self.upload(server)
            print('Uploaded: ', end='')
        else:
            self.parse_json(remote_resource)
            print('Retrieved: ', end='')
        print(self)

    ## Delete a Organization at the FHIR server
    def delete(self, server):
        server.delete(self)

    @staticmethod
    def get_all_remote_resources(server):
        print('Collect Observation resources...',end='')
        resources_dict = server.get_bundle('Observation')
        print('sort...',end='')
        resources = {}
        for r in resources_dict:
            r = Observation(r, 'json')
            i = r.get_id()
            resources[i] = r
        print('done')
        return resources

    @staticmethod
    def delete_all_remote_resources(server):
        res = Observation.get_all_remote_resources(server)
        for r in res.values():
            print('Delete: ', end='')
            r.print_json = False
            print(r)
            server.delete(r)

    def __str__(self):
        id = self.get_id()
        if self.print_json:
            json = self.resource.json()
            return (f"Observation [{id}]({self.remote_id}):\t{json}")
        else:
            return (f"Observation [{id}]({self.remote_id})")

# Unique types in GFF
dict_so = {
    'pseudogene': 'SO:0000336',
    'chromosome': 'SO:0000340',
    'biological_region': 'SO:0001411',
    'lnc_RNA': 'SO:0001877',
    'exon': 'SO:0000147',
    'pseudogenic_transcript': 'SO:0000516',
    'ncRNA_gene': 'SO:0001263',
    'miRNA': 'SO:0000276',
    'gene': 'SO:0000704',
    'mRNA': 'SO:0000234',
    'five_prime_UTR': 'SO:0000204',
    'CDS': 'SO:0000316',
    'three_prime_UTR': 'SO:0000205',
    'snRNA': 'SO:0000274',
    'ncRNA': 'SO:0000655',
    'unconfirmed_transcript': '	SO:0002139',
    'snoRNA': 'SO:0000275',
    'scRNA': 'SO:0000013',
    'rRNA': 'SO:0000252',
    'V_gene_segment': '	SO:0000466',
    'D_gene_segment': '	SO:0000466',
    'J_gene_segment': 'SO:0000470',
    'C_gene_segment': 'SO:0000478',
    'tRNA': 'SO:0000253'
}
