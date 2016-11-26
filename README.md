# ML@B-Intuit Collaboration: Predicting Life
Goal: Create a model that can detect when a user is going through an important event in their life using the user's emails.

## Dependencies
* [python2.7][1]
* [pymongo][2]
    * `pip install pymongo`
* [gensim][3] (only if you want to import word2vec model)
    * `pip install gensim`
* [numpy][4]
    * `pip install numpy`
* [scipy][5]
    * `pip install scipy`
* [Got Your Back (G.Y.B)][6]


## Gathering Data
* eparser.py
After generating your GYB directory, invoke `eparser.py` to store your parsed emails onto your local MongoDB in the `unlabeled` email collection.

Usage
```
welp
```

## Labeling Data
* labeller.py
This is a tool that allowed for the rapid labeling of emails, to generate a labeled dataset for supervised learning.

Usage
```
uhhh
```

## Featurizing Data

Example usage
```
code block here ahh
ahhhh
ahhhhhhh
```
## Model Generation
##### Word2Vec Similarity Models
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

