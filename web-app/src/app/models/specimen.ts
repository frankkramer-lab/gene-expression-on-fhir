import {Identifier} from './identifier';
import {Coding} from './coding';

export class Specimen {
  id: number;
  identifier: Identifier;
  type: Coding;
  subject: number;
  note: string;

  constructor(data){
    this.id = Number(data.id);
    this.identifier = new Identifier(data.identifier[0]);
    this.type = new Coding(data.type.coding[0]);
    this.subject = Number(data.subject.reference.split('/').pop());
    this.note = data.note[0].text;
    // console.log(this);
  }
}
