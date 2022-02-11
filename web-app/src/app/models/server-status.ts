export class ServerStatus {
  status = false;
  fhirEndpoint: string;

  constructor(status: any, fhirEndpoint){
    this.fhirEndpoint = fhirEndpoint;
    if (status.resourceType === 'Error') {
      this.status = false;
    } else {
      this.status = true;
    }
  }
}
