#!/bin/bash

if [ $# -ne 2 ]; then
	echo "Requires [dupmarked fragment file] [num_samples]" 1>&2
	exit 1
fi

awk '$5!="-1" {print $1,$2,$3,$5}' $1 | uniq -c | shuf -n $2 | awk -v numsamples=$2 'sum < numsamples {sum+=$0; print $2,$3,$4,$1}'
