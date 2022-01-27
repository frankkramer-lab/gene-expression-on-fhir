import os
import re

import pandas as pd
import numpy as np

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option('display.width', None)
np.set_printoptions(edgeitems=30, linewidth = 10000)

class gff3():
    def __init__(self, gff3_file, process=False, verbose=True):
        self.verbose = verbose
        self.gff3_file = gff3_file
        self.processed_file = re.sub(
            r"\.gz$",
            ".processed.csv.gz",
            self.gff3_file
        )

        if process:
            self.read_gpr()
        elif os.path.isfile(self.processed_file):
            self.read_processed()
        else:
            if self.verbose:
                print('No processed GFF3 file found, parsing GFF3 file:')
            self.read_gpr()


    def read_gpr(self):
        if self.verbose:
            print('Reading GFF3 file (',self.gff3_file,')...', end='')

        cols = {"seqid": str,
                "source": str,
                "type": str,
                "start": int,
                "end": int,
                "score": str,
                "strand": str,
                "phase": str,
                "attributes": str}

        self.data = pd.read_csv(self.gff3_file,
                                sep="\t",
                                names=cols.keys(),
                                dtype=cols,
                                comment='#')
        if self.verbose:
            print('done')

        self.data.replace({'source': {'.': np.nan},
                           'score':  {'.': np.nan},
                           'strand': {'.': np.nan},
                           'phase': {'.': np.nan}},
                          inplace=True)

        if self.verbose:
            print('Get different attributes from the "attributes" column...', end='')

        self.data['attributes'] = self.data['attributes'].map(
            lambda atts:
                dict(x.split("=") for x in atts.split(";"))
        )

        attributes = sorted(
            set(
                self.data['attributes'].map(
                    lambda atts:
                        atts.keys()).explode()
                )
        )

        if self.verbose:
            print('done')
            print('Attributes: ',attributes)
            print('Reorganize attributes into columns...', end='')

        def process_attributes(x):
            row = x['attributes']
            return [row[att] if att in row.keys() else np.nan for att in attributes]

        self.data[attributes] = self.data.apply(process_attributes, axis=1, result_type='expand')

        self.data.drop('attributes', axis=1, inplace=True)

        if self.verbose:
            print('done')
            print('Saving processed gff3 data...', end='')

        self.data.to_csv(self.processed_file, compression='gzip', index=False)

        if self.verbose:
            print('done')

    def read_processed(self):
        if self.verbose:
            print('Reading processed GFF3 file (',self.processed_file,')...', end='')

        cols = {'seqid': str,
                'source': str,
                'type': str,
                'start': int,
                'end': int,
                'score': float,
                'strand': str,
                'phase': str,
                'Alias': str,
                'ID': str,
                'Name': str,
                'Parent': str,
                'biotype': str,
                'ccdsid': str,
                'constitutive': str,
                'description': str,
                'ensembl_end_phase': str,
                'ensembl_phase': str,
                'exon_id': str,
                'external_name': str,
                'gene_id': str,
                'logic_name': str,
                'protein_id': str,
                'rank': str,
                'tag': str,
                'transcript_id': str,
                'transcript_support_level': str,
                'version': str
                }
        self.data = pd.read_csv(self.processed_file, dtype=cols)
        if self.verbose:
            print('done')

    def summary(self):
        for c in self.data.columns:
            print(f'{c}: ', self.data[c].dropna().unique())




# gff = gff3("../data/Homo_sapiens.GRCh38.99.chr.gff3.gz")
# gff.summary()

