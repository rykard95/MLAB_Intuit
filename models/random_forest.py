import random
import utils
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import linear_model
from math import sqrt

def rf_model():
    percent_training = .70 # proportion of data to use for training

    #get emails from local mongodb
    emails = []
    db = utils.get_local_db()
    for collection in db.collection_names():
        for record in db.get_collection(collection).find():
            emails.append([collection] + [record['Text']])

    # shuffle and split emails
    random.shuffle(emails)
    training_set = emails[:int(percent_training * len(emails))]
    testing_set = emails[int(percent_training * len(emails)):]
    training_labels = [row[0] for row in training_set]
    training_data = [row[1] for row in training_set]
    testing_data = [row[1] for row in testing_set]

    # tf-idf vectorize training set
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(training_data)
    X = X.toarray()

    # tf-idf vectorize testing set
    vectorized_testing_data = [vectorizer.transform([email]) for email in testing_data]
    total = len(vectorized_testing_data)

    # create random forest
    forest = RandomForestClassifier(n_estimators = int(sqrt(len(X[0])))+1)
    forest.fit(X, training_labels)

    # generate and return predictions
    tagged_emails = []
    for i in range(total):
        tagged_emails.append([forest.predict(vectorized_testing_data[i])[0], testing_data[i]])

    return tagged_emails

def rf_categorize(email):
    # get training corpus
    emails = []
    db = utils.get_local_db()
    for collection in db.collection_names():
        for record in db.get_collection(collection).find():
            emails.append([collection] + [record['Text']])

    # vectorize corpus
    labels = [row[0] for row in emails]
    data = [row[1] for row in emails]
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(data)
    X = X.toarray()

    # vectorize input
    email_vector = vectorizer.transform([email])

    # create random forest and return prediction
    forest = RandomForestClassifier(n_estimators = int(sqrt(len(X[0])))+1)
    forest.fit(X, labels)
    return forest.predict(email_vector)[0]
