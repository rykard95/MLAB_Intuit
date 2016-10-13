from pymongo import MongoClient

USERNAME = 'mlabintuit'
PASSWORD = 'mlab;123'
MONGODB_URI = 'mongodb://%s:%s@ds048319.mlab.com:48319' % (USERNAME, PASSWORD)

client = MongoClient('localhost:27017')

db = client.emails

def add_email(kvstore):
	db.unlabeled.insert_one(kvstore)
