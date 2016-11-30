import scipy.io
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import linkage, dendrogram
# from sentence.ranking import Ranking
# from evaluation.ranking.segment import kendall_tau
import sys
from utils import *
from pickle import load
from featurizer import generate_featurizer


def init():
    # Increase needed on max recursion depth (data too big)
    sys.setrecursionlimit(10000)

    # https://github.com/lefterav/rankeval
    rank_eval_dir = './rankeval-master/src/'
    sys.path.append(rank_eval_dir)

# Discounted Cumulative Gain
# u and v should be lists of same length
# {'tau': 0.5909090909090909,
#  'tau_all_pairs': 132,
#  'tau_avg_seg': 0.59090909090909094,
#  'tau_avg_seg_prob': 4.2322067287064823e-27,
#  'tau_concordant': 105,
#  'tau_discordant': 27,
#  'tau_original_ties': 0,
#  'tau_predicted_ties': 0,
#  'tau_predicted_ties_per': 0.0,
#  'tau_prob': 9.1709457975947886e-24,
#  'tau_sentence_ties': 0,
#  'tau_sentence_ties_per': 0.0,
#  'tau_valid_pairs': 132}
def dcg(u, v):
    result = kendall_tau(Ranking(u), Ranking(v))
    return result.tau

# texts, labels = get_data()
# # print(labels)
# data = featurize(texts, mode='tfidf')
# data_dist = scipy.spatial.distance.pdist(data)
def generate_dendrogram():
    with open('intuit_data', 'rb') as f:
        email_data = load(f)
    email_texts = [email['Text'] for email in email_data['data']]
    g = generate_featurizer(email_texts, mode='tfidf')
    print(email_texts[0])
    featurized_matrix = g(email_texts)
    print(featurized_matrix.root)
    data_dist = pdist(data)
    # 'single', 'complete', 'average'
    data_link = linkage(data_dist, method="single")

    dendrogram(data_link,
        truncate_mode='lastp',
        p=10,  # show only the last p merged clusters
        show_leaf_counts=False,  # otherwise numbers in brackets are counts
        leaf_rotation=90.,
        leaf_font_size=12.,
        # labels=labels,
        show_contracted=True,)
    plt.xlabel('Labels')
    plt.ylabel('Distance')
    plt.suptitle('Event Labels clustering', fontweight='bold', fontsize=14)
    # plt.scatter(data_link)
    plt.show()
generate_dendrogram()


# # clusternum = 8
# # clustdict = {i:[i] for i in range(len(linkage)+1)}
# # for i in range(len(linkage)-clusternum+1):
# #     clust1= int(linkage[i][0])
# #     clust2= int(linkage[i][1])
# #     clustdict[max(clustdict)+1] = clustdict[clust1] + clustdict[clust2]
# #     del clustdict[clust1], clustdict[clust2]
# # print(clustdict)
