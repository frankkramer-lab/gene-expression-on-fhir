import {Specimen} from './specimen';

export class TableHead {
  name: string;
  children: TableHead[];

  patientId: number;
  specimenId: number;

  get(name: string): TableHead {
    let res = this.children.filter((t: TableHead) => t.name === name).pop();
    if (res === undefined) {
      res = new TableHead(name);
      this.children.push(res);
    }
    return res;
  }

  getColspan(): number {
    if (this.children.length === 0) {
      return 1;
    } else {
      let sum = 0;
      this.children.forEach( c => sum += c.getColspan());
      return sum;
    }
  }

  constructor(name: string) {
    this.name = name;
    this.children = [];
  }
}

