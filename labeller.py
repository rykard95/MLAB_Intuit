#labeller.py
from pymongo import MongoClient

def get_first_email(collection):
	"""Gets relevant values of first email in a collection"""
	email = collection.find().limit(1)[0]
	relevant_values = ['subject', 'from', 'to', 'body']
	return {val: email[val] for val in relevant_values}

def get_first_email_id(collection):
	"""Gets id of first email in a collection"""
	email = collection.find().limit(1)[0]
	return email['_id']

def print_email(email):
	"""Prints given email dictionary"""
	print("----------------------------- Email ----------------------------------")
	print(email['subject'])
	print('FROM: ' + email['from'] + ' TO: ' + email['to'])
	print('')
	print(email['body'])
	print("----------------------------------------------------------------------")

def get_label(labels):
	"""Queries user for label"""
	for i, elem in enumerate(labels):
		print("[" + str(i) + "] " + elem)
	print('')
	index = input("Pick a number: ")
	while not index.isnumeric() or int(index) < 0 or int(index) >= len(labels):
		print("That is not a valid option.")
		index = input("Pick a number: ")
	return labels[int(index)]

def get_features(label, features):
	"""Queries user for features associated with a given label"""
	feature_responses = {}
	for feature in features[label]:
		response = input(feature + ' ')
		feature_responses[feature] = response
	return feature_responses

if __name__ == "__main__":
	#Instantiate connection to DB
	client = MongoClient('localhost:27017')
	db = client.emails
	#Declare constants
	LABELS = ['Moving Event', 'Pet Adoption', 'Attending College', 'Tuition Event',
	 		  'Job/Internship Event', 'Medical Event', 'Wedding', 'Funeral',
			  'Baby', 'Graduation', 'Travel Event', 'College/Scholarship Applications']
	FEATURES_ARR = [['Where was the move?', 'When was the move?'],
					['What kind of pet?'],
					['Which family member went to college?', 'Which college did they go to?'],
					['What was the cost of tuition?', 'Was there any financial aid?'],
					['Which company was involved?', 'How long is the internship? (Put \'N/A\' if not internship)', 'Where is the job?'],
					['Was it an injury\'[0]\' or illness\'[1]\'', 'Was there a hospitalization? (1 or 0)', 'How long did it last?', 'What was the severity?'],
					['Who was involved with the wedding?', 'When was the wedding?'],
					['Who was involved with the funeral?', 'When was the funeral?'],
					['When did this occur?'],
					['When was the graduation?', 'Where did you graduate from?'],
					['Where did you travel to?', 'How long was the travel?', 'How much was the travel costs?', 'Was it business or personal? (1 or 0)'],
					['Which college/scholarship was the acceptance from?', 'What is the acceptance status?']]
	DBS_ARR = [db.moving, db.pet, db.college, db.job, db.tuition, db.medical,
			   db.wedding, db.funeral, db.baby, db.grad, db.travel, db.application]
	assert (len(FEATURES_ARR) == len(LABELS) and len(DBS_ARR) == len(LABELS)), 'Missing entry in one or more of the constant arrays.'
	#Generate dictionaries
	FEATURES = {LABELS[i]: FEATURES_ARR[i] for i in range(len(LABELS))}
	DBS = {LABELS[i]: DBS_ARR[i] for i in range(len(LABELS))}
	#Iterate and classify emails
	unlabeled = db.unlabeled
	while unlabeled.count != 0:
		email = get_first_email(unlabeled)
		print_email(email)
		label = get_label(LABELS)
		features = get_features(label, FEATURES)
		email.update(features)
		DBS[label].insert_one(email)
		email_id = get_first_email_id(unlabeled)
		unlabeled.delete_one({'_id': email_id})
