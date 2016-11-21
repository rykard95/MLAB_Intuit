from pymongo import MongoClient
from gensim.models import Word2Vec
import numpy as np
from IPython import embed
from utils import *
from operator import add
from model import *
from matplotlib import pyplot as plt
from pylab import savefig
from scipy.io import savemat, loadmat

USERNAME = 'mlabintuit'
PASSWORD = 'mlab;123'
MONGODB_URI = 'mongodb://%s:%s@ds048319.mlab.com:48319' % (USERNAME, PASSWORD)

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
        score_vector = []
        body = clean(datum['Text'])
        subject = clean(datum['Subject'])
        for label in labels:            
            body_score = score(body, label, model, func, expand_label)
            subject_score = score(subject, label, model, func, expand_label)
            score_vector.append(body_score + subject_score)
        score_matrix.append(score_vector + [real_label])
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

def generate_histograms(score_matrix):
    # Label to number mapping
    labels = get_labels()
    label_to_number = {a[1]:a[0] for a in list(enumerate(labels))} 
    # Initialize the Histograms
    class_rank = {i:[] for i in range(len(labels))}
    correct_rank = []
    guess_rank = []
    each_class_correct_rank = {i:0 for i in range(len(labels))}
    correct_raw_scores = {i:[] for i in range(len(labels))}
    incorrect_raw_scores = {i:[] for i in range(len(labels))} 

    # Iterate through score matrix
    for score_vector in score_matrix:
        correct_label = label_to_number[str(score_vector[-1]).strip()] 
        score_vector = score_vector[:-1].astype(float)
        top_score_ind = np.argsort(score_vector)[::-1]
        score_vector = np.sort(score_vector)[::-1]
        rank = int(np.where(top_score_ind == correct_label)[0])
        
        # Add to Histogram
        correct_rank.append(correct_label)
        guess_rank.append(top_score_ind[0])
        class_rank[correct_label].append(rank)
        if correct_label == top_score_ind[0]:
            correct_raw_scores[correct_label].append(score_vector[0])
        else:

            incorrect_raw_scores[correct_label].append(score_vector[rank])
    
    plot_correct_hist(correct_rank)
    plot_guess_hist(guess_rank)
    for i in range(len(labels)):
        plot_label_rank(class_rank[i], labels[i])
        plot_correct_class_scores(correct_raw_scores[i], labels[i])
        plot_incorrect_class_scores(incorrect_raw_scores[i], labels[i])
    plot_correct_scores(correct_raw_scores)
    plot_incorrect_scores(incorrect_raw_scores)
          
def plot_guess_hist(guess_hist):
    bins = np.arange(13) - 0.5    
    n, bins, patches = plt.hist(guess_hist, bins, normed=1, facecolor='green', alpha=0.75) 
    labels = get_labels()
    plt.title("Guess Labels Histogram")
    plt.xlabel("Label")
    plt.xticks(np.arange(len(labels)), labels, rotation='vertical')
    plt.ylabel("Frequency of Labels")
    plt.tight_layout()
    savefig("w2v_figs/guess_hist.png")
    plt.clf()

def plot_correct_hist(correct_hist):
    bins = np.arange(13) - 0.5    
    n, bins, patches = plt.hist(correct_hist, bins, normed=1, facecolor='green', alpha=0.75) 
    labels = get_labels()
    plt.title("Correct Labels Histogram")
    plt.xlabel("Label")
    plt.xticks(np.arange(len(labels)), labels, rotation='vertical')
    plt.ylabel("Frequency of Labels")
    plt.tight_layout()
    savefig("w2v_figs/correct_hist.png")
    plt.clf()
    #plt.show()

def plot_label_rank(ranks, label):
    bins = np.arange(13) - 0.5
    n, bins, patches = plt.hist(ranks, bins, normed=1, facecolor='blue', alpha=0.75) 
    labels = np.arange(12)
    plt.title("Ranks for Label: " + label)
    plt.xticks(np.arange(len(labels)), labels)
    plt.ylabel("Frequency Rank Appearance")
    plt.tight_layout()
    savefig("w2v_figs/rank_" + label+'.png')
    plt.clf()
    #plt.show()
    
def plot_correct_scores(correct_scores):
    scores = np.array([a for v in correct_scores.values() for a in v])
    n, bins, patches = plt.hist(scores, 50, normed=1, facecolor='blue', alpha=0.75)
    plt.title("Histogram of Correct Label Scores")
    plt.ylabel("Frequency of scores")
    plt.xlabel("Score")
    plt.tight_layout()
    savefig('w2v_figs/correct_scores.png')
    #plt.show()
    plt.clf()

def plot_incorrect_scores(incorrect_scores):
    scores = np.array([a for v in incorrect_scores.values() for a in v])
    n, bins, patches = plt.hist(scores, 50, normed=1, facecolor='red', alpha=0.75)
    plt.title("Histogram of Incorrect Label Scores")
    plt.ylabel("Frequency of scores")
    plt.tight_layout()
    savefig('w2v_figs/Incorrect_scores.png')
    #plt.show()
    plt.clf()

def plot_correct_class_scores(correct_scores, label):
    scores = correct_scores
    n, bins, patches = plt.hist(scores, 50, normed=1, facecolor='blue', alpha=0.75)
    plt.title("Histogram of Correct Label Scores for " + label)
    plt.ylabel("Frequency of scores")
    plt.tight_layout()
    savefig('w2v_figs/Correct_scores_'+ label +'.png')
    #plt.show()
    plt.clf()
    
    pass

def plot_incorrect_class_scores(incorrect_scores, label):
    scores = incorrect_scores 
    n, bins, patches = plt.hist(scores, 50, normed=1, facecolor='red', alpha=0.75)
    plt.title("Histogram of Incorrect Label Scores for " + label)
    plt.ylabel("Frequency of scores")
    plt.tight_layout()
    savefig('w2v_figs/Incorrect_scores_'+label+'.png')
    #plt.show()
    plt.clf()

if __name__ == "__main__":
    k = 3
    print("Importing model...")
    local_db = get_local_db();
#    model = generate_model(local_db, 'emails')
#    model = generate_model(local_db)
    print("Generating scores")
#    r, score_matrix = results(local_db, model, max, k=k, expand_label=True)
#    print("For k = " + str(k) + ", our match rate was: " + str(r))
#    names = get_all_to(local_db) 
    score_matrix = loadmat('score_matrix')['score_matrix']
    generate_histograms(score_matrix)
    
