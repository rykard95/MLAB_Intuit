#!/usr/bin/env python

from sklearn.linear_model import RidgeClassifierCV
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.model_selection import GridSearchCV

from featurizer import generate_featurizer
from utils import import_data
from sklearn.metrics import accuracy_score, classification_report
import numpy as np

def generate_filter(X_train, y_train):
  
#    clf = RidgeClassifierCV(alphas=[0.01, 0.1, 1, 10]) 
    clf = RandomForestClassifier(n_jobs=4)
#    clf = AdaBoostClassifier()
    clf.fit(X_train, y_train)
    return clf
    
def test_filter(clf, transform, test_data_path):
    print("Testing event filter...")
    print("---------------------------------------------------------------------")
    email_texts, y_test = import_data(test_data_path)
    y_test[np.where(y_test != 'no event')] = 'event'
    X_test = transform(email_texts)
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(classification_report(y_test, y_pred))
    print("accuracy: " + str(accuracy))
    print("---------------------------------------------------------------------")
    

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-t', '--training_data_path', type=str,\
                             default="data/intuit_data", help="Path to training data")
    parser.add_argument('-s', '--test_data_path', type=str,\
                             default="data/intuit_test_data",\
                             help="Path to testing data")
    args = parser.parse_args()

    # Test for first level classifier
    email_texts, y_train = import_data(args.training_data_path)
    transform = generate_featurizer(email_texts)
    X_train = transform(email_texts)
    y_train[np.where(y_train != 'no event')] = 'event'

    clf = generate_filter(X_train, y_train)
    test_filter(clf, transform, args.test_data_path)
    
