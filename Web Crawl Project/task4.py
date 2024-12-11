"""
COMP20008 Semester 1
Assignment 1 Task 4
"""

import matplotlib.pyplot as plt
import pandas as pd
from typing import List, Dict
from collections import defaultdict

# Task 4 - Plotting the Most Common Words (2 Marks)
def task4(bow: pd.DataFrame, output_plot_filename: str) -> Dict[str, List[str]]:
    # The bow dataframe is the output of Task 3, it has 
    # three columns, link_url, words and seed_url. The 
    # output plot should show which words are most common
    # for each seed_url. The visualisation is your choice,
    # but you should make sure it makes sense for what it
    # is meant to be.
    # Implement Task 4 here
    dict1 = {}
    final_dict = {}
    ret_dict = {}
    word_list = bow['words'].tolist()
    seed_list = bow['seed_url'].tolist()
    length1 = len(seed_list)
    for i in range(length1):
        if seed_list[i] in dict1:
            dict1[seed_list[i]] += word_list[i]
        else:
            dict1[seed_list[i]] = word_list[i]
    for j in dict1:
        words = dict1[j]
        words_list = words.split(' ')
        dict2 = {}
        for k in words_list:
            if k in dict2:
                dict2[k] += 1
            else:
                dict2[k] = 1
        sorted_dict = {key: value for key, value in sorted(dict2.items(), key = lambda x: x[1], reverse = True)}
        top_10_sorted = dict(list(sorted_dict.items())[:10])
        final_dict[j] = top_10_sorted
    for x in final_dict:
        plt.bar(list(final_dict[x].keys()), list(final_dict[x].values()))
        plt.xticks(rotation=30)
        plt.title(x)
        plt.savefig(output_plot_filename)
    for y in final_dict:
        final_list = list(final_dict[y].keys())
        ret_dict[y] = final_list
    return ret_dict
