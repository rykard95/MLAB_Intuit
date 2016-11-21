from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import linear_model
import random
import utils
from math import sqrt

if __name__ == '__main__':
    num_samples = 100 # number of random forests to compute and then average
    percent_training = .80 # proportion of data to use for training
    avg = 0

    # get emails from local mongodb
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
    testing_labels = [row[0] for row in testing_set]
    testing_data = [row[1] for row in testing_set]

    # tf-idf vectorize training set
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(training_data)
    X = X.toarray()

    # create num_samples random forests
    for i in range(num_samples):
        forest = RandomForestClassifier(n_estimators = int(sqrt(len(X[0])))+1)
        forest.fit(X, training_labels)
        vectorized_testing_data = [vectorizer.transform([email]) for email in testing_data]
        total = len(vectorized_testing_data)
        correct = 0

        # compute accuracy of tests and average
        for k in range(total):
            if forest.predict(vectorized_testing_data[k]) == testing_labels[k]:
                correct += 1
        avg += (correct/total)

    print("average: "+str((avg/num_samples)))
