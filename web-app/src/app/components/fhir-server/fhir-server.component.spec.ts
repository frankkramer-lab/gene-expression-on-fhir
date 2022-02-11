import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FhirServerComponent } from './fhir-server.component';

describe('FhirServerComponent', () => {
  let component: FhirServerComponent;
  let fixture: ComponentFixture<FhirServerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ FhirServerComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(FhirServerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
