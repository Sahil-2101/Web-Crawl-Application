""" 
COMP20008 Semester 1
Assignment 1 Task 3
"""

from typing import Dict, List
import pandas as pd
import json
import requests
import bs4
import urllib
import unicodedata
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

from robots import process_robots, check_link_ok


# Task 3 - Producing a Bag Of Words for All Pages (2 Marks)
def task3(link_dictionary: Dict[str, List[str]], csv_filename: str):
    # link_dictionary is the output of Task 1, it is a dictionary
    # where each key is the starting link which was used as the 
    # seed URL, the list of strings in each value are the links 
    # crawled by the system. The output should be a csv which
    # has the link_url, the words produced by the processing and
    # the seed_url it was crawled from, this should be output to
    # the file with the name csv_filename, and should have no extra
    # numeric index.
    # Implement Task 3 here
    # Empty dataframe to demonstrate output data format.
    list2 = []
    sample_dict = {}
    with open('task_3_json.json', 'w') as f:
        json.dump(sample_dict , f)
    for i in link_dictionary:
        for j in link_dictionary[i]:
            list1 = []
            dict1 = {}
            task2(j, 'task_3_json.json')
            with open('task_3_json.json', 'r') as ret_val_file:
                ret_val_read = ret_val_file.read()
                ret_val = json.loads(ret_val_read)
                list1 = ret_val[j]
                str1 = ' '.join(list1)
                dict1 = {'link_url':j, 'words':str1, 'seed_url':i}
                list2.append(dict1)
    list3 = sorted(list2, key = lambda call: call['link_url'])        
    dataframe = pd.DataFrame(list3)
    dataframe.to_csv(csv_filename)
    return dataframe

def task2(link_to_extract: str, json_filename: str):
    # Download the link_to_extract's page, process it 
    # according to the specified steps and output it to
    # a file with the specified name, where the only key
    # is the link_to_extract, and its value is the 
    # list of words produced by the processing.
    # Implement Task 2 here
    dict1 = {}
    page = requests.get(link_to_extract)
    page.encoding = page.apparent_encoding
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    pre_pro = soup.find('div', id = 'mw-content-text')
    rem_ele_class(pre_pro, 'th', 'infobox-label')
    rem_ele_class(pre_pro, 'div', 'printfooter')
    rem_ele_id(pre_pro, 'div', 'toc')
    rem_ele_class(pre_pro, 'table', 'ambox')
    rem_ele_class(pre_pro, 'div', 'asbox')
    rem_ele_class(pre_pro, 'span', 'mw-editsection')
    text_tree = pre_pro.get_text(separator=' ')
    text_tree = text_tree.casefold()
    text_tree = unicodedata.normalize('NFKD', text_tree)
    new_text_tree = ""
    prev_char = ""
    
    new_text_tree = re.sub(r"[^a-zA-Z\s\\]", " ", text_tree)
    new_text_tree = re.sub(r"\s", " ", new_text_tree)
    new_text_tree = re.sub(' +', ' ', new_text_tree)

    text_tree_tokens = new_text_tree.split(' ')
    stop_words = stopwords.words('english')
    length_tokens = len(text_tree_tokens)
    i = 0
    while i < length_tokens:
        if text_tree_tokens[i] in stop_words:
            text_tree_tokens.remove(text_tree_tokens[i])
            i -= 1
            length_tokens -= 1
        i += 1
    
    length_tokens = len(text_tree_tokens)
    j = 0
    while j < length_tokens:    
        if len(text_tree_tokens[j]) < 2:
            text_tree_tokens.remove(text_tree_tokens[j])
            j -= 1
            length_tokens -= 1
        j += 1

    por_stem = PorterStemmer()
    for i in range(len(text_tree_tokens)):
        text_tree_tokens[i] = por_stem.stem(text_tree_tokens[i])
    dict1[link_to_extract] = text_tree_tokens
    with open(json_filename, 'w') as file:
        json.dump(dict1, file)

    return {}

def rem_ele_class(x, element, e_class):
    y = x.find_all(element, class_ = e_class)
    for z in y:
        z.extract()
    return ()

def rem_ele_id(x, element, e_id):
    y = x.find_all(element, id = e_id)
    for z in y:
        z.extract()
    return ()
