from pymongo import MongoClient

client = MongoClient('localhost:27017')

db = client.emails

def add_email(kvstore):
	db.unlabeled.insert_one(kvstore)
	