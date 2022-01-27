export class Coding {
  system: string;
  code: string;
  display: string;

  constructor(data){
    this.system = data.system;
    this.code = data.code;
    this.display = data.display;
  }
}
