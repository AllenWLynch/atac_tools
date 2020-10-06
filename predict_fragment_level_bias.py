
from joblib import load
import numpy as np
import argparse
import sys

class Preprocessor:
    
    def __init__(self):
        pass
    
    def fit(self):
        pass
    
    def transform(self, X):
        
        fraglen = X[:,0]
        gc_content = X[:,1]
        biases = X[:,2:]
        
        fraglen_features = np.log2(fraglen)
        bias_features = np.log(biases/(1 - biases))
        
        output = np.hstack([np.vstack([fraglen_features, gc_content]).T, bias_features])

        return output


class lines_grouper:

    def __init__(self, file_object, chunk_size):
        self.file_object = file_object
        self.chunk_size = chunk_size

    def __iter__(self):
        morelines = True
        while morelines:
            group = []
            for i in range(self.chunk_size):
                nextline = self.file_object.readline()
                if nextline == '':
                    morelines = False
                    break
                else:
                    group.append(nextline)
            if len(group) > 0:
                yield group

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-b','--bias_file',type = argparse.FileType('r'), default = sys.stdin, nargs = '?')
    parser.add_argument('-m','--fragment_model', type=str, required=True)
    parser.add_argument('--bias1',type=int, default = 6)
    parser.add_argument('--bias2', type = int, default=7)
    parser.add_argument('--gc', type = int, default=8)
    parser.add_argument('--len', type = int, default=9)

    args = parser.parse_args()

    print('Predicting bias ...', file = sys.stderr)
    
    pipeline = load(args.fragment_model)

    grouper = lines_grouper(args.bias_file, 1000)

    fragments_processed = 0
    for fragments in iter(grouper):

        fragments_processed += len(fragments)
        print('\rFragments processed: {}'.format(str(fragments_processed)), end = '', file = sys.stderr)
        
        fragment_features = list(zip(*[x.strip().split('\t') for x in fragments]))

        feature_matrix = np.vstack([
            fragment_features[args.len - 1],
            fragment_features[args.gc - 1],
            fragment_features[args.bias1 - 1],
            fragment_features[args.bias2 - 1],
        ]).astype(np.float32).T

        dup_rates = pipeline.predict(feature_matrix)

        for fragment, dup_rate in zip(fragments, dup_rates):
            print(fragment.strip(), str(dup_rate), sep = '\t')        
    
    print('', file = sys.stderr)