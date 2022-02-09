import {Identifier} from './identifier';
import {Coding} from './coding';
import {Color} from './color';

export class Observation {
  id: string;
  identifier: Identifier;
  gene: Coding;
  subject: number;
  specimen: number;
  value: number;
  derivedFrom: number;

  color: string;

  constructor(data){
    this.id = data.id;
    this.identifier = new Identifier(data.identifier[0]);
    this.gene = new Coding(data.extension[0].valueCodeableConcept.coding[0]);
    this.subject = Number(data.subject.reference.split('/').pop());
    this.specimen = Number(data.specimen.reference.split('/').pop());
    // Correct the multiplication for being an integer
    // 8.04957732029089
    // x*10E6
    this.value = Number(data.valueInteger) / 1000000;
    this.color = Color.getColor(this.value);

    this.derivedFrom = Number(data.derivedFrom[0].reference.split('/').pop());
    // console.log(this);
  }
}
