from pymongo import MongoClient

USERNAME = 'mlabintuit'
PASSWORD = 'mlab;123'
MONGODB_URI = 'mongodb://%s:%s@ds048319.mlab.com:48319' % (USERNAME, PASSWORD)

local_client = MongoClient('localhost:27017')
local_db = local_client.emails

remote_client = MongoClient("ds048319.mlab.com", 48319)
remote_db = remote_client['emails']
remote_db.authenticate(USERNAME, PASSWORD)
remote_db = remote_client.emails
negatives = remote_db.negatives

for record in negatives.find():
    local_db.negatives_clean.insert_one(record)
