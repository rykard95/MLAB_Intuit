"""
This file contains the ensemble regression code
for multiclass classification 
"""

import numpy as np
from pickle import load
from featurizer import generate_featurizer
from sklearn.linear_model import RidgeClassifierCV, LogisticRegressionCV,\
                                SGDClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from scipy.sparse import hstack

import pandas as pd
import seaborn as sn
from matplotlib import pyplot as plt

from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
from word2vec_model import featurize
from utils import import_data, generate_confusion_matrix

def generate_model(X, y, model='linear', regularizer='ridge'):
    if model == 'linear':
        if regularizer == 'ridge':
            clf = RidgeClassifierCV()
        else:
            raise ValueError("Unknown Regularizer")
    elif model == 'logistic':
            clf = LogisticRegressionCV()
    elif model == 'svm':
            clf = SGDClassifier()
    else:
        raise ValueError("Unexpected Model Type")
    
    clf.fit(X, y)
    return clf

def generate_ensemble(X, y, model='linear', regularizer=None):
    binary_ys = {label:None for label in np.unique(y)}
    models = {}
    for label in binary_ys:
        binary_ys[label] = binarize(label, y)
        models[label] = generate_model(X, binary_ys[label],\
                                model=model, regularizer=regularizer)
    return models

def predict(models, X):
    pass

def binarize(label, y):
    label = np.array([label for __ in range(len(y))])
    return (label == y).astype(int)

def run_test(mode='tfidf', model='linear', regularizer='ridge',\
                 train_data_path='data/intuit_data',\
                 test_data_path='data/intuit_test_data', augment=False):
    """
    Prints out score report of model under given featurization 
    """

    modes = {'bow': 'Bag of Words', 'tfidf': 'TF-IDF'}

    print("Using featurization " + modes[mode] + "...")
    print("Training " + model.upper() + " model with " + regularizer.upper() +\
                 " regularization...")
    
    if augment:
        print("Importing Word2Vec Model...")
        w2v_model = Word2Vec.load_word2vec_format('w2v.bin', binary=True)
        
         
    print("-------------------------------------------------------------------------")

    emails_train, y_train = import_data(train_data_path)
    transform = generate_featurizer(emails_train, mode=mode)
    X_train = transform(emails_train)
    eff_labels = np.unique(y_train)
    if augment:
        auxillary_features = [featurize(email, eff_labels, w2v_model)\
                                 for email in emails_train]
        auxillary_features = np.vstack(auxillary_features)
        X_train = hstack((X_train, auxillary_features))
    
    clf = generate_model(X_train, y_train, model=model,\
                             regularizer=regularizer)
    
    emails_test, y_test = import_data(test_data_path)
    X_test = transform(emails_test)
    if augment:
        auxillary_features = [featurize(email, eff_labels, w2v_model)\
                                 for email in emails_test]
        auxillary_features = np.vstack(auxillary_features)
        X_test = hstack((X_test, auxillary_features))
        
    y_pred = clf.predict(X_test)
    labels = np.unique(y_test)
    print(classification_report(y_test, y_pred))
    accuracy = str(np.around(accuracy_score(y_test, y_pred), decimals=3))
    print("accuracy: " + accuracy)
    if model != 'linear':
       regularizer = 'No'
    generate_confusion_matrix(y_test, y_pred, eff_labels, model.upper() + " model -  " + regularizer.upper() +" regularization - " + modes[mode] + " featurization - " + accuracy, model+'-'+mode+'-'+regularizer.lower()+'.png', True)
    print("-------------------------------------------------------------------------")

    

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-m', '--model', type=str, default='linear',\
                             help='Model type')
    parser.add_argument('-f', '--mode', type=str, default='tfidf',\
                             help='Featurization type') 
    parser.add_argument('-r', '--regularizer', type=str, default='ridge',\
                             help='Regularization type')
    parser.add_argument('-t', '--train_path', type=str, default='data/intuit_data',\
                             help='Path to training data')
    parser.add_argument('-s', '--test_path', type=str,
                             default='data/intuit_test_data',\
                             help='Path to testing data')
    parser.add_argument('-a', '--augment', type=bool, default=False,\
                             help='Augment the feature set')
    args = parser.parse_args() 
    run_test(mode=args.mode.lower(), model=args.model.lower(),\
                regularizer=args.regularizer.lower(),\
                train_data_path=args.train_path,\
                test_data_path=args.test_path, augment=args.augment)


