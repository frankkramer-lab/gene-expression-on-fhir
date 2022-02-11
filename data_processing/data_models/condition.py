from fhir.resources.condition import Condition as FHIRCondition
from fhir.resources.identifier import Identifier
from fhir.resources.reference import Reference as FHIRReference
from fhir.resources.codeableconcept import CodeableConcept


#############################
## Condition class
#############################
class Condition:
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
        self.resource = FHIRCondition.parse_obj(data)
        self.remote_id = data["id"]

    def parse_csv(self, data_dict, patients):
        resource = {}

        ## Set the study internal identifier to find the correct patient again
        resource['identifier'] = [Identifier(system=self.id_system,
                                             value=data_dict["individual"])]

        ## Set patient reference
        subject = FHIRReference()
        subject.reference='Patient/' + patients.resources[data_dict['individual']].remote_id
        resource['subject'] = subject

        coding = CodeableConcept()
        coding.coding = [{'system': "http://fhir.de/ValueSet/bfarm/icd-10-gm",
                    'code': '2A60.3',
                    'display': 'Acute myeloid leukaemia, not elsewhere classified by criteria of other types'}]
        resource['code'] = coding

        self.resource = FHIRCondition.parse_obj(resource)


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
        remote_resource = server.get_by_id('Condition', self.id_system, id)
        if remote_resource is None:
            self.upload(server)
            print('Uploaded: ', end='')
        else:
            self.parse_json(remote_resource)
            print('Retrieved: ', end='')
        print(self)

    @staticmethod
    def get_all_remote_resources(server):
        print('Collect Condition resources...', end='')
        resources_dict = server.get_bundle('Condition')
        print('sort...', end='')
        resources = {}
        for r in resources_dict:
            r = Condition(r, 'json')
            i = r.get_id()
            resources[i] = r
            print(r)
        print('done')
        return resources

    @staticmethod
    def delete_all_remote_resources(server):
        res = Condition.get_all_remote_resources(server)
        for r in res.values():
            print('Delete: ', end='')
            r.print_json = False
            print(r)
            server.delete(r)

    def __str__(self):
        if self.print_json:
            return(f"Condition [{self.get_id()}]({self.remote_id}):\t{self.resource.code.json()}")
        else:
            return(f"Condition [{self.get_id()}]({self.remote_id})")
