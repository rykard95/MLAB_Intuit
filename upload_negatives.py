from pymongo import MongoClient
import numpy as np
import re
from IPython import embed
from utils import *

def clean_emails(list_of_emails, stopwords):
    for email in list_of_emails:
        email['Text'] = clean(email['Text']) 
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
    local_db = get_local_db()        
    emails = get_random_emails(300, local_db)
    emails = clean_emails(emails, stopwords)

    upload_emails(emails, remote_db)
        
