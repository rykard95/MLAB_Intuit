from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import linear_model
import random
import utils

if __name__ == '__main__':
    num_samples = 100
    max_estimators = 1000
    for i in range(1, max_estimators+1):
        avg = 0
        for j in range(num_samples):
            emails = []
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
            forest = RandomForestClassifier(n_estimators = i) #See http://www.iro.umontreal.ca/~nie/IFT6255/class-email.pdf
            forest.fit(X.toarray(), training_labels)
            vectorized_testing_data = [vectorizer.transform([email]) for email in testing_data]
            total = len(vectorized_testing_data)
            correct = 0
            for k in range(total):
                if forest.predict(vectorized_testing_data[k]) == testing_labels[k]:
                    correct += 1
            avg += (correct/total)
        print("i: "+str(i)+", %: "+str((avg/num_samples)))
