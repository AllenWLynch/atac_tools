import argparse
import sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
import numpy as np
from sklearn.metrics import accuracy_score
from joblib import dump

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-l','--labels',type = argparse.FileType('r'), required= True)
    parser.add_argument('-m','--matrix',type = str, required=True)
    parser.add_argument('-o','--out_model', type = str, required = True)
    parser.add_argument('-c','--cores',type = int, required= True)
    parser.add_argument('--test_size', type = float, default = 0.1)
    parser.add_argument('--num_training_samples', type = int, default = -1)

    args = parser.parse_args()

    assert(args.cores > 0)

    print('Loading data ...')

    labels = np.array([
        int(label.strip()) for label in args.labels 
    ])

    features = np.load(args.matrix)

    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size = args.test_size, random_state = 1234)

    if args.num_training_samples > 0:
        X_train, y_train = X_train[:args.num_training_samples], y_train[:args.num_training_samples]

    print('Training data shape: {}\nTesting data shape:{}'.format(
        str(X_train.shape),
        str(X_test.shape)
    ))

    print('Training model ...')

    param_grid = {
        'C' : [0.01,0.1,1.0,10.0,100.0],
        'l1_ratio' : [0.01, 0.25,0.5,0.75,0.99],
    }
    logistic_regression_grid = GridSearchCV(
        LogisticRegression(random_state = 1234, solver = 'saga', penalty = 'elasticnet'), 
            param_grid = param_grid, n_jobs = 4, scoring = 'roc_auc', cv = 5)\
                .fit(X_train, y_train)

    model = logistic_regression_grid.best_estimator_

    print('Best AUC achieved: {}'.format(str(logistic_regression_grid.best_score_)))

    prediction = model.predict(X_test)
    accuracy = accuracy_score(y_test, prediction)

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


