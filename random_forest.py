from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import linear_model
import random
import utils
from math import sqrt

if __name__ == '__main__':
    emails = []
    avg = 0
    db = utils.get_local_db()
    for collection in db.collection_names():
        for record in db.get_collection(collection).find():
            emails.append([collection] + [record['Text']])
    random.shuffle(emails)
    percent_training = .80
    training_set = emails[:int(percent_training * len(emails))]
    testing_set = emails[int(percent_training * len(emails)):]
    training_labels = [row[0] for row in training_set]
    training_data = [row[1] for row in training_set]
    testing_labels = [row[0] for row in testing_set]
    testing_data = [row[1] for row in testing_set]
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(training_data)
    X = X.toarray()
    num_samples = 100
    for i in range(num_samples):
        forest = RandomForestClassifier(n_estimators = int(sqrt(len(X[0]))))
        forest.fit(X, training_labels)
        vectorized_testing_data = [vectorizer.transform([email]) for email in testing_data]
        total = len(vectorized_testing_data)
        correct = 0
        for k in range(total):
            if forest.predict(vectorized_testing_data[k]) == testing_labels[k]:
                correct += 1
        avg += (correct/total)
    print("trees: "+str(i)+", %: "+str((avg/num_samples)))
