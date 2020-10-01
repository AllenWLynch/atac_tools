
from joblib import load
import numpy as np
import argparse
import sys
from simplex_encoder import OligoEncoder, WMerSimplexEncoder


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
    parser.add_argument('-s','--sequences',type = argparse.FileType('r'), default = sys.stdin, nargs = '?')
    parser.add_argument('-m','--model', type=str, required=True)
    parser.add_argument('-w','--wmer_len', type = int, default= 2)

    args = parser.parse_args()

    print('Predicting bias ...', file = sys.stderr)
    encoder = OligoEncoder(args.wmer_len, WMerSimplexEncoder)

    model = load(args.model)

    grouper = lines_grouper(args.sequences, 1000)

    sequences_processed = 0
    for sequences in iter(grouper):

        sequences_processed += len(sequences)
        sequences = [x.strip() for x in sequences]

        features = encoder.generate_feature_matrix(sequences)
        probs = model.predict_proba(features)[:,1]
        
        print('\n'.join([str(x) for x in probs.reshape(-1)]))

        print('\rSequences processed: {}'.format(str(sequences_processed)), end = '', file = sys.stderr)
    
    print('', file = sys.stderr)