from pyfaidx import Fasta
import argparse
import numpy as np
import sys

np.random.seed(1234)


def sample_regions(probs, num_regions):
    return np.random.choice(len(probs), p = probs, size = (num_regions,))

def sample_cut_site(region):
    (chrom, start, end) = region
    cut_center = start + np.random.choice(end - start) #uniform over selected region
    cut_site = (chrom, cut_center, cut_center + 1)

    return cut_site


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('accessibility_regions', type = argparse.FileType('r'), help= 'bedgraph file of accessibility over regions')
    parser.add_argument('num_samples', type = int, default= 1e5)
    parser.add_argument('-n','--count_normalization', choices=['sqrt','log2','none'], default='none')
    
    args = parser.parse_args()

    regions, accessibility = [],[]
    for line in args.accessibility_regions.readlines():
        chrom, start, end, region_accessibility = line.strip().split('\t')
        regions.append((chrom, int(start), int(end)))
        accessibility.append(int(region_accessibility))

    counts = np.array(accessibility)

    if args.count_normalization == 'sqrt':
        counts = np.sqrt(counts)
    elif args.count_normalization == 'log2' : 
        counts = np.log2(counts)

    region_probs = counts / counts.sum()

    sampled_regions = np.random.choice(len(regions), p = region_probs, size = args.num_samples, replace = True)

    for i, region in enumerate(sampled_regions):
        cut_site = sample_cut_site(regions[region])

        if i%20 == 0:
            print('\rSampling {}/{}'.format(str(i), str(args.num_samples)), file = sys.stderr, end = '')
            
        print('\t'.join([str(x) for x in cut_site]))





