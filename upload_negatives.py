from pymongo import MongoClient
import numpy as np
import re
from IPython import embed
from utils import *

def clean(text, stopwords):
    text = text[2:-1]
    text = re.sub('On.*at.*wrote:.*', '', text)
    text = text.replace('\\n', ' ')
    text = text.replace('\\r', ' ')
    text = text.replace('>', ' ')
    text = re.sub("[^a-zA-Z0-9\s.?!]", '', text)
    text = ' '.join(word for word in text.split() if word not in stopwords)
    return text

def clean_emails(list_of_emails, stopwords):
    for email in list_of_emails:
        email['Text'] = clean(email['Text'], stopwords)
    return list_of_emails

def get_random_emails(n, db):
    emails = list(db.skipped.find())
    range_obj = np.arange(len(emails))
    indices = np.random.choice(range_obj, n, replace=False)
    returned_emails = []
    for i in indices:    
        returned_emails.append(emails[i])
    return returned_emails

def upload_emails(list_of_emails, db):
    collection = db.negatives
    for email in list_of_emails:
        try:
            collection.insert_one(email)
        except:
            collection.delete_one(email)
    print('Upload complete...')
    
if __name__ == "__main__":
    from nltk.corpus import stopwords
    stopwords = stopwords.words("english")

    remote_db = get_remote_db()
    
    local_client = MongoClient('localhost:27017')
    local_db = local_client.emails        
    emails = get_random_emails(100, local_db)
    emails = clean_emails(emails, stopwords)

    upload_emails(emails, remote_db)
        
