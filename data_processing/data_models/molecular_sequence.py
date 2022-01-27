from fhir.resources.reference import Reference
from fhir.resources.patient import Patient as FHIRPatient
from fhir.resources.observation import Observation as FHIRObservation
from fhir.resources.molecularsequence import MolecularSequence as FHIRMolecularSequence
from fhir.resources.molecularsequence import MolecularSequenceVariant as FHIRMolecularSequenceVariant
from fhir.resources.molecularsequence import MolecularSequenceReferenceSeq as FHIRMolecularSequenceReferenceSeq
from fhir.resources.identifier import Identifier
from fhir.resources.codeableconcept import CodeableConcept
import pandas as pd

#############################
## Molecular Sequence
#############################
class MolecularSequence:
    id_system = 'ensemble_id'
    remote_id = None
    resource = None
    print_json = False

    # Unique types in GFF
    cigar_dict = {
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

    def __init__(self, data, data_type, chromosome=None):
        if data_type == "csv":
            self.parse_csv(data, chromosome)
        # elif data_type == 'chromosome':
        #     self.parse_chromosome(data)
        else:
            self.parse_json(data)


    def parse_json(self, data):
        self.resource = FHIRMolecularSequence.parse_obj(data)
        self.remote_id = data["id"]

    # def parse_chromosome(self, data):
    #     self.resource = FHIRMolecularSequence.parse_obj({'coordianteSystem': 1})
    #     self.resource.genomeBuild: 'GRCh38.p13'
    #
    #     chromosome = CodeableConcept()
    #     chromosome.coding = [{'system': "http://hl7.org/fhir/ValueSet/chromosome-human",
    #                           'code': data['seqid'],
    #                           'display': 'chromosome ' + data['seqid']}]
    #     self.resource.referenceSeq.chromosome = chromosome
    #
    #     type = CodeableConcept()
    #     type.coding = [{'system': "http://hl7.org/fhir/ValueSet/sequence-type",
    #                     'code': 'dna',
    #                     'display': 'DNA Sequence'}]
    #     self.resource.type = type
    #
    #     self.resource.repository = [{
    #         'type': 'directlink',
    #         'url': 'http://ftp.ensembl.org/pub/release-99/gff3/homo_sapiens/Homo_sapiens.GRCh38.99.chromosome.'+chromosome+'.gff3.gz',
    #         'name': 'Genome Reference Consortium Human Build 38 p13 Ensembl 99: Jan 2020'
    #     }]

    def parse_csv(self, data, chromosome):
        ## create chromosomes
        # for c in data['seqid'].unique():

        ## then genes referencing the chromosomes
        # seqid #
        # source
        # type  #
        # start #
        # end   #
        # strand    #
        # ID = gene:ENSG....    #
        # name
        # biotype
        # description
        # gene_id   #
        # logic_name
        # version

        self.resource = FHIRMolecularSequence.parse_obj({"coordinateSystem": 1})

        self.resource.identifier = [Identifier(system=self.id_system,
                                               value=data["gene_id"]),
                                    Identifier(system='gene_symbol',
                                               value=data["Name"])]

        # type = CodeableConcept()
        # type.coding = [{'system': "http://hl7.org/fhir/ValueSet/sequence-type",
        #                 'code': 'dna',
        #                 'display': 'DNA Sequence'}]
        self.resource.type = 'dna'

        chromosome = CodeableConcept()
        chromosome.coding = [{'system': "http://hl7.org/fhir/ValueSet/chromosome-human",
                              'code': data['seqid'],
                              'display': 'chromosome ' + data['seqid']}]
        self.resource.referenceSeq = FHIRMolecularSequenceReferenceSeq()
        self.resource.referenceSeq.chromosome = chromosome

        self.resource.referenceSeq.orientation = 'sense' if data['strand'] == '+' else 'antisense'

        refseqId = CodeableConcept()
        refseqId.coding = [{'system': 'http://hl7.org/fhir/ValueSet/sequence-referenceSeq',
                            'code': data['gene_id'],
                            'display': data['ID']}]
        self.resource.referenceSeq.referenceSeqId = refseqId

        self.resource.referenceSeq.windowStart = data['start']
        self.resource.referenceSeq.windowEnd = data['end']

        self.resource.repository = [{
            'type': 'directlink',
            'url': 'https://www.ensembl.org/Homo_sapiens/Gene/Summary?db=core;g='+data['gene_id'],
            'name': 'Ensembl database'
        }]


    def get_id(self):
        id = None
        for i in self.resource.identifier:
            if i.system == self.id_system:
                id = i.value
        return id

    ## Upload a Molecular Sequence to the FHIR server
    def upload(self, server):
        server.upload(self)

    ## Update with remote resource
    def update(self, server):
        id = self.get_id()
        remote_resource = server.get_by_id('MolecularSequence', self.id_system, id)
        if remote_resource is None:
            self.upload(server)
            print('Uploaded: ',end='')
        else:
            self.parse_json(remote_resource)
            print('Retrieved: ', end='')
        print(self)

    @staticmethod
    def get_all_remote_resources(server):
        print('Collect MolecularSequence resources...', end='')
        resources_dict = server.get_bundle('MolecularSequence')
        print('sort...', end='')
        resources = {}
        for r in resources_dict:
            r = MolecularSequence(r, 'json')
            i = r.get_id()
            resources[i] = r
            print(r)
        print('done')
        return resources

    @staticmethod
    def delete_all_remote_resources(server):
        res = MolecularSequence.get_all_remote_resources(server)
        for r in res.values():
            print('Delete: ', end='')
            r.print_json = False
            print(r)
            server.delete(r)

    def __str__(self):
        if self.print_json:
            return(f"MolecularSequence [{self.get_id()}]({self.remote_id}):\t{self.resource.json()}")
        else:
            return(f"MolecularSequence [{self.get_id()}]({self.remote_id})")

#Uploaded: Observation [Mucositis-BRENC3:ENSG00000288573](252684)