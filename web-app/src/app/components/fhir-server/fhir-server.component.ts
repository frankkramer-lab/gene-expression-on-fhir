import { Component, OnInit } from '@angular/core';
import {ServerStatus} from '../../models/server-status';
import {FhirService} from '../../services/fhir.service';

@Component({
  selector: 'app-fhir-server',
  templateUrl: './fhir-server.component.html',
  styleUrls: ['./fhir-server.component.css']
})
export class FhirServerComponent implements OnInit {

  serverStatus: ServerStatus | undefined;
  fhirEndpoint: string;

  constructor(private fhirService: FhirService) { }

  ngOnInit(): void {
    this.fhirEndpoint = this.fhirService.defaultFhirEndpoint;
    this.fhirService.getServerStatus().subscribe(status => {
        this.serverStatus = status;
      }
    );
  }

  checkServer(): void {
    this.serverStatus = undefined;
    this.fhirService.setFhirEndpoint(this.fhirEndpoint).subscribe(status => {
        this.serverStatus = status;
      }
    );
  }

  defaultFhirServer(): void {
    this.fhirEndpoint = this.fhirService.defaultFhirEndpoint;
    this.checkServer();
  }
}
