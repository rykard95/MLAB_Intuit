import nltk
import utils
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
from nltk.corpus import wordnet as wn
from random_forest import rf_model, rf_categorize
# run nltk.download() once to populate corpora

emails = []
features = {
"college_clean": [('ORGANIZATION', 'college')],
"pet_clean": [('PERSON', 'pet')],
"tuition_clean": [('MONEY', 'TUITION')],
"application_clean": [('ORGANIZATION', 'college')],
"travel_clean": [('LOCATION', 'destination')],
"grad_clean": [('DATE', 'graduation')],
"funeral_clean": [('PERSON', 'name')],
"job_clean": [('MONEY', 'salary')],
"medical_clean": [('DATE', 'bill')],
"moving_clean": [('LOCATION', 'destination')]} # could add more features here
# list of parts of speech available at http://www.nltk.org/book/ch07.html

def extract_all(use_random_forest):
    if use_random_forest:
        emails = rf_model()
        emails = [email for email in emails if email[0] != 'negatives_clean']
    else:
        db = utils.get_local_db()
        for collection in db.collection_names():
            if collection != 'negatives_clean':
                for record in db.get_collection(collection).find():
                    emails.append([collection] + [record['Text']])

    # find features for each email
    email_data = []
    for email_set in emails:
        email = email_set[1]
        fields = features[email_set[0]]

        # extract named entities
        tokenized_email = nltk.word_tokenize(email)
        tagged_email =  nltk.pos_tag(tokenized_email)
        named_entity_email = nltk.ne_chunk(tagged_email)
        entities = []

        # concatenate multi-word entities
        for branch in named_entity_email:
            if isinstance(branch, nltk.tree.Tree):
                entity = ''
                for sub_entity in branch:
                    entity += (sub_entity[0] + ' ')
                if [branch.label(), entity.strip()] not in entities:
                    entities.append([branch.label(), entity.strip()])

        # use entities to fill in fields
        matches = []
        for field in fields:
            field_matches = []
            for entity in entities:
                # compute semantic distance and threshold
                if wn.synsets(field[1]) and wn.synsets(entity[1]):
                    a = wn.synsets(field[1])[0]
                    b = wn.synsets(entity[1])[0]
                    dist = a.path_similarity(b)
                    if dist and dist > 0.05:
                        field_matches.append([dist, entity[1]])
            matches.append([field[1], field_matches])
        email_data.append([email_set[0], email, matches])
    return email_data

def extract_one(email):
    # use random-forest to find email category
    category = rf_categorize(email)
    if category != 'negatives_clean':
        fields = features[category]

        # extract named entities
        tokenized_email = nltk.word_tokenize(email)
        tagged_email =  nltk.pos_tag(tokenized_email)
        named_entity_email = nltk.ne_chunk(tagged_email)
        entities = []

        # concatenate multi-word entities
        for branch in named_entity_email:
            if isinstance(branch, nltk.tree.Tree):
                entity = ''
                for sub_entity in branch:
                    entity += (sub_entity[0] + ' ')
                if [branch.label(), entity.strip()] not in entities:
                    entities.append([branch.label(), entity.strip()])

        # use entities to fill in fields
        matches = []
        for field in fields:
            field_matches = []
            for entity in entities:
                # compute semantic distance and threshold
                if wn.synsets(field[1]) and wn.synsets(entity[1]):
                    a = wn.synsets(field[1])[0]
                    b = wn.synsets(entity[1])[0]
                    dist = a.path_similarity(b)
                    if dist and dist > 0.05:
                        field_matches.append([dist, entity[1]])
            matches.append([field[1], field_matches])

        # return categorized email with field guess probablities
        return [category, email, matches]
