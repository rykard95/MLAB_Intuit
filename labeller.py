#!usr/bin/env python

def printEmail(collection):
	data = collection.find().limit(1)[0]
	print("----------------------------- Email Body -----------------------------")
	print('\n')
	print(data['body'])
	print('\n')
	print("----------------------------------------------------------------------")

def getLabel(labels):
	"""Queries user for structured label"""
	for i in range(len(labels)):
		print("[" + str(i) + "]" + str(labels[i]))
	print('')
	label = input("Pick a label: ")
	if label not in VALID_LABELS:
		print("That is not a valid option.")
	if label == 's':
		return -1
	else:
		return str(label)

def getFeatures(label, features):
	"""Further queries user for extra features"""
	pass

def mergeDict(a, b):
	"""Helper function to merge the initial database features
	with auxilliary features"""
	pass


if __name__ == "__main__":
	from pymongo import MongoClient
	client = MongoClient('localhost:27017')
	db = client.emails

	LABELS = ['Moving Event', 'Pet Adoption', 'Attending College', 'Tuition Event', 'Job/Internship Event', \
			'Medical Event', 'Wedding', 'Funeral', 'Baby', 'Graduation', 'Travel Event', 'College/Scholarship Applications']
	VALID_LABELS = [str(i) for i in range(len(LABELS))] + ['s']
	
	AUX_FEATURES = [['Where was the move?', 'When was the move?'],\
				['What kind of pet?'],\
				['Which family member went to college?', 'Which college did they go to?'],\
				['What was the cost of tuition?', 'Was there any financial aid?'],\
				['Which company was involved?', 'How long is the internship? (Put \'N/A\' if not internship)', 'Where is the job?'],\
				['Was it an injury\'[0]\' or illness\'[1]\'', 'Was there a hospitalization? (1 or 0)', 'How long did it last?', 'What was the severity?'],\
				['Who was involved with the wedding?', 'When was the wedding?'],\
				['Who was involved with the funeral?', 'When was the funeral?'],\
				['When did this occur?'],\
				['When was the graduation?', 'Where did you graduate from?'],\
				['Where did you travel to?', 'How long was the travel?', 'How much was the travel costs?', 'Was it business or personal? (1 or 0)'],\
				['Which college/scholarship was the acceptance from?', 'What is the acceptance status?']]

	DBS = [db.moving, db.pet, db.college, db.job, db.medical, db.wedding, db.funeral, db.baby, db.grad, db.travel, db.application]



	

	numEmailsRead = 0

	printEmail(db.unlabeled)
	getLabel(LABELS)
