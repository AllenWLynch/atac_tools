import argparse



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('chr',type = str)
    parser.add_argument('start', type = int)
    parser.add_argument('end', type = int)

    args = parser.parse_args()

    assert(args.end > args.start)

    for n, i in enumerate(range(args.start, args.end)):
        print(args.chr, i-1,i,n, "0", '+',sep = '\t')
        print(args.chr, i,i+1,n, "0", '-',sep = '\t')