"""
COMP20008 Semester 1
Assignment 1 Task 2
"""

import json

import requests
import bs4
import urllib
import unicodedata
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

from robots import process_robots, check_link_ok


# Task 2 - Extracting Words from a Page (4 Marks)
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
    text_tree = str(text_tree)
    text_tree = text_tree.casefold()
    text_tree = unicodedata.normalize('NFKD', text_tree)
    new_text_tree = ""
    prev_char = ""
    for i in text_tree:
        if (i.isalpha() or i == '\\'):
            new_text_tree += i
        else:
            new_text_tree += ' '
    new_text_tree = ' '.join(new_text_tree.split())
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
    with open(json_filename, 'a') as file:
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
