import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable, Subscriber, throwError} from 'rxjs';
import {catchError, concat, expand, first, map, pluck, retry, tap, toArray, take} from 'rxjs/operators';
import {Patient} from '../models/patient';
import {Bundle} from '../models/bundle';
import {forkJoin} from 'rxjs/internal/observable/forkJoin';
import {Specimen} from '../models/specimen';
import {MolecularSequence} from '../models/molecular-sequence';

@Injectable({
  providedIn: 'root'
})
export class FhirService {

  fhirEndpoint = 'http://localhost:8080/fhir/';

  constructor(private http: HttpClient) { }

  getPatientById(id: number): Observable<Patient> {
    return this.http.get<Observable<Patient>>(this.fhirEndpoint + 'Patient/' + id).pipe(
      map(data => new Patient(data))
    );
  }

  getPatients(): Observable<Bundle> {
    return this.http.get<Observable<Bundle>>(this.fhirEndpoint + 'Patient').pipe(
      map(data => new Bundle(data, 'Patient'))
    );
  }

  getConditions(): Observable<Bundle> {
    return this.http.get<Observable<Bundle>>(this.fhirEndpoint + 'Condition').pipe(
      map(data => new Bundle(data, 'Condition'))
    );
  }

  // GET http://localhost:8080/fhir/Specimen?subject=Patient/1
  getSpecimensByPatient(patientId: number): Observable<Bundle> {
    const url = this.fhirEndpoint + 'Specimen?subject=Patient%2F' + patientId;
    return this.http.get<Observable<Bundle>>(url).pipe(
      map(data => new Bundle(data, 'Specimen'))
    );
  }

  getSpecimens(): Observable<Bundle> {
    return this.http.get<Observable<Bundle>>(this.fhirEndpoint + 'Specimen').pipe(
      map(data => new Bundle(data, 'Specimen'))
    );
  }

  getObservations(): Observable<Bundle> {
    return this.http.get<Observable<Bundle>>(this.fhirEndpoint + 'Observation').pipe(
      map(data => new Bundle(data, 'Observation'))
    );
  }

  getObservationsByReference(molecularSequenceId: number, patientId = -1): Observable<Bundle> {
    // derivedFrom MolecularSequence/20717
    // subject Patient/1
    // http://localhost:8080/fhir/Observation?derived-from=20717&subject=2&_pretty=true
    let url = this.fhirEndpoint + 'Observation?derived-from=' + molecularSequenceId;
    if (patientId >= 0) {
      url += '&subject=' + patientId;
    }
    return this.http.get<Observable<Bundle>>(url).pipe(
      map(data => new Bundle(data, 'Observation'))
    );
  }

  getMolecularSequences(offset = 0, count = 12, isGeneSymbol = true, searchTerms = []): Observable<Bundle> {
    let url = this.fhirEndpoint + 'MolecularSequence?_count=' + count + '&_getpagesoffset=' + offset * count;
    if (searchTerms.length !== 0){
      url += isGeneSymbol ? '&identifier=gene_symbol%7C' : '&identifier=ensemble_id%7C';
      url += searchTerms.join('%2C');
    }
    console.log(url);
    return this.http.get<Observable<Bundle>>(url).pipe(
      map(data => new Bundle(data, 'MolecularSequence'))
    );
  }

  getPCSMS(): Observable<{patients: Bundle, conditions: Bundle, specimens: Bundle}> {
    return forkJoin({
      patients: this.getPatients(),
      conditions: this.getConditions(),
      specimens: this.getSpecimens()
    });
  }
}


