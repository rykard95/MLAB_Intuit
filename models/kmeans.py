from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.cluster import KMeans
import utils

emails_array = []
label_array = []

# get emails and labels
db = utils.get_remote_db()
for collection in db.collection_names():
    for record in db.get_collection(collection).find():
        if 'Text' in record:
            emails_array.append(record['Text'])
            # segment data labels by 'event' or 'non-event'
            if collection == 'negatives':
                label_index = 0
            else:
                label_index = 1
            label_array.append(label_index)

# BagOfWords, TermFrequency-InverseDocumentFrequency
vectorizers = [CountVectorizer(), TfidfVectorizer()]

for vectorizer in vectorizers:    
    # featurize emails
    data = vectorizer.fit_transform(emails_array).toarray()

    # apply kmeans to emails vectors
    kmeans = KMeans(n_clusters=2, random_state=0).fit(data)

    # calculate matches
    matches = 0
    for i in range(len(label_array)):
        pred = kmeans.labels_[i]
        meas = label_array[i]
        if pred == meas:
            matches += 1
    misses = len(label_array) - matches

    # line-up labels 
    # note: k-means here is simply dividing the data, so the label it produces is irrelevant (only the grouping is)
    if misses > matches:
        matches, misses = misses, matches

    # spit out accuracy
    accuracy = matches / (matches + misses)
    print("accuracy: ", accuracy)