#!/usr/bin/env python
from utils import import_data, generate_confusion_matrix
from featurizer import generate_featurizer
from event_filter import generate_filter
from linear_model import generate_model
import numpy as np
from IPython import embed
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier

class HierachicalClassifier:
    
    def __init__(self, model):
        self.filter = None
        self.clf = None
        self.model = model

    def fit(self, X, y):
        y_train_filter = y.copy()
        y_train_filter[np.where(y_train_filter != 'no event')] = 'event'
        self.filter = generate_filter(X_train, y_train_filter)

        event_indices = np.where(y != 'no event')
        X_train_clf = X_train[event_indices]
        y_train_clf = y[event_indices]
        if model == 'rf' or model == 'random forest':
            num_trees = int(np.sqrt(X_train_clf.shape[1]))+1
            self.clf = RandomForestClassifier(n_estimators=num_trees, n_jobs=-1)
        else:
            self.clf = generate_model(X_train_clf, y_train_clf, model='svm')
        
    def predict(self, X):
        if not self.clf:
            return "You must fit the model first"
    
        y_filter_pred = self.filter.predict(X)
        event_indices = np.where(y_filter_pred == 'event')[0]
        y_filter_pred = y_filter_pred[np.where(y_filter_pred == 'no event')]
        X_filtered = X[event_indices]
        if X_filtered.shape[0] == 0:
            return y_filter_pred

        y_clf_pred = self.clf.predict(X_filtered)
   
        return self.combine_predictions(y_filter_pred, y_clf_pred, event_indices)
 
    def combine_predictions(self, y_filter, y_clf, event_indices):
        y_pred = []
        y_filter = list(y_filter)
        y_clf = list(y_clf)
        for i in range(len(y_filter) + len(y_clf)):
            if i in event_indices:
                y_pred.append(y_clf.pop(0))
            else:
                y_pred.append(y_filter.pop(0))
        return np.array(y_pred)
    
if __name__ == "__main__":
    from argparse import ArgumentParser
    
    email_texts, y_train = import_data('data/intuit_data')
    transform = generate_featurizer(email_texts)
    X_train = transform(email_texts)

    model = HierachicalClassifier('rf')
    model.fit(X_train, y_train) 

    email_texts, y_test = import_data('data/intuit_test_data')
    X_test = transform(email_texts)
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))
    print("accuracy: " + str(accuracy_score(y_test, y_pred)))
    
    generate_confusion_matrix(y_test, y_pred, np.unique(y_train),\
                                 'Hierachical Classification', 'hc.png', True)
    
     
     
     
    
