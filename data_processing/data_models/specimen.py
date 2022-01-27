from fhir.resources.specimen import Specimen as FHIRSpecimen
from fhir.resources.identifier import Identifier
from fhir.resources.reference import Reference as FHIRReference
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.annotation import Annotation


#############################
## Specimen class
#############################
class Specimen:
    id_system = 'study_internal_id'
    remote_id = None
    resource = None
    print_json = False

    def __init__(self, data, data_type, patients = None):
        if data_type == "csv":
            self.parse_csv(data, patients)
        else:
            self.parse_json(data)

    def parse_json(self, data):
        self.resource = FHIRSpecimen.parse_obj(data)
        self.remote_id = data["id"]

    def parse_csv(self, data_dict, patients):
        resource = {}

        ## Set the study internal identifier to find the correct patient again
        resource['identifier'] = [Identifier(system=self.id_system,
                                             value=data_dict["sample"])]
        resource['accessionIdentifier'] = Identifier(system=self.id_system,
                                                    value=data_dict["sample"])

        ## Set patient reference
        subject = FHIRReference()
        subject.reference='Patient/' + patients.resources[data_dict['individual']].remote_id
        resource['subject'] = subject

        self.resource = FHIRSpecimen.parse_obj(resource)

        type = CodeableConcept()
        type.coding = [{'system': "http://terminology.hl7.org/CodeSystem/v2-0487",
                    'code': 'BX',
                    'display': 'Biopsy'}]
        self.resource.type = type

        self.resource.receivedTime = '2008-03-06' if data_dict['treatment'] == 'two days post-chemotherapy' else '2008-03-04'
        self.resource.note = [Annotation(text=data_dict['treatment'])]


    def get_id(self):
        id = None
        for i in self.resource.identifier:
            if i.system == self.id_system:
                id = i.value
        return id

    ## Upload a Patient to the FHIR server
    def upload(self, server):
        server.upload(self)

    ## Update with remote resource
    def update(self, server):
        id = self.get_id()
        remote_resource = server.get_by_id('Specimen', self.id_system, id)
        if remote_resource is None:
            self.upload(server)
            print('Uploaded: ', end='')
        else:
            self.parse_json(remote_resource)
            print('Retrieved: ', end='')
        print(self)

    @staticmethod
    def get_all_remote_resources(server):
        print('Collect Specimen resources...', end='')
        resources_dict = server.get_bundle('Specimen')
        print('sort...', end='')
        resources = {}
        for r in resources_dict:
            r = Specimen(r, 'json')
            i = r.get_id()
            resources[i] = r
            print(r)
        print('done')
        return resources

    @staticmethod
    def delete_all_remote_resources(server):
        res = Specimen.get_all_remote_resources(server)
        for r in res.values():
            print('Delete: ', end='')
            r.print_json = False
            print(r)
            server.delete(r)

    def __str__(self):
        id = self.resource.accessionIdentifier.value
        if self.print_json:
            return(f"Specimen [{id}]({self.remote_id}):\t{self.resource.type.json()}")
        else:
            return (f"Specimen [{id}]({self.remote_id})")
