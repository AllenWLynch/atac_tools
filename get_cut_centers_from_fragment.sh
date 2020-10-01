#!/bin/bash

if (($# == 1)); then
    fragment_file=$1
elif (($# == 0)); then
    fragment_file=/dev/stdin
else
    echo "requires [fragment_file] or stdin" 1>&2
    exit
fi

awk '{
    print $1,$2,$2+1,$4,NR,"+";
    print $1,$3,$3+1,$4,NR,"-";
}' $fragment_file | tr " " "\t"