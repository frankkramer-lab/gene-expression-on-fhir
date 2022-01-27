export class Identifier {
  system: string;
  value: string;

  constructor(data){
    this.system = data.system;
    this.value = data.value;
  }
}
