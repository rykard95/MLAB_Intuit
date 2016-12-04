from pickle import load
import sys
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.feature_extraction import DictVectorizer

def bag_of_words(texts):
    vectorizor = CountVectorizer(texts)
    vectorizor.fit(texts)
    return vectorizor.transform


def tfidf(texts):
    vectorizor = TfidfVectorizer()
    vectorizor.fit(texts)
    return vectorizor.transform

def term_frequency(term, tokenized_document):
    return tokenized_document.count(term)

def tf_modified(texts, labels):
    tokenize = lambda doc: doc.lower().split(" ")
    # travel_texts = [texts[i] for i in range(len(texts)) if labels[i]=='travel']
    # moving_texts = [texts[i] for i in range(len(texts)) if labels[i]=='moving']
    # tuition_texts = [texts[i] for i in range(len(texts)) if labels[i]=='tuition']
    # funeral_texts = [texts[i] for i in range(len(texts)) if labels[i]=='funeral']
    # application_texts = [texts[i] for i in range(len(texts)) if labels[i]=='application']
    # job_texts = [texts[i] for i in range(len(texts)) if labels[i]=='job']
    # baby_texts = [texts[i] for i in range(len(texts)) if labels[i]=='baby']
    # college_texts = [texts[i] for i in range(len(texts)) if labels[i]=='college']
    # pet_texts = [texts[i] for i in range(len(texts)) if labels[i]=='pet']
    # grad_texts = [texts[i] for i in range(len(texts)) if labels[i]=='grad']
    # medical_texts = [texts[i] for i in range(len(texts)) if labels[i]=='medical']
    # wedding_texts = [texts[i] for i in range(len(texts)) if labels[i]=='wedding']
    # negative_texts = [texts[i] for i in range(len(texts)) if labels[i]=='negative']

    tokenized_docs = [tokenize(doc) for doc in texts]
    all_terms = set([term for doc in tokenized_docs for term in doc])

    tf_modified_matrix = []
    for doc in tokenized_docs:
        tf_dict = {}
        for term in all_terms:
            tf = term_frequency(term, doc)
            label = labels[tokenized_docs.index(doc)]
            label_texts = [tokenized_docs[i] for i in range(len(tokenized_docs)) if labels[i]==label]
            normalized_tf = tf/(sum([term_frequency(term, d) for d in label_texts])) if tf!=0 else 0
            tf_dict[term] = normalized_tf
        tf_modified_matrix.append(tf_dict)

    vec = DictVectorizor()
    return vec.fit_transform(tf_modified_matrix).toarray()



def n_gram(texts, n):
    vectorizor = CountVectorizer(ngram_range=(n,n))
    train_data_features = vectorizor.fit_transform(texts).toarray()
    print(vectorizor.get_feature_names())
    return train_data_features

def get_data():
    with open('intuit_data', 'rb') as f:
        data = load(f)
    # data is a dictionary with fields:
    #   `data`  => list of emails
    #   `label` => list of labels
    #   `stats` => counts of emails
    #   `label[i]` corresponds to `data[i]`
    emails = data['data']
    labels = data['label']
    
    texts = convert_data_to_texts(emails)

    return texts, labels

def convert_data_to_texts(emails):
    texts = []
    for email in emails:
        texts.append(email['Text'])
    return texts

def generate_featurizer(texts, mode='tfidf'):
    """
    Featurization wrapper for TF-IDF and 
    Bag of Words. More featurization modes
    can be added by following the structure
    """
    if mode == 'tfidf':
        return tfidf(texts)
    elif mode == 'bow':
        return bag_of_words(texts)

    
def featurization():
    texts, labels = get_data()
    result = input('Select which featurization method you would like to use: \n [0]: Bag of words \n [1]: Tf-idf \n [2]: Modified TF \n [3]: N-gram Bag of words \n')
    if result=='0':
        return bag_of_words(texts)
    elif result=='1':
        return tfidf(texts)
    elif result=='2':
        return tf_modified(texts, labels)
    elif result=='3':
        n = input('Please input an n value for n-gram featurization')
        return n_gram(texts, n)
    else:
        print('Please select one of the options')

if __name__=='__main__':
    print(featurization())
