#!/bin/bash


if (($# == 2)); then
    upstream=$1
    offset=$2
    cuts_file=/dev/stdin
elif (($# == 3)); then
    upstream=$2
    offset=$3
    cuts_file=$1
else
    echo "Must pass [cuts_file / stdin] [upstream] [downstream] arguments" 1>&2
    exit
fi

a=$((($offset - 1) / 2))

awk -v up=$upstream -v a=$a '{print $1,$2-a-up,$2+a+1+up,$4,$5,$6}' $cuts_file | tr " " "\t"