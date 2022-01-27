import { Component, OnInit } from '@angular/core';
import {Patient} from '../../models/patient';
import {FhirService} from '../../services/fhir.service';
import {Specimen} from '../../models/specimen';

@Component({
  selector: 'app-patient-list',
  templateUrl: './patient-list.component.html',
  styleUrls: ['./patient-list.component.css']
})
export class PatientListComponent implements OnInit {

  constructor(private fhirService: FhirService) { }

  patients: Patient[] | undefined;
  specimens: Specimen[] | [];

  getSpecimenById(id: number): Specimen[] {
    let specs = this.specimens.filter((s: Specimen) => s.subject === id);
    return specs;
  }

  ngOnInit(): void {

    this.fhirService.getPatients().subscribe((data) => {
      this.patients = data.entries as Patient[];
      console.log(this.patients);
    });

    this.fhirService.getSpecimens().subscribe((data) => {
      this.specimens = data.entries as Specimen[];
      console.log(this.specimens);
    });
  }

}
