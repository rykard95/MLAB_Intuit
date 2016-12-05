from pylab import plot,show
from scipy.cluster.vq import kmeans, vq
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import utils

emails_array = []
label_array = []

# get emails
db = utils.get_remote_db()
for collection in db.collection_names():
    for record in db.get_collection(collection).find():
        if 'Text' in record:
            emails_array.append(record['Text'])
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

    # apply PCA to vectors
    data = PCA(n_components=2).fit_transform(data)

    # applying kmeans
    centroids, _ = kmeans(data, 2)

    # assign each sample to a cluster
    idx, _ = vq(data, centroids)

    # assign colors to clusters and plot
    plot(data[idx==0, 0], data[idx==0, 1], 'ob',
         data[idx==1, 0], data[idx==1, 1], 'or')
    plot(centroids[:, 0], centroids[:,1], 'sg', markersize=8)
    show()