import { Component, OnInit } from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {ParamMap} from '@angular/router';
import {switchMap} from 'rxjs/internal/operators/switchMap';
import {Patient} from '../../models/patient';
import {Specimen} from '../../models/specimen';
import {FhirService} from '../../services/fhir.service';
import {MolecularSequence} from '../../models/molecular-sequence';
import {Observation} from '../../models/observation';
import {map} from 'rxjs/operators';

@Component({
  selector: 'app-patient-gene-expression',
  templateUrl: './patient-gene-expression.component.html',
  styleUrls: ['./patient-gene-expression.component.css']
})
export class PatientGeneExpressionComponent implements OnInit {

  id: number;
  patient: Patient | undefined;
  specimens: Specimen[] | undefined;
  molecularSequence: MolecularSequence[] | undefined;
  hasPrevious = false;
  hasNext = false;
  isLoading = true;
  showPagination = true;
  offset =  0;
  searchTermPlaceholder = 'EGFR TSPAN6 ENSG00000002330 CDKN2A CDKN2B SSX1';
  searchTerm = '';

  constructor(private route: ActivatedRoute, private fhirService: FhirService) { }

  ngOnInit(): void {
    this.id = Number(this.route.snapshot.paramMap.get('id'));

    this.isLoading = true;

    this.fhirService.getPatientById(this.id).subscribe((pat) => {
      this.patient = pat;
    });

    this.fhirService.getSpecimensByPatient(this.id).subscribe((data) => {
      this.specimens = data.entries as Specimen[];
      console.log(this.specimens);
    });

    this.getMolecularSequences();
  }

  next(): void {
    if (this.hasNext && !this.isLoading){
      this.isLoading = true;
      this.getMolecularSequences(this.offset + 1);
    }
  }

  previous(): void {
    if (this.hasPrevious && !this.isLoading) {
      this.isLoading = true;
      this.getMolecularSequences(this.offset - 1);
    }
  }

  example(): void {
    this.searchTerm = this.searchTermPlaceholder;
    this.search();
  }

  search(): void {
    console.log(this.searchTerm);
    this.showPagination = false;
    const geneSymbols = [];
    const ensembleIds = [];
    this.searchTerm.toUpperCase().split(/[ ,\t]+/).forEach(t => {
      if (/ENSG[0-9]{11}/.test(t)){
        ensembleIds.push(t);
      }else{
        geneSymbols.push(t);
      }
    });

    if ((geneSymbols.length !== 0 ) || (ensembleIds.length !== 0)) {
      this.molecularSequence = [];
      if (geneSymbols.length !== 0) {
        this.addMolecularSequences(0, true, geneSymbols);
      }
      if (ensembleIds.length !== 0) {
        this.addMolecularSequences(0, false, ensembleIds);
      }
      this.hasNext = false;
      this.hasPrevious = false;
    }
  }


  getMolecularSequences(offset = 0): void {
    console.log('Get: offset=' + offset);
    this.showPagination = true;
    this.molecularSequence = [];
    this.addMolecularSequences(offset);
    // this.fhirService.getMolecularSequences(offset).subscribe((data) => {
    //   this.molecularSequence = data.entries as MolecularSequence[];
    //
    //   this.hasNext = data.next !== undefined;
    //   this.hasPrevious = data.previous !== undefined;
    //   this.offset = offset;
    //
    //   this.molecularSequence.forEach(m => {
    //     this.fhirService.getObservationsByReference(m.id, this.id).subscribe(obs => {
    //       m.setObservations(obs.entries as Observation[]);
    //       console.log(m.observations);
    //     });
    //   });
    //   console.log(this.molecularSequence);
    //   this.isLoading = false;
    // });
  }

  addMolecularSequences(offset = 0, isGeneSymbol = true, searchTerms = []): void {
    console.log('Get: offset=' + offset);

    offset = isNaN(Number(offset)) ? 0 : Number(offset);
    offset = offset < 0 ? 0 : offset;

    const ccount = searchTerms.length !== 0 ? searchTerms.length + 12 : 12;

    this.fhirService.getMolecularSequences(offset, ccount, isGeneSymbol, searchTerms)
      .subscribe((data) => {
        // this.molecularSequence.concat(data.entries as MolecularSequence[]);
        console.log('add mol seq: ' + this.molecularSequence);

        this.hasNext = data.next !== undefined;
        this.hasPrevious = data.previous !== undefined;
        this.offset = offset;

        (data.entries as MolecularSequence[]).forEach(m => {
          this.molecularSequence.push(m);
          this.fhirService.getObservationsByReference(m.id, this.id).subscribe(obs => {
            m.setObservations(obs.entries as Observation[]);
            console.log(m.observations);
          });
        });
        console.log(this.molecularSequence);
        this.isLoading = false;
    });
  }

  // getMolecularSequences(offset = 0): void {
  //   console.log('Get: offset=' + offset);
  //   this.fhirService.getMolecularSequences(offset).subscribe((data) => {
  //     this.molecularSequence = data.entries as MolecularSequence[];
  //
  //     this.hasNext = data.next !== undefined;
  //     this.hasPrevious = data.previous !== undefined;
  //     this.offset = offset;
  //
  //     this.molecularSequence.forEach(m => {
  //       this.fhirService.getObservationsByReference(m.id, this.id).subscribe(obs => {
  //         m.setObservations(obs.entries as Observation[]);
  //         console.log(m.observations);
  //       });
  //     });
  //     console.log(this.molecularSequence);
  //     this.isLoading = false;
  //   });
  // }

}
