import argparse
import sklearn
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
import numpy as np
from sklearn.metrics import accuracy_score
from joblib import dump

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-l','--labels',type = argparse.FileType('r'), required= True)
    parser.add_argument('-w','--weights', type = argparse.FileType('r'), required=True)
    parser.add_argument('-m','--matrix',type = str, required=True)
    parser.add_argument('-o','--out_model', type = str, required = True)
    parser.add_argument('-c','--cores',type = int, required= True)
    parser.add_argument('--test_size', type = float, default = 0.1)
    parser.add_argument('--num_training_samples', type = int, default = -1)

    args = parser.parse_args()

    assert(args.cores > 0)

    print('Loading data ...')

    labels = np.array([
        int(label.strip()) for label in args.labels.readlines()
    ])

    weights = np.array([
        float(weight.strip()) for weight in args.weights.readlines()
    ])

    features = np.load(args.matrix)

    X_train, X_test, weights_train, weights_test, y_train, y_test = train_test_split(features, weights, labels, test_size = args.test_size, random_state = 1234)

    if args.num_training_samples > 0:
        X_train, weights_train, y_train = X_train[:args.num_training_samples], weights_train[:args.num_training_samples], y_train[:args.num_training_samples]

    print('Training data shape: {}\nTesting data shape:{}'.format(
        str(X_train.shape),
        str(X_test.shape)
    ))

    print('Training model ...')

    param_grid = {
        'C' : [0.01,0.1,1.0,10.0,100.0]
    }
    svm_grid = GridSearchCV(
        LinearSVC(dual = False), 
            param_grid = param_grid, n_jobs = args.cores, scoring = 'roc_auc', cv = 5)\
                .fit(X_train, y_train, sample_weight = weights_train)

    model = svm_grid.best_estimator_

    print('Best AUC achieved: {}'.format(str(svm_grid.best_score_)))

    prediction = model.predict(X_test)
    accuracy = accuracy_score(y_test, prediction, sample_weight = weights_test)

    print('Validation set accuracy: {}'.format(str(accuracy)))
    print('Saving model ...')
    saved = False
    filepath = args.out_model
    while not saved:
        try:
            dump(model, filepath)
            saved = True
        except Exception as err:
            print(err)
            filepath = input('Alternative save file (enter to exit):')
            if filepath == '':
                raise err

    print('Done!')