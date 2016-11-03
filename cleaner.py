#cleans the body of all the emails in the MongoDB database
from pymongo import MongoClient
from labeller import print_email
import re
from nltk.corpus import stopwords

stopwords = stopwords.words("english")

USERNAME = 'mlabintuit'
PASSWORD = 'mlab;123'
MONGODB_URI = 'mongodb://%s:%s@ds048319.mlab.com:48319' % (USERNAME, PASSWORD)

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
    for collection in OLD_COLLECTIONS:
        for record in collection.find():
            new_record = record.copy()
            temp_text = new_record['Text']

            temp_text = temp_text[2:-1] #removes first 2 characters and last character

            # reply_separator = '\\n\\nOn'
            # temp_text = temp_text.split(reply_separator, 1)[0]

            temp_text = re.sub('On.*at.*wrote:.*', '', temp_text) #removes everything in the text that is involved with a reply message

            # forward_separator = '*\\n\\n'
            # temp_text = temp_text.split(forward_separator, 1)[-1]

            temp_text = re.sub('---------- Forwarded message ----------.*\*', '', temp_text) #removes everything in the text that is involved with a forward message

            temp_text = temp_text.replace('\\n', ' ')
            temp_text = temp_text.replace('\\r', ' ')
            temp_text = temp_text.replace('>', ' ')
            temp_text = ' '.join(word for word in temp_text.split() if word not in stopwords)

            new_record['Text'] = temp_text

            CLEAN_COLLECTIONS[OLD_COLLECTIONS.index(collection)].insert_one(new_record)
