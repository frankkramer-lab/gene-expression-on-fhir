import {Identifier} from './identifier';
import {Coding} from './coding';
import {Observation} from './observation';

export class MolecularSequence {
  id: number;
  ensembl: string;
  ensemblUrl: string;
  geneSymbol: string;
  chromosome: Coding;
  orientation: string;
  start: number;
  end: number;

  observations = {};
  oloaded = false;

  setObservations(observations: Observation[]): void{
    observations.forEach(o => {
      this.observations[o.specimen] = o;
    });
    this.oloaded = true;
  }

  constructor(data){
    this.id = Number(data.id);
    data.identifier.forEach(i => {
      if (i.system === 'ensemble_id'){
        this.ensembl = i.value;
      }else if (i.system === 'gene_symbol'){
        this.geneSymbol = i.value;
      }
    });
    this.chromosome = new Coding(data.referenceSeq.chromosome.coding[0]);
    this.orientation = data.referenceSeq.orientation;
    this.start = Number(data.referenceSeq.windowStart);
    this.end = Number(data.referenceSeq.windowEnd);
    this.ensemblUrl = data.repository[0].url;
    // console.log(this);
  }
}
