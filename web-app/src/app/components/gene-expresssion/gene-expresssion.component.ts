import { Component, OnInit } from '@angular/core';
import {FhirService} from '../../services/fhir.service';
import {Patient} from '../../models/patient';
import {Specimen} from '../../models/specimen';
import {MolecularSequence} from '../../models/molecular-sequence';
import {ActivatedRoute} from '@angular/router';
import {Observation} from '../../models/observation';
import {Condition} from '../../models/condition';
import {TableHead} from '../../models/table-head';
import {ServerStatus} from '../../models/server-status';

@Component({
  selector: 'app-gene-expresssion',
  templateUrl: './gene-expresssion.component.html',
  styleUrls: ['./gene-expresssion.component.css']
})
export class GeneExpresssionComponent implements OnInit {

  serverStatus: ServerStatus | undefined;

  patients: Patient[] | undefined;
  conditions: Condition[] = [];
  specimens: Specimen[] | undefined;

  tableHead: TableHead = new TableHead('conditions');

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
    this.isLoading = true;

    this.fhirService.getServerStatus().subscribe(status => {
        this.serverStatus = status;
      }
    );

    this.fhirService.getPCSMS().subscribe(obj => {
      this.tableHead.get('None');
      this.conditions = obj.conditions.entries as Condition[];
      this.specimens = obj.specimens.entries as Specimen[];
      this.patients = obj.patients.entries as Patient[];
      this.patients.forEach( p => {
        const c = this.getConditonById(p.id);
        const specimen: Specimen[] = this.getSpecimenById(p.id);
        specimen.forEach( s => {
          const patient = this.tableHead.get(c).get(s.note).get(p.getName());
          patient.patientId = p.id;
          patient.specimenId = s.id;
        });
      });

      // console.log('TableHead:');
      // console.log(this.tableHead);
      // this.tableHead.children.forEach(c => console.log(c.getColspan()));
    });

    this.getMolecularSequences();
  }

  getSpecimenById(id: number): Specimen[] {
    return this.specimens.filter((s: Specimen) => s.subject === id);
  }

  getConditonById(id: number): string {
    const condition = this.conditions.filter((c: Condition) => c.subject === id);
    return condition.length === 0 ? 'None' : condition[0].code.display;
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
    // console.log(this.searchTerm);
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
    // console.log('Get: offset=' + offset);
    this.showPagination = true;
    this.molecularSequence = [];
    this.addMolecularSequences(offset);
  }

  addMolecularSequences(offset = 0, isGeneSymbol = true, searchTerms = []): void {
    // console.log('Get: offset=' + offset);

    offset = isNaN(Number(offset)) ? 0 : Number(offset);
    offset = offset < 0 ? 0 : offset;

    const ccount = searchTerms.length !== 0 ? searchTerms.length + 12 : 12;

    this.fhirService.getMolecularSequences(offset, ccount, isGeneSymbol, searchTerms)
      .subscribe((data) => {
        // console.log('add mol seq: ' + this.molecularSequence);

        this.hasNext = data.next !== undefined;
        this.hasPrevious = data.previous !== undefined;
        this.offset = offset;

        (data.entries as MolecularSequence[]).forEach(m => {
          this.molecularSequence.push(m);
          this.fhirService.getObservationsByReference(m.id).subscribe(obs => {
            const observations = obs.entries as Observation[];
            const orderedObservations: Observation[] = [];
            this.tableHead.children.forEach(condition => {
              condition.children.forEach( specimen => {
                specimen.children.forEach( patient => {
                  orderedObservations.push(observations.filter(o => {
                    return o.specimen === patient.specimenId && o.subject === patient.patientId;
                  })[0]);
                });
              });
            });
            m.setObservations(orderedObservations);
            // console.log(m.observations);
          });
        });
        // console.log(this.molecularSequence);
        this.isLoading = false;
      });
  }

}
