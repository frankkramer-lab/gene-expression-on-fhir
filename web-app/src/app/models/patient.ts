import {Identifier} from './identifier';

export class Patient {
  id: number;
  identifier: Identifier;
  name: PatientName;
  telecom: PatientTelecom;
  gender: string;
  birthDate: string;
  address: PatientAddress;
  maritalStatus: MaritalStatus;

  getName(): string {
    return this.name.given.join(' ') + ' ' + this.name.family;
  }



  constructor(data: any){
    console.log("Patient:");
    console.log(data);
    this.id = Number(data.id);
    this.identifier = new Identifier(data.identifier[0]);
    this.name = new PatientName(data.name[0]);
    this.gender = data.gender;
    this.birthDate = data.birthDate;
    this.telecom = new PatientTelecom(data.telecom[0]);
    this.address = new PatientAddress(data.address[0]);
    this.maritalStatus = new MaritalStatus(data.maritalStatus);
  }

}


export class PatientName {
  family: string;
  given: string[];

  constructor(data: any) {
    this.family = data.family;
    this.given = data.given;
  }
}

export class PatientTelecom {
  system: string;
  value: string;

  constructor(data: any) {
    this.system = data.system;
    this.value = data.value;
  }
}

export class PatientAddress {
  line: string[];
  city: string;
  district: string;
  state: string;
  postalCode: string;

  constructor(data) {
    this.line = data.line;
    this.city = data.city;
    this.district = data.district;
    this.state = data.state;
    this.postalCode = data.postalCode;
  }
}

export class MaritalStatus {
  code: string;
  text: string;

  constructor(data){
    this.code = data.coding[0].code;
    this.text = data.text;
  }
}
