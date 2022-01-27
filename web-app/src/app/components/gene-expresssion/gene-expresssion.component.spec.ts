import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GeneExpresssionComponent } from './gene-expresssion.component';

describe('GeneExpresssionComponent', () => {
  let component: GeneExpresssionComponent;
  let fixture: ComponentFixture<GeneExpresssionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ GeneExpresssionComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(GeneExpresssionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
