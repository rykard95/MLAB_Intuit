from utils import *
from featurizer import generate_featurizer
from pickle import load
import numpy as np
from sklearn.ensemble import RandomForestClassifier as rf
from sklearn.metrics import accuracy_score

if __name__ == "__main__":
    with open('intuit_data', 'rb') as f:
        email_data = load(f)
   
    print("Testing TF-IDF Featurizer") 
    email_texts = [email['Text'] for email in email_data['data']]
    f = generate_featurizer(email_texts, mode='tfidf')
    X = f(email_texts)
    labels = email_data['label']
    app = np.array(['application' for __ in range(len(labels))])
    y = (labels == app).astype(int)

    clf = rf()
    clf.fit(X, y)
    
    y_pred = clf.predict(X)
    print("The accuracy score of recall is: " + str(accuracy_score(y, y_pred))) 
    print("Test passed")
