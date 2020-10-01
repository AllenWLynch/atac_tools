#!/bin/bash

scriptspath=/Users/alynch/projects/atac_bias/scripts/

if [ $# -ne 3 ]; then
    echo "requires [FASTA] [REGIONS] [MODEL]"
    exit
else
    genome=$1
    bedfile=$2
    modelfile=$3
fi

cutsites=$(python3 $scriptspath/regions_to_cutsites.py $bedfile) 

sequences=$($scriptspath/expand_cut_center.sh <(echo "$cutsites") 4 9 | python3 $scriptspath/faidx_wrapper.py $genome)

metadata=$(paste <(echo "$cutsites") <(echo "$sequences") | grep -v "N" | awk 'length($7)==17')

bias=$(cat <(echo "$metadata") | cut -f7 | python3 $scriptspath/predict_bias.py -m $modelfile)

paste <(echo "$metadata") <(echo "$bias")
