import { Component, OnInit } from '@angular/core';
import {Color} from '../../models/color';

@Component({
  selector: 'app-expression-legend',
  templateUrl: './expression-legend.component.html',
  styleUrls: ['./expression-legend.component.css']
})
export class ExpressionLegendComponent implements OnInit {

  minColor = Color.getColor(0);
  maxColor = Color.getColor(10);

  constructor() { }

  ngOnInit(): void {
  }

}
