from pyfaidx import Fasta
import argparse
import subprocess
from collections import Counter
import sys

parser = argparse.ArgumentParser()
parser.add_argument('fasta_file', type = argparse.FileType('r'))
parser.add_argument('bed_file', nargs = "?", type = argparse.FileType('r'), default= sys.stdin)
parser.add_argument('-d','--delimiter', type = str, default='\t')
parser.add_argument('-gc','--gc-content',action='store_true')
parser.add_argument('-l','--lazy',action='store_true')

if __name__ == "__main__":

    args = parser.parse_args()

    genes = Fasta(args.fasta_file.name)

    regions = args.bed_file.readlines()
    num_regions = len(regions)

    for i, region in enumerate(regions):
        if i % 50 == 0:
            print('\rProcessed {:.2f} percent of regions'.format(i/num_regions * 100), end = '', file = sys.stderr)
        try:
            #print(region.strip().split(args.delimiter), args.delimiter)
            chrom, start, end = region.strip().split(args.delimiter)[:3]
            start, end = int(start), int(end)
            strand = region.strip().split(args.delimiter)[5]

            sequence = genes[chrom][start : end]

            if strand == '-':
                sequence = sequence.reverse.complement
            
            if args.gc_content:
                nuc_counts = Counter(sequence.seq.upper())
                gc_content = (nuc_counts['G'] + nuc_counts['C']) / len(sequence)
                print(gc_content)
            else:
                print(sequence.seq.upper())

        except (KeyError,ValueError) as err:
            print('Error on region: {}'.format(region), file = sys.stderr)
            if args.lazy:
                print('N'*(end-start))
            else:
                raise err

    print('', file = sys.stderr)