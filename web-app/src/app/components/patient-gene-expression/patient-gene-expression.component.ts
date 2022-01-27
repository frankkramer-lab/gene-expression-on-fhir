import { Component, OnInit } from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {ParamMap} from '@angular/router';
import {switchMap} from 'rxjs/internal/operators/switchMap';

@Component({
  selector: 'app-patient-gene-expression',
  templateUrl: './patient-gene-expression.component.html',
  styleUrls: ['./patient-gene-expression.component.css']
})
export class PatientGeneExpressionComponent implements OnInit {

  id: string;
  constructor(private route: ActivatedRoute) { }

  ngOnInit(): void {
    this.id = this.route.snapshot.paramMap.get('id');
  }

}
