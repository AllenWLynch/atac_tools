#!/bin/bash

if [ $# -ne 5 ]; then
    echo "requires [FASTA] [REGIONS] [CUTSITE-MODEL] [FRAGMENT-MODEL] [SCRIPTS-PATH]"
    exit
else
    genome=$1
    bedfile=$2
    cutsite_model=$3
    fragment_model=$4
    scriptspath=$5
fi

#scriptspath=/Users/alynch/projects/atac_bias/scripts/

echo "Finding cut centers ..." 1>&2
cutsites=$($scriptspath/get_cut_centers_from_fragment.sh $bedfile)

echo "Getting nucleotide sequences ..." 1>&2
sequences=$($scriptspath/expand_cut_center.sh <(echo "$cutsites") 4 9 | python3 $scriptspath/faidx_wrapper.py $genome)

echo "Filtering sequences ..." 1>&2
metadata=$(paste <(echo "$cutsites") <(echo "$sequences") | awk '$7 !~ /N/' | awk 'length($7)==17')

bias=$(cat <(echo "$metadata") | cut -f7 | python3 $scriptspath/predict_bias.py -m $cutsite_model)

echo "Aggregating bias predictions ..." 1>&2
fragment_cutsite_biases=$(paste <(echo "$metadata") <(echo "$bias") | python3 $scriptspath/collapse_to_fragments.py)

echo "Predicting fragment duplication rate ..." 1>&2
other_features=$($scriptspath/get_fragment_features.sh $genome $bedfile)

paste $bedfile <(echo "$fragment_cutsite_biases") <(echo "$other_features") | awk 'NF==9' | \
    python $scriptspath/predict_fragment_level_bias.py -m $fragment_model
