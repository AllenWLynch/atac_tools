import argparse
import sklearn
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from xgboost import XGBRegressor
import numpy as np
from sklearn.metrics import accuracy_score
from joblib import dump
import json
from sklearn.metrics import mean_squared_error

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-t','--target',type = argparse.FileType('r'), required= True)
    parser.add_argument('-w','--weights', type = argparse.FileType('r'))
    parser.add_argument('-m','--matrix',type = str, required=True)
    parser.add_argument('-o','--out_model', type = str, required = True)
    parser.add_argument('-c','--cores',type = int, required= True)
    parser.add_argument('--test_size', type = float, default = 0.1)
    parser.add_argument('--num_training_samples', type = int, default = -1)
    parser.add_argument('--param_config', type = argparse.FileType('r'), required= True, help = 'Json file with parameter configurations')

    args = parser.parse_args()

    #test to make sure dump will work to specified file
    dump({}, args.out_model)

    assert(args.cores > 0)

    print('Loading data ...')

    targets = np.array([
        float(target.strip()) for target in args.target.readlines()
    ])

    if args.weights:
        weights = np.array([
            float(weight.strip()) for weight in args.weights.readlines()
        ])
    else:
        weights = np.ones(len(targets))

    features = np.load(args.matrix)

    X_train, X_test, y_train, y_test, weights_train, weights_test = \
        train_test_split(features, weights, targets, test_size = args.test_size, random_state = 1234)

    if args.num_training_samples > 0:
        X_train, weights_train, y_train = X_train[:args.num_training_samples], weights_train[:args.num_training_samples], y_train[:args.num_training_samples]

    print('Training data shape: {}\nTesting data shape:{}'.format(
        str(X_train.shape),
        str(X_test.shape)
    ))

    print('Training model ...')

    param_grid = json.loads(args.param_config.read())

    trees_grid = GridSearchCV(XGBRegressor(n_jobs = 1), 
            param_grid = param_grid, n_jobs = args.cores, scoring = 'neg_mean_squared_error', cv = 10)\
                .fit(X_train, y_train, sample_weight = weights_train)

    model = trees_grid.best_estimator_

    print('Best MSE achieved: {}'.format(str(-1 * trees_grid.best_score_)))

    prediction = model.predict(X_test)
    score = mean_squared_error(y_test, prediction, sample_weight = weights_test)

    print('Validation set MSE: {}'.format(str(score)))
    print('Saving model ...')
    
    dump(model, args.out_model)
        
    print('Done!')