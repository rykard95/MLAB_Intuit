from pymongo import MongoClient

USERNAME = 'mlabintuit'
PASSWORD = 'mlab;123'
MONGODB_URI = 'mongodb://%s:%s@ds048319.mlab.com:48319' % (USERNAME, PASSWORD)

connection = MongoClient("ds048319.mlab.com", 48319)
db = connection['emails']
db.authenticate(USERNAME, PASSWORD)

def add_email(kvstore):
	db.unlabeled.insert_one(kvstore)
