import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PatientGeneExpressionComponent } from './patient-gene-expression.component';

describe('PatientGeneExpressionComponent', () => {
  let component: PatientGeneExpressionComponent;
  let fixture: ComponentFixture<PatientGeneExpressionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PatientGeneExpressionComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PatientGeneExpressionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
