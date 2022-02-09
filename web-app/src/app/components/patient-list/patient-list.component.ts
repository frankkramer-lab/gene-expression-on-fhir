import { Component, OnInit } from '@angular/core';
import {Patient} from '../../models/patient';
import {FhirService} from '../../services/fhir.service';
import {Specimen} from '../../models/specimen';
import {Condition} from '../../models/condition';

@Component({
  selector: 'app-patient-list',
  templateUrl: './patient-list.component.html',
  styleUrls: ['./patient-list.component.css']
})
export class PatientListComponent implements OnInit {

  constructor(private fhirService: FhirService) { }

  patients: Patient[] | undefined;
  specimens: Specimen[] | undefined;
  conditions: Condition[] | undefined;

  getSpecimenById(id: number): Specimen[] {
    if (this.specimens === undefined) {
      return [];
    }
    const specs = this.specimens.filter((s: Specimen) => s.subject === id);
    return specs;
  }

  getConditionById(id: number): Condition | undefined {
    if (this.conditions === undefined) {
      return undefined;
    }
    const condition = this.conditions.filter((c: Condition) => c.subject === id).pop();
    return condition;
  }

  ngOnInit(): void {

    this.fhirService.getPatients().subscribe((data) => {
      this.patients = data.entries as Patient[];
      // console.log(this.patients);
    });

    this.fhirService.getSpecimens().subscribe((data) => {
      this.specimens = data.entries as Specimen[];
      // console.log(this.specimens);
    });

    this.fhirService.getConditions().subscribe((data) => {
      this.conditions = data.entries as Condition[];
      // console.log(this.specimens);
    });

  }

}
