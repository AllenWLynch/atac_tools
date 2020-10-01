#!/bin/bash

if (($#==4)); then
    fasta=$1
    bedfile=$2
    modelfile=$3
    matrixfile=$4
else
    echo "requires [fasta] [bedfile | stdin] [bias_model_file] [encoded_matrix_file]" 1>&2
    exit
fi
sequence_len=17

echo "Getting nucleotide sequences ..." 1>&2
sequences=$(python /Users/alynch/projects/atac_bias/scripts/faidx_wrapper.py $fasta $bedfile)

echo "Filtering sequences ..." 1>&2
filtered_sequences=$(paste $bedfile <(echo "$sequences") | cut -f5,7 | grep -v "N" | awk -v l=$sequence_len 'length($2)==l {print $0}')

fragment_ids=$(echo "$filtered_sequences" | cut -f1)
cut_sequences=$(echo "$filtered_sequences" | cut -f2)

echo "Encoding cut sites ..." 1>&2
python /Users/alynch/projects/atac_bias/scripts/simplex_encoder.py -o $matrixfile <(echo "$cut_sequences")

echo "Calculating cut site bias ..." 1>&2
bias_prob=$(python /Users/alynch/projects/atac_bias/scripts/predict_bias.py -f "$matrixfile.npy" -m $modelfile)

echo "Aggregating by fragment ..." 1>&2
python /Users/alynch/projects/atac_bias/scripts/aggregate_by_fragment.py <(echo "$fragment_ids") <(echo "$bias_prob")