from fhir.resources.patient import Patient as FHIRPatient
from fhir.resources.identifier import Identifier
from fhir.resources.contactpoint import ContactPoint
from fhir.resources.humanname import HumanName
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.address import Address

#############################
## Patient class
#############################
class Patient:
    id_system = 'study_internal_id'
    remote_id = None
    resource = None
    print_json = False

    def __init__(self, data, data_type):
        if data_type == "csv":
            self.parse_csv(data)
        else:
            self.parse_json(data)

    def parse_json(self, data):
        self.resource = FHIRPatient.parse_obj(data)
        self.remote_id = data["id"]

    def parse_csv(self, data_dict):
        ## Create a blank FHIR Patient
        self.resource = FHIRPatient()

        ## Set the study internal identifier to find the correct patient again
        self.resource.identifier = [Identifier(system=self.id_system,
                                               value=data_dict["Id"])]

        ## Set date of birth
        self.resource.birthDate = data_dict['BIRTHDATE']

        ## Set telephone number
        self.resource.telecom = [ContactPoint(system='phone', value=data_dict['PHONE'])]

        ## Set name
        name = HumanName()
        name.family = data_dict['LAST']
        name.given=[data_dict['FIRST']]
        self.resource.name = [name]

        ## Set marital status
        code = "M" if data_dict['MARITAL'] == 'M' else 'UNK'
        code_text = "Married" if data_dict['MARITAL'] == 'M' else 'unknown'
        self.resource.maritalStatus = CodeableConcept()
        self.resource.maritalStatus.text = code_text
        self.resource.maritalStatus.coding=[{
            'system': 'http://terminology.hl7.org/CodeSystem/v3-MaritalStatus',
            'code': code
        }]

        ## Set gender
        self.resource.gender = 'male' if data_dict['GENDER'] == 'M' else 'female'

        ## Set address
        address = dict()
        if 'CITY' in data_dict.keys():
            address['city'] = data_dict['CITY']
        if 'COUNTY' in data_dict.keys():
            address['district'] = data_dict['COUNTY']
        if 'STATE' in data_dict.keys():
            address['state'] = data_dict['STATE']
        if 'ADDRESS' in data_dict.keys():
            address['line'] = [data_dict['ADDRESS']]
        if 'ZIP' in data_dict.keys():
            address['postalCode'] = str(data_dict['ZIP'])
        if len(address) != 0:
            self.resource.address = [Address.parse_obj(address)]

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
        remote_resource = server.get_by_id('Patient', self.id_system, id)
        if remote_resource is None:
            self.upload(server)
            print('Uploaded: ', end='')
        else:
            self.parse_json(remote_resource)
            print('Retrieved: ', end='')
        print(self)

    @staticmethod
    def get_all_remote_resources(server):
        print('Collect Patient resources...', end='')
        resources_dict = server.get_bundle('Patient')
        print('sort...', end='')
        resources = {}
        for r in resources_dict:
            r = Patient(r, 'json')
            i = r.get_id()
            resources[i] = r
            print(r)
        print('done')
        return resources

    @staticmethod
    def delete_all_remote_resources(server):
        res = Patient.get_all_remote_resources(server)
        for r in res.values():
            print('Delete: ', end='')
            r.print_json = False
            print(r)
            server.delete(r)

    def __str__(self):
        id = self.resource.identifier[0].value
        f = self.resource.name[0].family
        g = self.resource.name[0].given
        if self.print_json:
            json = self.resource.json()
            return(f"Patient [{id}]({self.remote_id}):\t{json}")
        else:
            return(f"Patient [{id}]({self.remote_id}):\t{f}, {g[0]}")


