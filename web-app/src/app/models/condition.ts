import {Identifier} from './identifier';
import {Coding} from './coding';
import {Patient} from './patient';

export class Condition {
  id: string;
  identifier: Identifier;
  code: Coding;
  subject: string;

  constructor(data){
    this.id = data.id;
    this.identifier = data.identifier[0];
    this.code = new Coding(data.code.coding[0]);
    this.subject = data.subject.reference;
  }
}
