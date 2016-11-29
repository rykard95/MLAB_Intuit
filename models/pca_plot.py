from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import numpy as np
import utils

if __name__ == '__main__':

    # label color mapping
    labels = ['grad', 'college', 'application', 'pet', 'moving', 'travel', 'funeral', 'tuition', 'medical', 'job', 'event', 'unlabeled', 'negatives']
    colors = ['orange', 'blue', 'red', 'darkgreen', 'turquoise', 'purple', 'magenta', 'brown', 'lightgreen', 'black', 'yellow', 'gray', 'pink']

    emails_array = []
    label_array = []

    # get emails
    db = utils.get_remote_db()
    for collection in db.collection_names():
        for record in db.get_collection(collection).find():
            if 'Text' in record:
                emails_array.append(record['Text'])
                label_array.append(labels.index(collection))

    # PLUG-IN FEATURIZAION HERE
    # apply tf-idf to data
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(emails_array)
    X = X.toarray()
 
    # apply PCA to vectors
    X = PCA(n_components=2).fit_transform(X)

    # plot data
    for i in range(len(X)):
        x, y = X[i, 0], X[i, 1]
        label = label_array[i]
        plt.scatter(x, y, c=colors[label], cmap=plt.cm.Paired)

    # legend
    patches = [mpatches.Patch(color=colors[i], label=labels[i]) for i in range(len(labels))]
    plt.legend(handles=patches, loc=4, fontsize=10)

    plt.show()