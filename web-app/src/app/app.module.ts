import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { PatientListComponent } from './components/patient-list/patient-list.component';
import {RouterModule} from '@angular/router';
import { HomeComponent } from './components/home/home.component';
import {HttpClientModule} from '@angular/common/http';
import { PatientGeneExpressionComponent } from './components/patient-gene-expression/patient-gene-expression.component';
import { GeneExpresssionComponent } from './components/gene-expresssion/gene-expresssion.component';

@NgModule({
  declarations: [
    AppComponent,
    PatientListComponent,
    HomeComponent,
    PatientGeneExpressionComponent,
    GeneExpresssionComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    RouterModule.forRoot([
      {path: '', component: HomeComponent},
      {path: 'patients', component: PatientListComponent},
      {path: 'expression', component: GeneExpresssionComponent},
      {path: 'expression/:id', component: PatientGeneExpressionComponent}
    ])
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
