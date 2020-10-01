from collections import defaultdict
import argparse
import sys

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('cutsite_features',nargs='?',type = argparse.FileType('r'), default=sys.stdin)

    args = parser.parse_args()

    current_linenum = 1
    
    coldstart = True
    for cutsite_features in args.cutsite_features.readlines():

        features = cutsite_features.strip().split('\t')
        linenum = int(features[4])

        if linenum  < current_linenum:
            raise Exception('Cutsite features bedfile was not sorted by fragment number')
        elif linenum > current_linenum:
            for i in range(current_linenum, linenum): print('')
        elif not coldstart:
            print('\t', end = '')

        current_linenum = linenum

        bias_val = features[7]
        print(bias_val, end = '')
        coldstart=False