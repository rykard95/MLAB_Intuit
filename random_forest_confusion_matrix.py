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

if __name__ == '__main__':
    percent_training = .30 # proportion of data to use for training

    # get emails and labels from local mongodb
    emails = []
    label_set = []
    db = utils.get_local_db()
    for collection in db.collection_names():
        label_set.append(collection)
        for record in db.get_collection(collection).find():
            emails.append([collection] + [record['Text']])

    # shuffle and split emails
    random.shuffle(emails)
    training_set = emails[:int(percent_training * len(emails))]
    testing_set = emails[int(percent_training * len(emails)):]
    training_labels = [row[0] for row in training_set]
    training_data = [row[1] for row in training_set]
    testing_labels = [row[0] for row in testing_set]
    testing_data = [row[1] for row in testing_set]

    # tf-idf vectorize training set
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(training_data)
    X = X.toarray()

    # tf-idf vectorize testing set
    vectorized_testing_data = [vectorizer.transform([email]) for email in testing_data]
    total = len(vectorized_testing_data)

    # create random forest and compute predictions
    forest = RandomForestClassifier(n_estimators = int(sqrt(len(X[0])))+1)
    forest.fit(X, training_labels)
    predictions = []
    for i in range(len(vectorized_testing_data)):
        predictions.append(forest.predict(vectorized_testing_data[i]))

    # generate confusion matrix: C_i,j is equal to the number of observations known to be in group i but predicted to be in group j
    cm = confusion_matrix(predictions, testing_labels, labels=label_set)
    label_set = [label[:-6] for label in label_set]
    df_cm = pd.DataFrame(cm, index=label_set, columns=label_set)
    plt.figure(figsize = (10,7))
    sn.heatmap(df_cm, annot=True)
    plt.savefig('random_forest_confusion_matrix.png', format='png')
