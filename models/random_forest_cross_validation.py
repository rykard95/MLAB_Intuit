import utils
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import linear_model
from sklearn.cross_validation import cross_val_score
from math import sqrt

if __name__ == '__main__':
    num_samples = 100 # number of random forests to compute and then average

    # get emails from local mongodb
    emails = []
    db = utils.get_local_db()
    for collection in db.collection_names():
        for record in db.get_collection(collection).find():
            emails.append([collection] + [record['Text']])

    # create labels and vectorize data
    labels = [row[0] for row in emails]
    vectorizer = TfidfVectorizer()
    data = vectorizer.fit_transform([row[1] for row in emails]).toarray()

    # create random forst and perform cross validation
    forest = RandomForestClassifier(n_estimators = int(sqrt(len(data[0])))+1)
    scores = cross_val_score(forest, data, labels, cv=num_samples)

    # write output to file
    output = open('random_forest_cross_validation.txt', 'w')
    for i in range(len(scores)):
        print(str(i)+": "+str(scores[i]), file=output)
    output.close()
