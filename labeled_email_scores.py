from pymongo import MongoClient
from gensim.models import Word2Vec
import numpy as np
from IPython import embed
from nltk.corpus import stopwords

USERNAME = 'mlabintuit'
PASSWORD = 'mlab;123'
MONGODB_URI = 'mongodb://%s:%s@ds048319.mlab.com:48319' % (USERNAME, PASSWORD)

stopwords = stopwords.words("english")

def score(text, label, model):
    score = 0
    text = text.split(' ')
    for word in text:
        try:
            score += model.similarity(word, label)
        except KeyError as e:
            continue
    return score / float(len(text))

def remove_stop_words(text):
    return ' '.join([word for word in text.split() if word not in stopwords])    

def generate_scores(collection, label, model):
    score_vector = []
    for datum in collection.find():
        body = remove_stop_words(datum['Text'])
        subject = remove_stop_words(datum['Subject'])
        body_score = score(body, label, model)
        subject_score = score(subject, label, model)
        score_vector.append(body_score + subject_score)
    return np.array(score_vector)


def get_next_label_collection(db):
    collection_names = db.collection_names()
    while collection_names:
        name = collection_names.pop(0)
        if 'clean' not in name:
            continue
        collection = db.get_collection(name)
        label = name.replace('_clean', '')
        yield collection, label
            
    
if __name__ == "__main__":
    
    print("Importing model...")
    model = Word2Vec.load_word2vec_format('w2v.bin', binary=True)
    
    print("Connecting to local database...")
    local_client = MongoClient('localhost:27017')
    local_db = local_client.emails
    scores = {label: generate_scores(collection, label, model) for collection,label in get_next_label_collection(local_db)}

    

    
