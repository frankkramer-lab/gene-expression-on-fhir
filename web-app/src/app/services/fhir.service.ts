import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable, Subscriber, throwError} from 'rxjs';
import {catchError, concat, expand, first, map, pluck, retry, tap, toArray, take, mergeMap} from 'rxjs/operators';
import {Patient} from '../models/patient';
import {Bundle} from '../models/bundle';
import {forkJoin} from 'rxjs/internal/observable/forkJoin';
import {Specimen} from '../models/specimen';
import {MolecularSequence} from '../models/molecular-sequence';
import {of} from 'rxjs/internal/observable/of';
import {ServerStatus} from '../models/server-status';

@Injectable({
  providedIn: 'root'
})
export class FhirService {

  fhirEndpoint: string | undefined;
  defaultFhirEndpoint = 'http://localhost:8080/fhir/';

  mockDir = 'assets/data/';

  constructor(private http: HttpClient) { }

  setFhirEndpoint(fhirEndpoint: string): Observable<ServerStatus> {
    this.fhirEndpoint = fhirEndpoint;
    return this.http.get<Observable<ServerStatus>>(this.fhirEndpoint + '$meta').pipe(
      catchError(err => of({resourceType: 'Error'})),
      map(data => new ServerStatus(data, fhirEndpoint))
    );
  }

  initServerStatus(): void {
    if (this.fhirEndpoint === undefined) {
      this.fhirEndpoint = this.defaultFhirEndpoint;
    }
  }

  getServerStatus(): Observable<ServerStatus> {
    this.initServerStatus();
    return this.http.get<Observable<ServerStatus>>(this.fhirEndpoint + '$meta').pipe(
      catchError(err => of({resourceType: 'Error'})),
      map(data => new ServerStatus(data, this.fhirEndpoint))
    );
  }

//   test.subscribe(
//     res => this.serverAvailable = true,
//   error => this.serverAvailable = false
// );

  getPatientById(id: number): Observable<Patient> {
    return this.getServerStatus().pipe(
      mergeMap( status => {
        const url = status.status ? this.fhirEndpoint + 'Patient/' + id : this.mockDir + 'patients/Patient-' + id + '.json';
        return this.http.get<Observable<Patient>>(url).pipe(
          map(data => new Patient(data))
        );
      })
    );
  }

  // getPatients(): Observable<Bundle> {
  //   return this.http.get<Observable<Bundle>>(this.fhirEndpoint + 'Patient').pipe(
  //     map(data => new Bundle(data, 'Patient'))
  //   );
  // }

  getPatients(): Observable<Bundle> {
    return this.getServerStatus().pipe(
      mergeMap( status => {
        const url = status.status ? this.fhirEndpoint + 'Patient/' : this.mockDir + 'Patients.json';
        return this.http.get<Observable<Bundle>>(url).pipe(
          map(data => new Bundle(data, 'Patient'))
        );
      })
    );
  }

  getConditions(): Observable<Bundle> {
    return this.getServerStatus().pipe(
      mergeMap( status => {
        const url = status.status ? this.fhirEndpoint + 'Condition' : this.mockDir + 'Conditions.json';
        return this.http.get<Observable<Bundle>>(url).pipe(
          map(data => new Bundle(data, 'Condition'))
        );
      })
    );
  }

  // GET http://localhost:8080/fhir/Specimen?subject=Patient/1
  getSpecimensByPatient(patientId: number): Observable<Bundle> {
    return this.getServerStatus().pipe(
      mergeMap( status => {
        let url = '';
        if (status.status) {
          url = this.fhirEndpoint + 'Specimen?subject=Patient%2F' + patientId;
        } else {
          url = this.mockDir + 'specimens/Specimen-' + patientId + '.json';
        }
        return this.http.get<Observable<Bundle>>(url).pipe(
          map(data => new Bundle(data, 'Specimen'))
        );
      })
    );
  }

  getSpecimens(): Observable<Bundle> {
    return this.getServerStatus().pipe(
      mergeMap( status => {
        const url = status.status ? this.fhirEndpoint + 'Specimen' : this.mockDir + 'Specimens.json';
        return this.http.get<Observable<Bundle>>(url).pipe(
          map(data => new Bundle(data, 'Specimen'))
        );
      })
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
    return this.getServerStatus().pipe(
      mergeMap( status => {
        let url = this.fhirEndpoint + 'Observation?derived-from=' + molecularSequenceId;
        if (status.status) {
          if (patientId >= 0) {
            url += '&subject=' + patientId;
          }
        } else {
          if (patientId >= 0) {
            url = this.mockDir + 'observations/Observation-' + molecularSequenceId + '-' + patientId + '.json';
          } else {
            url = this.mockDir + 'observations/Observation-' + molecularSequenceId + '.json';
          }
        }
        return this.http.get<Observable<Bundle>>(url).pipe(
          map(data => new Bundle(data, 'Observation'))
        );
      })
    );
  }

  getMolecularSequences(offset = 0, count = 12, isGeneSymbol = true, searchTerms = []): Observable<Bundle> {
    return this.getServerStatus().pipe(
      mergeMap( status => {
        let url = this.fhirEndpoint + 'MolecularSequence?_count=' + count + '&_getpagesoffset=' + offset * count;
        if (status.status) {
          if (searchTerms.length !== 0){
            url += isGeneSymbol ? '&identifier=gene_symbol%7C' : '&identifier=ensemble_id%7C';
            url += searchTerms.join('%2C');
          }
        } else {
          url = this.mockDir + 'MolecularSequences.json';
        }

        return this.http.get<Observable<Bundle>>(url).pipe(
          map(data => new Bundle(data, 'MolecularSequence'))
        );
      })
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


