import random
import utils
import seaborn as sn
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import linear_model
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from math import sqrt
from pickle import load

if __name__ == '__main__':
    # get training corpus/labels
    with open('data/intuit_data', 'rb') as f:
        data = load(f)
    emails = [email['Text'] for email in data['data']]
    labels = [label for label in data['label']]
    label_set = list(set(labels))

    # vectorize corpus
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(emails)
    X = X.toarray()

    # create random forest
    forest = RandomForestClassifier(n_estimators = int(sqrt(len(X[0])))+1, n_jobs=4)
    forest.fit(X, labels)

    # read in and vectorize testing data
    with open('data/intuit_test_data', 'rb') as f:
        data = load(f)
    email_vectors = [vectorizer.transform([email['Text']]) for email in data['data']]
    email_labels = [label for label in data['label']]

    # predict classification
    predicted_email_labels = [forest.predict(email_vector)[0] for email_vector in email_vectors]

    # generate confusion matrix: C_i,j is equal to the number of observations known to be in group i but predicted to be in group j
    cm = confusion_matrix(predicted_email_labels, email_labels, labels=label_set)
    df_cm = pd.DataFrame(cm, index=label_set, columns=label_set)
    plt.figure(figsize = (10,7))
    sn.heatmap(df_cm, annot=True)
    plt.savefig('random_forest_confusion_matrix.png', format='png')
    print("------------------------------------------------------------")
    accuracy = accuracy_score(predicted_email_labels, email_labels)
    print(classification_report(predicted_email_labels, email_labels))
    print("accuracy: " + str(accuracy))
    print("------------------------------------------------------------")
