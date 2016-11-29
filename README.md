# ML@B-Intuit Collaboration: Predicting Life
Goal: Create a model that can detect when a user is going through an important event in their life using the user's emails.

## Dependencies
* [python2.7][1] (For NLP Packages)
* [python3][9] (For parsing raw emails)
* [pymongo][2]
    * `pip install pymongo`
* [gensim][3] (only if you want to import word2vec model)
    * `pip install gensim`
* [numpy][4]
    * `pip install numpy`
* [scipy][5]
    * `pip install scipy`
* [Got Your Back (G.Y.B)][6]
* [seaborn][7]
    * `pip install seaborn`
* [nltk][8]
    * `pip install nltk`


## Gathering Data
* eparser.py
* 
After [generating your GYB directory][6], invoke `eparser.py` to store your parsed emails onto your local MongoDB in the `unlabeled` email collection.

Usage
```
python3 parser.py [path to folder with GYB emails]
```
Example
```
python3 ~/Documents/Berkeley/ML/Intuit/got-your-back-1.0/GYB-GMail-Backup-matthewtrepte@gmail.com/2016
```
#### Structure
```python
email = {'From': "Email Sender",
        'Subject': "Email Subject",
        'Text': "Email Body Text",
        'To': "Email Recipient",
        '_id': "Datum Id"
        }
```
## Labeling Data
* labeller.py
* 
This is a tool that allowed for the rapid labeling of emails, to generate a labeled dataset for supervised learning.

Usage
```
python labeller.py
```
![alt text][labeller]
## Featurizing Data

Example usage
```python
from featurizer import featurize
data = featurize(list_of_emails, mode='tfidf')
```

##### Word2Vec Similarity Models
Used as auxillary features as opposed to a standalone model. This model takes as input, the words which are chosen to semantically represent the labels and outputs a vector that represents the similarity scores of an email and each label.

```python
from word2vec_model import featurize
feature_vector = featurize(email)
```

## Clustering
Used to investigate the underlying structure of our featurization. We would like to know how many clusters exist intrinsically and see if they align well with our given labels.

## Model Generation

##### Random Forests
##### Regression

### Data Cache
Since importing the word2vec is a lot of overhead, a cache of the scores is included in the repo, named `score_matrix.mat`, for convenience.  

[1]: https://www.python.org/downloads/release/python-2712/
[2]: https://api.mongodb.com/python/current/
[3]: https://radimrehurek.com/gensim/
[4]: http://www.numpy.org/
[5]: https://www.scipy.org/
[6]: https://github.com/jay0lee/got-your-back/wiki
[7]: http://seaborn.pydata.org/
[8]: http://www.nltk.org/
[9]: https://www.python.org/downloads/

[labeller]: https://github.com/rykard95/MLAB_Intuit/blob/master/imgs/Intuit_labeller_screenshot.png

