from IPython import embed
from pymongo import MongoClient

def get_labels(path="labels.txt"):
    labels = []
    with open(path, 'r') as f:
        line = f.readline()
        line = line.split(',')
    for el in line:
        labels.append(el.strip())
    return labels

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
 
