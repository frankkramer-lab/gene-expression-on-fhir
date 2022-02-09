import {Patient} from './patient';
import {Condition} from './condition';
import {Specimen} from './specimen';
import {Observable} from 'rxjs';
import {Observation} from './observation';
import {MolecularSequence} from './molecular-sequence';

export class Bundle {
  total: number;
  entries: Patient[] | Condition[] | Specimen[] | Observation[] | MolecularSequence[];
  previous: string = undefined;
  next: string = undefined;

  constructor(data: any, resourceType: string){
    // console.log('Bundle:');
    // console.log(data);
    this.total = data.number;

    data.link.forEach(l => {
      if (l.relation === 'next') {
        this.next = l.url;
      }else if (l.relation === 'previous') {
        this.previous = l.url;
      }
    });

    if (data.entry !== undefined) {
      this.entries = data.entry.map(e => {
          // console.log('Create Entry:');
          // console.log(e);
          if (resourceType === 'Patient') {
            return new Patient(e.resource);
          } else if (resourceType === 'Condition') {
            return new Condition(e.resource);
          } else if (resourceType === 'Specimen') {
            return new Specimen(e.resource);
          } else if (resourceType === 'Observation') {
            return new Observation(e.resource);
          } else if (resourceType === 'MolecularSequence') {
            return new MolecularSequence(e.resource);
          }
        }
      );
    } else {
      this.entries = [];
    }
  }
}
