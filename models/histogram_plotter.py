import numpy as np
from pylab import savefig
from matplotlib import pyplot as plt
from os import listdir, mkdir
from utils import *


def generate_histograms(score_matrix):
    # Label to number mapping
    labels = get_labels()
    label_to_number = {a[1]:a[0] for a in list(enumerate(labels))} 
    # Initialize the Histograms
    class_rank = {i:[] for i in range(len(labels))}
    correct_rank = []
    guess_rank = []
    each_class_correct_rank = {i:0 for i in range(len(labels))}
    correct_raw_scores = {i:[] for i in range(len(labels))}
    incorrect_raw_scores = {i:[] for i in range(len(labels))} 

    # Iterate through score matrix
    for score_vector in score_matrix:
        correct_label = label_to_number[str(score_vector[-1]).strip()] 
        score_vector = score_vector[:-1].astype(float)
        top_score_ind = np.argsort(score_vector)[::-1]
        score_vector = np.sort(score_vector)[::-1]
        rank = int(np.where(top_score_ind == correct_label)[0])
        
        # Add to Histogram
        correct_rank.append(correct_label)
        guess_rank.append(top_score_ind[0])
        class_rank[correct_label].append(rank)
        if correct_label == top_score_ind[0]:
            correct_raw_scores[correct_label].append(score_vector[0])
        else:

            incorrect_raw_scores[correct_label].append(score_vector[rank])

    if 'w2v_figs' not in listdir("."):
        mkdir('w2v_figs')
        
    plot_correct_hist(correct_rank)
    plot_guess_hist(guess_rank)
    for i in range(len(labels)):
        plot_label_rank(class_rank[i], labels[i])
        plot_correct_class_scores(correct_raw_scores[i], labels[i])
        plot_incorrect_class_scores(incorrect_raw_scores[i], labels[i])
    plot_correct_scores(correct_raw_scores)
    plot_incorrect_scores(incorrect_raw_scores)
          
def plot_guess_hist(guess_hist):
    bins = np.arange(13) - 0.5    
    n, bins, patches = plt.hist(guess_hist, bins, normed=1, facecolor='green', alpha=0.75) 
    labels = get_labels()
    plt.title("Guess Labels Histogram")
    plt.xlabel("Label")
    plt.xticks(np.arange(len(labels)), labels, rotation='vertical')
    plt.ylabel("Frequency of Labels")
    plt.tight_layout()
    savefig("w2v_figs/guess_hist.png")
    plt.clf()

def plot_correct_hist(correct_hist):
    bins = np.arange(13) - 0.5    
    n, bins, patches = plt.hist(correct_hist, bins, normed=1, facecolor='green', alpha=0.75) 
    labels = get_labels()
    plt.title("Correct Labels Histogram")
    plt.xlabel("Label")
    plt.xticks(np.arange(len(labels)), labels, rotation='vertical')
    plt.ylabel("Frequency of Labels")
    plt.tight_layout()
    savefig("w2v_figs/correct_hist.png")
    plt.clf()

def plot_label_rank(ranks, label):
    bins = np.arange(13) - 0.5
    n, bins, patches = plt.hist(ranks, bins, normed=1, facecolor='blue', alpha=0.75) 
    labels = np.arange(12)
    plt.title("Ranks for Label: " + label)
    plt.xticks(np.arange(len(labels)), labels)
    plt.ylabel("Frequency Rank Appearance")
    plt.tight_layout()
    savefig("w2v_figs/rank_" + label+'.png')
    plt.clf()
    
def plot_correct_scores(correct_scores):
    scores = np.array([a for v in correct_scores.values() for a in v])
    n, bins, patches = plt.hist(scores, 50, normed=1, facecolor='blue', alpha=0.75)
    plt.title("Histogram of Correct Label Scores")
    plt.ylabel("Frequency of scores")
    plt.xlabel("Score")
    plt.tight_layout()
    savefig('w2v_figs/correct_scores.png')
    plt.clf()

def plot_incorrect_scores(incorrect_scores):
    scores = np.array([a for v in incorrect_scores.values() for a in v])
    n, bins, patches = plt.hist(scores, 50, normed=1, facecolor='red', alpha=0.75)
    plt.title("Histogram of Incorrect Label Scores")
    plt.ylabel("Frequency of scores")
    plt.tight_layout()
    savefig('w2v_figs/Incorrect_scores.png')
    plt.clf()

def plot_correct_class_scores(correct_scores, label):
    scores = correct_scores
    n, bins, patches = plt.hist(scores, 50, normed=1, facecolor='blue', alpha=0.75)
    plt.title("Histogram of Correct Label Scores for " + label)
    plt.ylabel("Frequency of scores")
    plt.tight_layout()
    savefig('w2v_figs/Correct_scores_'+ label +'.png')
    plt.clf()
    

def plot_incorrect_class_scores(incorrect_scores, label):
    scores = incorrect_scores 
    n, bins, patches = plt.hist(scores, 50, normed=1, facecolor='red', alpha=0.75)
    plt.title("Histogram of Incorrect Label Scores for " + label)
    plt.ylabel("Frequency of scores")
    plt.tight_layout()
    savefig('w2v_figs/Incorrect_scores_'+label+'.png')
    plt.clf()
