scriptspath=/Users/alynch/projects/atac_bias/scripts/

if [ $# -ne 3 ]; then
    echo "requires [FASTA] [REGIONS] [MODEL]"
    exit
else
    genome=$1
    bedfile=$2
    modelfile=$3
fi

scriptspath=/Users/alynch/projects/atac_bias/scripts/

echo "Finding cut centers ..." 1>&2
cutsites=$($scriptspath/get_cut_centers_from_fragment.sh $bedfile)

echo "Getting nucleotide sequences ..." 1>&2
sequences=$($scriptspath/expand_cut_center.sh <(echo "$cutsites") 4 9 | python3 $scriptspath/faidx_wrapper.py $genome)

echo "Filtering sequences ..." 1>&2
metadata=$(paste <(echo "$cutsites") <(echo "$sequences") | awk '$7 !~ /N/' | awk 'length($7)==17')

bias=$(cat <(echo "$metadata") | cut -f7 | python3 $scriptspath/predict_bias.py -m $modelfile)

echo "Aggregating bias predictions ..." 1>&2
fragment_bias=$(paste <(echo "$metadata") <(echo "$bias") | python3 $scriptspath/collapse_to_fragments.py)

paste $bedfile <(echo "$fragment_bias")
