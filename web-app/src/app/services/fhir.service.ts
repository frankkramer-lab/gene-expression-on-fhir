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

  //GET http://localhost:8080/fhir/Specimen?subject=Patient/1
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

  getObservationsByReference(molecularSequenceId: number, patientId: number): Observable<Bundle> {
    // derivedFrom MolecularSequence/20717
    // subject Patient/1
    // http://localhost:8080/fhir/Observation?derived-from=20717&subject=2&_pretty=true
    const url = this.fhirEndpoint + 'Observation?derived-from=' + molecularSequenceId + '&subject=' + patientId;
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

  // getMolecularSequences(offset = 0, count = 12): Observable<Bundle> {
  //   const url = this.fhirEndpoint + 'MolecularSequence?_count=' + count + '&_getpagesoffset=' + offset * count;
  //   console.log(url);
  //   return this.http.get<Observable<Bundle>>(url).pipe(
  //     map(data => new Bundle(data, 'MolecularSequence'))
  //   );
  // }


  getPCSMS() {
    return forkJoin({
      patients: this.getPatients(),
      conditions: this.getConditions(),
      specimens: this.getSpecimens(),
      molecularSequences: this.getMolecularSequences()
    });
  }

  // getGeTable() {
  //   return forkJoin({
  //     patients: this.getPatients().pipe(first()),
  //     conditions: this.getConditions().pipe(first()),
  //     specimens: this.getSpecimens().pipe(first()),
  //   }).pipe(tap(console.log)).subscribe({
  //     next: value => console.log(value),
  //     complete: () => console.log('This is how it ends!'),
  //   });
  // }

  // See Meta: hydrator.effects.ts
  // Nur nicht der erste effect (funct noch nicht)

  // https://rxjs.dev/guide/operators
  // https://blog.angular-university.io/rxjs-higher-order-mapping/

  // loadData$ = createEffect(() => {
  //   return this.actions$.pipe(
  //     ofType(loadQueryParams),
  //     concatMap(() => {
  //       return forkJoin({
  //         network: this.apiService.loadNetwork(),
  //         patients: this.apiService.loadPatientsClassified(),
  //         thresholds: this.apiService.loadThresholds(),
  //       }).pipe(
  //         map((payload) => loadDataSuccess(payload)),
  //         catchError(() => of(loadDataFailure())),
  //       );
  //     }),
  //   );
  // });


//   return forkJoin({
//                     data1: this.apiService.loadStuff(),
//   data2: this.apiService.loadOtherStuff()
// }).pipe(
//   map((payload) => {
//     console.log(payload.data1);
//     console.log(payload.data2);
//
//     return mergeMap({
//       data3: this.apiService.loadLater(),
//
//     })
//
//   }),
//   catchError(() => {
//     console.log("Sth went wrong");
//   }),
// );


  // getGeTable(): Observable<Bundle> {
  //   let patients = this.getPatients();
  //   let specimens = this.getSpecimens();
  //
  // }
}


