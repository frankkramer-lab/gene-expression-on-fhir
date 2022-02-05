import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ExpressionLegendComponent } from './expression-legend.component';

describe('ExpressionLegendComponent', () => {
  let component: ExpressionLegendComponent;
  let fixture: ComponentFixture<ExpressionLegendComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ExpressionLegendComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ExpressionLegendComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
