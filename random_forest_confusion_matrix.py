import random
import utils
import seaborn as sn
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import linear_model
from sklearn.metrics import confusion_matrix
from math import sqrt
from pickle import load

if __name__ == '__main__':
    # get training corpus/labels
    emails = []
    label_set = []
    db = utils.get_local_db()
    for collection in db.collection_names():
        # the [:-6] is to account for the suffix '_clean'
        label_set.append(collection[:-6])
        for record in db.get_collection(collection).find():
            emails.append([collection] + [record['Text']])

    # vectorize corpus
    labels = [row[0][:-6] for row in emails]
    data = [row[1] for row in emails]
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(data)
    X = X.toarray()

    # create random forest
    forest = RandomForestClassifier(n_estimators = int(sqrt(len(X[0])))+1)
    forest.fit(X, labels)

    # read in and vectorize testing data
    with open('intuit_data', 'rb') as f:
        data = load(f)
    email_vectors = [vectorizer.transform([email['Text']]) for email in data['data']]
    email_labels = [label if label != 'negative' else 'negatives' for label in data['label']] # if-else to account for variation in naming

    # predict classification
    predicted_email_labels = [forest.predict(email_vector)[0] for email_vector in email_vectors]

    # generate confusion matrix: C_i,j is equal to the number of observations known to be in group i but predicted to be in group j
    cm = confusion_matrix(predicted_email_labels, email_labels, labels=label_set)
    df_cm = pd.DataFrame(cm, index=label_set, columns=label_set)
    plt.figure(figsize = (10,7))
    sn.heatmap(df_cm, annot=True)
    plt.savefig('random_forest_confusion_matrix.png', format='png')
