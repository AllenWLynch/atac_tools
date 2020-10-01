
import argparse
import sys

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('regions', default=sys.stdin, nargs = '?', type = argparse.FileType('r'))

    args = parser.parse_args()

    for region_num, region in enumerate(args.regions):

        region = region.strip().split('\t')

        chrom,start,end = region[:3]
        try:
            name = region[4]
        except IndexError:
            name = str(region_num)

        for index, i in enumerate(range(int(start), int(end))):

            print(chrom, str(i), str(i+1), name, str(index + 1), '+', sep = '\t')
            print(chrom, str(i), str(i+1), name, str(index + 1), '-', sep = '\t')