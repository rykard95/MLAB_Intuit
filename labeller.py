#labeller.py
from pymongo import MongoClient
from IPython import embed

USERNAME = 'mlabintuit'
PASSWORD = 'mlab;123'
MONGODB_URI = 'mongodb://%s:%s@ds048319.mlab.com:48319' % (USERNAME, PASSWORD)

HISTORY = []

def pushHistory(data):
	HISTORY.append(data)
	if len(HISTORY) >= 100:
		HISTORY.pop(0)

def popHistory(data):
	return HISTORY.pop()


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

def get_labels(group_labels):
	"""Queries user for label"""
	for i, elem in enumerate(group_labels):
	    print("[" + str(i) + "] " + elem)
	print("[s] Skip")
	print("[e] General event")
	print('')
	index = input("Choose labels separated by spaces: ")

	if 'e' in index: 
		return -1
	elif 's' in index:
		return -2
	return translate_labels(group_labels,index)

def translate_labels(label_list, label_string):
	labels = label_string.split(" ")
	text_labels = []
	for label in labels:
		if label.isnumeric() and int(label) in range(len(label_list)):
			text_labels.append(label_list[int(label)])
	return text_labels

def get_features(label, features):
	"""Queries user for features associated with a given label"""
	feature_responses = {}
	for feature in features[label]:
		response = input(feature + ' ')
		feature_responses[feature] = response
	return feature_responses

if __name__ == "__main__":
	#Instantiate connection to DB
	local_client = MongoClient('localhost:27017')
	local_db = local_client.emails

	remote_client = MongoClient(MONGODB_URI)
	remote_db = remote_client.emails
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
	DBS_ARR = [remote_db.moving, remote_db.pet, remote_db.college, remote_db.job, remote_db.tuition, remote_db.medical,
			   remote_db.wedding, remote_db.funeral, remote_db.baby, remote_db.grad, remote_db.travel, remote_db.application]
	assert (len(FEATURES_ARR) == len(LABELS) and len(DBS_ARR) == len(LABELS)), 'Missing entry in one or more of the constant arrays.'
	#Generate dictionaries
	FEATURES = {LABELS[i]: FEATURES_ARR[i] for i in range(len(LABELS))}
	DBS = {LABELS[i]: DBS_ARR[i] for i in range(len(LABELS))}
	#Iterate and classify emails
	unlabeled = local_db.unlabeled
	while unlabeled.count != 0:
		base_email = get_first_email(unlabeled)
		print_email(base_email)
		labels = get_labels(LABELS)
        #Check to see if skipped
		if isinstance(labels, list):
			for label in labels:
				email = base_email.copy()
				features = get_features(label, FEATURES)
				print('')
				email.update(features)
				DBS[label].insert_one(email)
		elif labels == -1:
			remote_db.event.insert_one(base_email)
		else:
			local_db.skipped.insert_one(base_email)
		email_id = get_first_email_id(unlabeled)
		unlabeled.delete_one({'_id': email_id})
