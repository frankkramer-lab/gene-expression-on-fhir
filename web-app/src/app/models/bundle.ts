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
    console.log('Bundle:');
    console.log(data);
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
          console.log('Create Entry:');
          console.log(e);
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

// export class Bundle {
//   total: number;
//   entry: Entry[];
//
//   bla() {
//     console.log("No!");
//     return "Yes!";
//   }
//
//   getPatients (){
//     return this.entry.map(e => e.resource);
//   }
//
//   constructor(data: any){
//     console.log('Bundle:');
//     console.log(data);
//     this.total = data.number;
//     this.entry = data.entry.map(e => {
//         console.log("Create Entry:");
//         console.log(e);
//         return new Entry(e);
//       }
//     );
//     // this.entry = data.entry.forEach(e => {
//     //   console.log("Create Entry:");
//     //   console.log(e);
//     //   return new Entry(e);
//     // }
//     // ) ;
//   }
// }

// export class Entry {
//   fullUrl: string;
//   resource: any;
//   search: any;
//
//   constructor(data: any) {
//     this.fullUrl = data.fullUrl;
//     this.resource = new Patient(data.resource);
//     this.search = data.search;
//   }
// }
