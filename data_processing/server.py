import urllib.request
import urllib.parse
import json
from data_models.patient import Patient
from data_models.observation import Observation
from data_models.molecular_sequence import MolecularSequence

class FHIR_server:
    def __init__(self, fhir_server_endpoint):
        if not fhir_server_endpoint.endswith('/'):
            fhir_server_endpoint += '/'
        self.fhir_server_endpoint = fhir_server_endpoint

    def get_all_patients(self):
        results = []
        for p in self.get_bundle('Patient'):
            results.append(Patient(p, data_type="json"))
        return results

    def get_all_observations(self):
        results = []
        for p in self.get_bundle('Observation'):
            results.append(Observation(p, data_type="json"))
        return results

    def get_all_molecularsequences(self):
        results = []
        for p in self.get_bundle('MolecularSequence'):
            results.append(MolecularSequence(p, data_type="json"))
        return results

    def get_patient_observations(self, id):
        results = []
        for p in self.get_bundle_patient_observations("Observation", id):
            results.append(Observation(p, data_type="json"))
        return results

    def search_patients(self):
        results = []
        for p in self.get_search('Patient'):
            results.append(Patient(p, data_type="json"))
        return results

    def search_molecularsequences(self, search):
        results = []
        for p in self.get_search("MolecularSequence", search):
            results.append(MolecularSequence(p, data_type="json"))
        return results

    def get_bundle(self, resource_name):
        next_link = self.fhir_server_endpoint + resource_name + '?identifier=submitter|' + self.submitter
        results = []
        while next_link is not None:
            req = urllib.request.Request(next_link)
            response = urllib.request.urlopen(req)
            remote_records = json.loads(response.read().decode('utf8'))
            next_link = None
            for e in remote_records.get('link', []):
                if e['relation'] == 'next':
                    next_link = e['url']
            if 'entry' in remote_records:
                for e in remote_records['entry']:
                    results.append(e['resource'])
        return results

    def get_bundle_patient_observations(self, resource_name, patient_id):
        next_link = self.fhir_server_endpoint + resource_name + '?subject=' + patient_id
        results = []
        while next_link is not None:
            req = urllib.request.Request(next_link)
            response = urllib.request.urlopen(req)
            remote_records = json.loads(response.read().decode('utf8'))
            next_link = None
            for e in remote_records.get('link', []):
                if e['relation'] == 'next':
                    next_link = e['url']
            if 'entry' in remote_records:
                for e in remote_records['entry']:
                    results.append(e['resource'])
        return results

    def get_by_id(self, resource_name, system, id):
        url = self.fhir_server_endpoint + resource_name
        param = '?identifier=' + urllib.parse.quote_plus(system + '|' + id)
        req = urllib.request.Request(url+param)
        response = urllib.request.urlopen(req)
        bundle = json.loads(response.read().decode('utf8'))
        res = None
        if bundle['total'] > 1:
            res =  bundle['entry'][0]['resource']
        return res


    def upload(self, resource_object):
        resource_class = type(resource_object).__name__
        if resource_class not in ['Patient', 'Condition', 'Observation', 'MolecularSequence', 'Specimen']:
            raise TypeError('resource must be one of Patient, Observation or MolecularSequence')

        data = resource_object.resource.json().encode('utf8')

        req = urllib.request.Request(self.fhir_server_endpoint + resource_class,
                                     data=data,
                                     headers={'content-type': 'application/fhir+json'})
        response = urllib.request.urlopen(req)
        response = json.loads(response.read().decode('utf8'))
        ## return the remote id
        resource_object.parse_json(response)
        # resource_object.remote_id = response['id']

    def get_bundle(self, resource_name):
        next_link = self.fhir_server_endpoint + resource_name
        results = []
        while next_link is not None:
            req = urllib.request.Request(next_link)
            response = urllib.request.urlopen(req)
            remote_records = json.loads(response.read().decode('utf8'))
            next_link = None
            for e in remote_records.get('link', []):
                if e['relation'] == 'next':
                    next_link = e['url']
            if 'entry' in remote_records:
                for e in remote_records['entry']:
                    results.append(e['resource'])
        return results


    def delete(self, resource_object):
        resource_class = type(resource_object).__name__
        if resource_class not in ['Patient', 'Condition', 'Observation', 'MolecularSequence', 'Specimen']:
            raise TypeError('resource must be one of Patient, Observation or MolecularSequence')
        if resource_object.remote_id is not None:
            url = self.fhir_server_endpoint + resource_class + '/' + resource_object.remote_id
            req = urllib.request.Request(url,
                                         method='DELETE')
            urllib.request.urlopen(req)
            resource_object.remote_id = None


    def get_search(self, resource_name, search):
        next_link = self.fhir_server_endpoint + resource_name + search
        results = []
        while next_link is not None:
            req = urllib.request.Request(next_link)
            response = urllib.request.urlopen(req)
            remote_records = json.loads(response.read().decode('utf8'))
            next_link = None
            for e in remote_records.get('link', []):
                if e['relation'] == 'next':
                    next_link = e['url']
            if 'entry' in remote_records:
                for e in remote_records['entry']:
                    results.append(e['resource'])
        return results

    def get_resource_count(self):
        url = self.fhir_server_endpoint+'$get-resource-counts'
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        bundle = json.loads(response.read().decode('utf8'))
        result = {}
        for e in bundle['parameter']:
            result[e['name']] = e['valueInteger']
        return result
