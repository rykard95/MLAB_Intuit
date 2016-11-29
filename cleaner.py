#cleans the body of all the emails in the MongoDB database
from pymongo import MongoClient
from labeller import print_email
import re
import hashlib


USERNAME = 'mlabintuit'
PASSWORD = 'mlab;123'
MONGODB_URI = 'mongodb://%s:%s@ds048319.mlab.com:48319' % (USERNAME, PASSWORD)

stop_words = set(['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'I',
'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at', 'this', 'but',
'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my'
, 'one', 'all', 'would', 'there', 'their', 'what', 'so', 'up', 'out', 'if',
'about', 'who', 'get', 'which', 'go', 'me', 'when', 'make', 'can', 'like',
'time', 'no', 'just', 'him', 'know', 'take', 'people', 'into', 'year',
'your', 'good', 'some', 'could', 'them', 'see', 'other', 'than', 'then',
'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also', 'back',
'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well', 'way',
'even', 'new', 'want', 'because', 'any', 'these', 'give', 'day', 'most', 'us'])


if __name__ == "__main__":
    local_client  = MongoClient('localhost:27017')
    local_db = local_client.emails

    remote_client = MongoClient("ds048319.mlab.com", 48319)
    remote_db = remote_client['emails']
    remote_db.authenticate(USERNAME, PASSWORD)
    remote_db = remote_client.emails

    OLD_COLLECTIONS = [remote_db.moving, remote_db.pet, remote_db.college, remote_db.tuition, remote_db.job, remote_db.medical,
			   remote_db.wedding, remote_db.funeral, remote_db.baby, remote_db.grad, remote_db.travel, remote_db.application]

    CLEAN_COLLECTIONS = [local_db.moving_clean, local_db.pet_clean, local_db.college_clean, local_db.tuition_clean, local_db.job_clean, local_db.medical_clean,
			   local_db.wedding_clean, local_db.funeral_clean, local_db.baby_clean, local_db.grad_clean, local_db.travel_clean, local_db.application_clean]

    for collection in CLEAN_COLLECTIONS:
        collection.remove()

    for collection in OLD_COLLECTIONS:
        for record in collection.find():
            new_record = record.copy()
            temp_text = new_record['Text']

            temp_text = temp_text[2:-1] #removes first 2 characters and last character


            temp_text = re.sub('On.*at.*wrote:.*', '', temp_text) #removes everything in the text that is involved with a reply message


            temp_text = re.sub('---------- Forwarded message ----------.*\*', '', temp_text) #removes everything in the text that is involved with a forward message

            temp_text = temp_text.replace('\\n', ' ')
            temp_text = temp_text.replace('\\r', ' ')
            temp_text = temp_text.replace('>', ' ')


            tokenized_email = temp_text.split()
            tokenized_email = [word for word in tokenized_email if word not in stop_words]
            cleaned_email = ' '.join(tokenized_email)

            new_record['Text'] = cleaned_email

            CLEAN_COLLECTIONS[OLD_COLLECTIONS.index(collection)].insert_one(new_record)
