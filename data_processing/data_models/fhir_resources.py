from fhir.resources.patient import Patient as FHIRPatient
from fhir.resources.organization import Organization as FHIROrganization
from fhir.resources.encounter import Encounter as FHIREncounter

from fhir.resources.identifier import Identifier

from fhir.resources.fhirdate import FHIRDate
from fhir.resources.contactpoint import ContactPoint
from fhir.resources.humanname import HumanName
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.address import Address
from fhir.resources.coding import Coding
from fhir.resources.period import Period
from fhir.resources.fhirreference import FHIRReference



#############################
## Patient class
#############################

class Patient:
    remote_id = None
    resource = None

    def __init__(self, data_dict, data_type):
        if data_type == 'json':
            self.parse_json(data_dict)
        elif data_type == 'csv':
            self.parse_csv(data_dict)
        else:
            raise TypeError('type must be either "csv" or "json"!')

    def parse_json(self, data_dict):
        self.remote_id = data_dict['id']
        self.resource = FHIRPatient(data_dict)


    def parse_csv(self, data_dict):
        self.resource = FHIRPatient()

        ## Set date of birth
        if 'BIRTHDATE' in data_dict.keys():
            self.resource.birthDate = FHIRDate(data_dict['BIRTHDATE'])

        ## Set date of death
        if 'DEATHDATE' in data_dict.keys():
            self.resource.deceasedDateTime = FHIRDate(data_dict['DEATHDATE'])

        ## Set telephone number
        if 'PHONE' in data_dict.keys():
            self.resource.telecom = [ContactPoint(dict(system='phone', value=data_dict['PHONE']))]

        ## Set name
        name = dict(family=data_dict['LAST'], given=[data_dict['FIRST']])
        if 'PREFIX' in data_dict.keys():
            name['prefix'] = [data_dict['PREFIX']]
        if 'SUFFIX' in data_dict.keys():
            name['suffix'] = [data_dict['SUFFIX']]
        self.resource.name = [HumanName(name)]

        ## Set marital status
        if 'MARITAL' in data_dict.keys():
            code_text = "Married" if data_dict['MARITAL'] == 'M' else 'Single'
            self.resource.maritalStatus = CodeableConcept(dict(coding=[dict(system='http://terminology.hl7.org/CodeSystem/v3-MaritalStatus',
                                                                            code=data_dict['MARITAL'])],
                                                               text=code_text))

        ## Set gender
        if 'GENDER' in data_dict.keys():
            self.resource.gender = 'male' if data_dict['GENDER'] == 'M' else 'female'

        ## Set address
        address = dict()
        if 'CITY' in data_dict.keys():
            address['city'] = data_dict['CITY']
        if 'STATE' in data_dict.keys():
            address['state'] = data_dict['STATE']
        if 'ADDRESS' in data_dict.keys():
            address['line'] = [data_dict['ADDRESS']]
        if 'ZIP' in data_dict.keys():
            address['postalCode'] = str(data_dict['ZIP'])
        if len(address) != 0:
            self.resource.address = [Address(address)]

        #print(self.resource.as_json())

    def set_submitter(self, submitter):
        self.resource.identifier = [Identifier(dict(system="submitter",
                                                    value=submitter))]

    ## Upload a Patient to the FHIR server
    def upload(self, server):
        server.upload(self)



    ## Delete a Patient at the FHIR server
    def delete(self, server):
        server.delete(self)

    def to_string(self):
        result = self.resource.name[0].given[0] + ' ' + self.resource.name[0].family
        if 'prefix' in vars(self.resource.name[0]) and self.resource.name[0].prefix is not None:
            result = self.resource.name[0].prefix[0] + ' ' + result
        if 'suffix' in vars(self.resource.name[0]) and self.resource.name[0].suffix is not None:
            result = result + ' ' + self.resource.name[0].suffix[0]
        result = 'PAT: ' + result + ' (' + str(self.remote_id) + ')'
        return result


#############################
## Organization class
#############################

class Organization:
    remote_id = None
    resource = None

    def __init__(self, data_dict, data_type):
        if data_type == 'json':
            self.parse_json(data_dict)
        elif data_type == 'csv':
            self.parse_csv(data_dict)
        else:
            raise ValueError('type must be either "csv" or "json"!')

    def parse_json(self, data_dict):
        self.remote_id = data_dict['id']
        self.resource = FHIROrganization(data_dict)


    def parse_csv(self, data_dict):
        self.resource = FHIROrganization()

        ## Set name
        self.resource.name = data_dict['NAME']

        ## Set address
        address = dict()
        if 'CITY' in data_dict.keys():
            address['city'] = data_dict['CITY']
        if 'STATE' in data_dict.keys():
            address['state'] = data_dict['STATE']
        if 'ADDRESS' in data_dict.keys():
            address['line'] = [data_dict['ADDRESS']]
        if 'ZIP' in data_dict.keys():
            address['postalCode'] = str(data_dict['ZIP'])
        if len(address) != 0:
            self.resource.address = [Address(address)]


    def set_submitter(self, submitter):
        self.resource.identifier = [Identifier(dict(system="submitter",
                                                    value=submitter))]


    ## Upload a Organization to the FHIR server
    def upload(self, server):
        server.upload(self)



    ## Delete a Organization at the FHIR server
    def delete(self, server):
        server.delete(self)


    def to_string(self):
        result = self.resource.name + ' in ' + self.resource.address[0].city
        result = 'ORG: ' + result + ' (' + str(self.remote_id) + ')'
        return result


#############################
## Encounter class
#############################

class Encounter:
    remote_id = None
    resource = None

    def __init__(self, data_dict, data_type, patients=None, organizations=None):
        if data_type == 'json':
            self.parse_json(data_dict)
        elif data_type == 'csv':
            self.parse_csv(data_dict, patients, organizations)
        else:
            raise TypeError('type must be either "csv" or "json"!')

    def parse_json(self, data_dict):
        self.remote_id = data_dict['id']
        self.resource = FHIREncounter(data_dict)


    def parse_csv(self, data_dict, patients, organizations):
        self.resource = FHIREncounter()
        if patients is None:
            raise TypeError('patients has to be set!')
        if organizations is None:
            raise TypeError('organizations has to be set!')

        self.resource.status = 'finished'   # Hint in exer

        encounter_classes = dict(emergency='EMER',
                                 inpatient='IMP',
                                 ambulatory='AMB',
                                 outpatient='AMB')     # Hint in exerc
        self.resource.class_fhir = Coding(dict(system='http://terminology.hl7.org/ValueSet/v3-ActEncounterCode',
                                               code=encounter_classes[data_dict['ENCOUNTERCLASS']]))

        self.resource.period = Period(dict(start=data_dict['START'],
                                           end=data_dict['STOP']))

        coding = [dict(system="http://hl7.org/fhir/ValueSet/icd-10",
                       code=data_dict['code'],
                       display=data_dict['ICD10-CM'])]

        self.resource.reasonCode = [CodeableConcept(dict(coding=coding))]

        patient = patients[data_dict['PATIENT']]
        self.resource.subject = FHIRReference(dict(reference='Patient/' + patient.remote_id))

        organization = organizations[data_dict['PROVIDER']]
        self.resource.serviceProvider = FHIRReference(dict(reference='Organization/' + organization.remote_id))

        # print(self.resource.as_json())


    def set_submitter(self, submitter):
        self.resource.identifier = [Identifier(dict(system="submitter",
                                                    value=submitter))]

    ## Upload a Encounter to the FHIR server
    def upload(self, server):
        server.upload(self)


    ## Delete a Encounter at the FHIR server
    def delete(self, server):
        server.delete(self)


    def to_string(self):
        p_id = self.resource.subject.reference.split('/')[1]
        o_id = self.resource.serviceProvider.reference.split('/')[1]
        result = 'ENC: Treatment(' + self.remote_id + ') of ' + self.resource.reasonCode[0].coding[0].display + ' [' + self.resource.class_fhir.code + '] for patient(' + p_id + ') by organization(' + o_id + ')'
        return result

