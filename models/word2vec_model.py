from pymongo import MongoClient
from gensim.models import Word2Vec
import numpy as np
from IPython import embed
from utils import *
from operator import add
from scipy.io import savemat, loadmat
from histogram_plotter import generate_histograms

def score(text, label, model, func, expand_label):
    score = 0
    text = text.split(' ')
    scale = 1.0
    if expand_label:
        label = get_label_words()[label]
    else:
        label = [label]

    if func == add:
        scale = float(len(text))
    for word in text:
        for l in label:
            try:
                score = func(model.similarity(word, l), score)
            except (KeyError, AttributeError) as e:
                continue
    return score / scale


def generate_scores(collection, label, model, func=add):
    score_vector = []
    for datum in collection.find():
        body = clean(datum['Text'])
        subject = clean(datum['Subject'])
        body_score = score(body, label, model, func)
        subject_score = score(subject, label, model, func)
        score_vector.append(body_score + subject_score)
    return np.array(score_vector)

def generate_cross_scores(db, model, func, expand_label):
    score_matrix = []
    labels = get_labels()
    for datum, real_label in get_all_clean_emails(db, get_label=True):
        score_matrix.append(featurize(datum, labels) + [real_label])
    score_matrix = np.vstack(score_matrix)
    score_mat = {'score_matrix': score_matrix}
    savemat('score_matrix', score_mat)
    return score_matrix

def get_next_label_collection(db):
    collection_names = db.collection_names()
    while collection_names:
        name = collection_names.pop(0)
        if 'clean' not in name:
            continue
        collection = db.get_collection(name)
        label = name.replace('_clean', '')
        yield collection, label
            
def results(db, model, comp_func, k=1, expand_label=False):
    if k < 1:
        raise ValueError
    score_matrix = generate_cross_scores(local_db, model, comp_func, expand_label)
    labels = np.array(get_labels())
    
    # Sort scores in descending order
    top_score_ind = np.argsort(score_matrix[:, :score_matrix.shape[1]-2,], axis=1)
    top_score_ind = np.fliplr(top_score_ind)

    # Get top K guesses
    y_hat = []
    for i in range(k):
        y_hat.append(labels[top_score_ind[:,i]])
    y_hat = np.vstack(y_hat).T

    y = score_matrix[:, score_matrix.shape[1]-1]
    score_pool = []
    for i in range(k):
        score_pool.append((y == y_hat[:, i]).astype(int))
    score_pool = np.vstack(score_pool).T

    r = np.max(score_pool, axis=1)
    return float(np.count_nonzero(r)) / float(len(r)), score_matrix
    
def generate_model(db=None, corpus='google'):
    if corpus == "google":
        return Word2Vec.load_word2vec_format('w2v.bin', binary=True)
    elif corpus == "emails":
        emails = list(get_all_emails(db))
        sentences = []
        for email in emails:
            sentences += create_sentences(email['Text'])
        model = Word2Vec(sentences, size=200)    
        return model

def featurize(email, labels):
	score_vector = []
    body = clean(datum['Text'])
    subject = clean(datum['Subject'])
    for label in labels:            
        body_score = score(body, label, model, func, expand_label)
        subject_score = score(subject, label, model, func, expand_label)
        score_vector.append((body_score + subject_score)/2.0)
    return score_vector


def get_to(email):
    name = email['To'].split()
    if name:
        name = name[0]
        name = name.split('@')[0]
        name = clean(name).lower()
    return name

def get_all_to(db):
    emails = list(get_all_clean_emails(db, get_label=False))
    names = []
    for email in emails:    
        names.append(get_to(email))
    names = np.unique(names)
    names = [name for name in names if '?' not in name\
                     and name != '[]' and len(name)<24]
    return np.unique(names) 

if __name__ == "__main__":
    k = 1
    print("Importing model...")
    local_db = get_local_db();
    model = generate_model(local_db)
    print("Generating scores")
    r, score_matrix = results(local_db, model, max, k=k, expand_label=True)
    print("For k = " + str(k) + ", our match rate was: " + str(r))
    #score_matrix = loadmat('score_matrix')['score_matrix']
    #generate_histograms(score_matrix)
    
