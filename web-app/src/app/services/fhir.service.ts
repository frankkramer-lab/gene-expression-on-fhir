import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable, Subscriber, throwError} from 'rxjs';
import {catchError, concat, expand, first, map, pluck, retry, tap, toArray, take} from 'rxjs/operators';
import {Patient} from '../models/patient';
import {Bundle} from '../models/bundle';

@Injectable({
  providedIn: 'root'
})
export class FhirService {

  fhirEndpoint = 'http://localhost:8080/fhir/';

  constructor(private http: HttpClient) { }

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

  getSpecimens(): Observable<Bundle> {
    return this.http.get<Observable<Bundle>>(this.fhirEndpoint + 'Specimen').pipe(
      map(data => new Bundle(data, 'Specimen'))
    );
  }


    // return this.http.get(this.fhirEndpoint + 'Patient').pipe(
    //   pluck('entry'),
    //   tap(console.log),
    //   pluck('fullUrl'),
    //   tap(console.log)
    // );
    // getPatients(): Observable<Patient[]> {
    //   return this.http.get(this.fhirEndpoint + 'Patient').pipe(
    //     map((res: Bundle) => res.entry),
    //     map((res: Resource) => {
    //       return new Patient(...res.resource);
    //     })
    //   );
    // console.log(res);
    // return res;
}


