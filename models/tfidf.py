from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import linear_model
import utils

if __name__ == '__main__':

    emails_array = []
    label_array = []


    db = utils.get_local_db()
    for collection in db.collection_names():
        for record in db.get_collection(collection).find():
            emails_array.append(record['Text'])
            label_array.append(1 if collection == 'college' else 0)

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(emails_array)

    regr = linear_model.LinearRegression()
    regr.fit(X.toarray(), label_array)
    error = np.mean((regr.predict(X.toarray()) - label_array) ** 2)

    print(error)
