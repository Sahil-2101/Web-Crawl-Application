"""
COMP20008 Semester 1
Assignment 1 Task 5
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, Union, List
import seaborn as sb

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import PCA
from sklearn.preprocessing import Normalizer


# Task 5 - Dimensionality Reduction (3 marks)
def task5(bow_df: pd.DataFrame, tokens_plot_filename: str, distribution_plot_filename: str) -> Dict[str, Union[List[str], List[float]]]:
    # bow_df is the output of Task 3, for this task you 
    # should generate a bag of words, normalisation of the 
    # data perform PCA decomposition to 2 components, and 
    # then plot all URLs in a way which helps you answer
    # the discussion questions. If you would like to verify 
    # your PCA results against the sample data, you can return
    # the PCA weights - containing the list of most positive
    # weighted words, most negatively weighted words and the 
    # weights in the PCA decomposition for each respective word.
    # Implement Task 5 here
    vectorizer = CountVectorizer()
    bag_of_words = vectorizer.fit_transform(bow_df['words'])
    tokens = vectorizer.get_feature_names_out()
    normal_key = Normalizer('max')
    normalized_bow = normal_key.fit_transform(bag_of_words)
    sklearn_pca = PCA(n_components=2)
    pca_bow = sklearn_pca.fit_transform(normalized_bow.toarray())
    graph = plt.figure()
    sub_graph = graph.subfigures(nrows=2, ncols=1)
    graph1 = graphing(tokens, sklearn_pca.components_[0], sub_graph[0])
    graph2 = graphing(tokens, sklearn_pca.components_[1], sub_graph[1])
    graph.savefig(tokens_plot_filename)
    
    new_fig = plt.figure()
    sb.scatterplot(x=pca_bow[:, 0], y=pca_bow[:, 1], hue=bow_df['seed_url'])
    plt.savefig(distribution_plot_filename)

    final_dict = {}
    dict1 = {}
    dict2 = {}
    positive_1 = list(graph1[0].keys())
    positive_weights_1 = list(graph1[0].values())
    negative_1 = list(graph1[1].keys())
    negative_weights_1 = list(graph1[1].values())
    dict1['positive'] = positive_1
    dict1['negative'] = negative_1
    dict1['positive_weights'] = positive_weights_1
    dict1['negative_weights'] = negative_weights_1
    positive_2 = list(graph2[0].keys())
    positive_weights_2 = list(graph2[0].values())
    negative_2 = list(graph2[1].keys())
    negative_weights_2 = list(graph2[1].values())
    dict2['positive'] = positive_2
    dict2['negative'] = negative_2
    dict2['positive_weights'] = positive_weights_2
    dict2['negative_weights'] = negative_weights_2
    final_dict["0"] = dict1
    final_dict["1"] = dict2

    return final_dict

def graphing(tokens, weights, graph):
    graph_dict = {}
    for i in range(len(tokens)):
        graph_dict[tokens[i]] = weights[i]
    sorted_dict = {key: value for key, value in sorted(graph_dict.items(), key = lambda x: x[1], reverse = True)}
    top_10_weights = dict(list(sorted_dict.items())[:10])
    bottom_10_weights = dict(list(sorted_dict.items())[-10:])
    plot = graph.subplots(nrows =2, ncols = 1)
    plot[0].bar(top_10_weights.keys(), top_10_weights.values())
    plot[1].bar(bottom_10_weights.keys(), bottom_10_weights.values())
    return [top_10_weights, bottom_10_weights]
