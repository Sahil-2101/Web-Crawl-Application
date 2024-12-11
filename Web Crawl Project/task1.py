""" 
COMP20008 Semester 1
Assignment 1 Task 1
"""

import pandas as pd
import json
from typing import Dict, List

import requests
import bs4
import urllib
from robots import process_robots, check_link_ok

# A simple page limit used to catch procedural errors.
SAFE_PAGE_LIMIT = 1000


# Task 1 - Get All Links (3 marks)
def task1(starting_links: List[str], json_filename: str) -> Dict[str, List[str]]:
    # Crawl each url in the starting_link list, and output
    # the links you find to a JSON file, with each starting
    # link as the key and the list of crawled links for the
    # value.
    # Implement Task 1 here
    length = len(starting_links)
    dict1 = {}
    for i in range(length):
        web_list1 = []
        new_list1 = []
        new_list2 = []
        list1_count = 0
        website = starting_links[i]
        protocol = website[:21]
        page = requests.get(website)
        soup = bs4.BeautifulSoup(page.text, 'html.parser')
        for j in soup.find_all('a', href = True):
            if ('samplewiki') in j['href']:
                new_website = protocol+j['href']
                if new_website not in web_list1:
                    web_list1.append(new_website)
                    list1_count += 1
                    new_page = requests.get(new_website)
                    new_soup = bs4.BeautifulSoup(new_page.text, 'html.parser')
                    for k in new_soup.find_all('a', href = True):
                        if ('samplewiki') in k['href']:
                            new_website = protocol+k['href']
                            if new_website not in web_list1:
                                web_list1.append(new_website)
                                new_list1.append(new_website)
                                list1_count += 1
            elif ('fullwiki') in j['href']:
                new_website = protocol+j['href']
                if new_website not in web_list1:
                    web_list1.append(new_website)
                    list1_count += 1
                    new_page = requests.get(new_website)
                    new_soup = bs4.BeautifulSoup(new_page.text, 'html.parser')
                    for k in new_soup.find_all('a', href = True):
                        if ('fullwiki') in k['href']:
                            new_website = protocol+k['href']
                            if new_website not in web_list1:
                                web_list1.append(new_website)
                                new_list1.append(new_website)
                                list1_count += 1
        success = 1
        while success > 0:
            success = 0
            for web in new_list1:
                next_page = requests.get(web)
                next_soup = bs4.BeautifulSoup(next_page.text, 'html.parser')
                for next_website in next_soup.find_all('a', href = True):
                    if ('samplewiki') in next_website['href']:
                        next_web = protocol+next_website['href']
                        if next_web not in web_list1:
                            web_list1.append(next_web)
                            new_list2.append(next_web)
                            success += 1
                    elif ('fullwiki') in next_website['href']:
                        next_web = protocol+next_website['href']
                        if next_web not in web_list1:
                            web_list1.append(next_web)
                            new_list2.append(next_web)
                            success += 1
            new_list1 = new_list2
            new_list2 = []                        
        web_list1.sort()
        dict1[website] = web_list1
    with open(json_filename, 'w') as file:
        json.dump(dict1, file)

    return {}

