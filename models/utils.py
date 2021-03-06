from IPython import embed
from pymongo import MongoClient
import sklearn.feature_extraction.stop_words as sw
from sklearn.metrics import confusion_matrix
import pandas as pd
import seaborn as sn
from matplotlib import pyplot as plt
import re 
from pickle import load, dump
import numpy as np

STOPWORDS = sw.ENGLISH_STOP_WORDS 
def clean(text, stopwords=STOPWORDS):
    text = text[2:-1]
    text = re.sub('On.*at.*wrote:.*', '', text)
    text = re.sub('---------- Forwarded message ----------.*\*', '', text)
    text = text.replace('\\n', ' ')
    text = text.replace('\\r', ' ')
    text = text.replace('>', ' ')
    text = re.sub("[^a-zA-Z0-9\s.?!]", '', text)    
    text = ' '.join(word for word in text.split() if word not in stopwords and len(word) < 25) 
    return text    

def get_labels(path="config/labels.txt"):
    labels = []
    with open(path, 'r') as f:
        line = f.readline()
        line = line.split(',')
    for el in line:
        labels.append(el.strip())
    return labels

def get_label_words(path="config/label_words.txt"):
    label_words = {}
    with open(path, 'r') as f:
        for line in f.readlines():
            label, words = line.split(":")
            label_words[label.strip()] = [label] + [el.strip() for el in words.split(',')]
    return label_words
            
def get_remote_db():
    USERNAME = 'mlabintuit'
    PASSWORD = 'mlab;123'
    remote_client = MongoClient('ds048319.mlab.com', 48319)
    remote_db = remote_client['emails']
    remote_db.authenticate(USERNAME, PASSWORD)
    return remote_db

def get_local_db():
    local_client = MongoClient('localhost:27017')
    return local_client.emails

def get_all_clean_emails(db, get_skipped=False, get_label=False):
    if get_skipped and get_label:
        raise ValueError
    collection_names = db.collection_names()
    while collection_names:
        name = collection_names.pop(0)
        if 'clean' not in name:
            continue
        collection = db.get_collection(name)
        emails = list(collection.find())
        name = name.replace('_clean', '')
        while emails:
            email = emails.pop(0)
            email['Text'] = clean(email['Text'])
            if get_label:
                yield email, name
            else:
                yield email
    if get_skipped:
        collection = db.get_collection('skipped')
        emails = list(collection.find())
        while emails:
            yield emails.pop(0)

def get_all_emails(db):
    collection_name = db.collection_names()
    while collection_name:
        name = collection_name.pop(0)
        collection = db.get_collection(name)
        emails = list(collection.find())
        while emails:
            email = emails.pop(0)
            try:
                email['Text'] = clean(email['Text'])
            except:
                continue
            yield email

def get_all_emails_in_collection(db, collection):
    collection = db.get_collection(collection)
    emails = list(collection.find())
    for email in emails:
        email['Text'] = clean(email['Text'])
        if not email['Text']:
            continue
        yield email

def import_data(path):
    with open(path, 'rb') as f:
        email_data = load(f)
    
    email_texts = [email['Text'] for email in email_data['data']]
    return email_texts, email_data['label']

def label_replace(path, target, val):
    with open(path, 'rb') as f:
        data = load(f)

    labels = np.array(data['label'])
    labels[np.where(labels == target)] = val
    data['label'] = labels
    
    with open(path, 'wb') as f:
        dump(data, f, protocol=2)

def generate_confusion_matrix(y_test, y_pred, labels, title, filename, show=False):
    cm = confusion_matrix(y_test, y_pred, labels=labels)
    df_cm = pd.DataFrame(cm, index=labels, columns=labels)
    plt.figure(figsize=(12,8))
    ax = sn.heatmap(df_cm, annot=True)
    plt.ylabel("Actual Label", fontsize=14, fontweight='bold')
    plt.xlabel("Predicted Label", fontsize=14, fontweight='bold')
    plt.title(title, fontsize=16, fontweight='bold')
    
    ttl = ax.title
    ttl.set_position([0.5, 1.03])
    plt.savefig(filename)
   
    if show:
        plt.show()
    
