import json
import re
import urllib.request
import os
import operator 
import heapq
import random
import itertools
from html_parsers import State_Newspapers_Index_Parser
from html_parsers import Check_If_Actually_Paper_Parser
from html_parsers import Collect_Paper_Attributes_Parser
from html_parsers import Collect_State_Indexes_Parser
from simple_logger import SimpleLogger
from collections import defaultdict


from urllib.request import Request, urlopen
from datetime import datetime

logger = SimpleLogger()

class Paper():
    def __init__(self):
        self.url = ""
        self.name = ""
        self.location = ""
        self.readership = None

    def __str__(self):
        return self.name

    
def collect_papers_Michigan(all_paper_urls):
    filename = "W_html.txt"
    site = "https://en.wikipedia.org/wiki/List_of_newspapers_in_Michigan"
    req = Request(site, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read().decode("utf-8") 
    f = open(filename,"w+")
    f.write(webpage)
    f.close()
    parse_newspapers_from_state_wikipedia_index(filename, all_paper_urls, "Michigan", './urls')


def collect_papers_Alabama(all_paper_urls):
    filename = "W_html.txt"
    site = "https://en.wikipedia.org/wiki/List_of_newspapers_in_Alabama"
    req = Request(site, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read().decode("utf-8") 
    f = open(filename,"w+")
    f.write(webpage)
    f.close()
    parse_newspapers_from_state_wikipedia_index(filename, all_paper_urls, "Alabama", './urls')


def collect_papers_Maryland(all_paper_urls):
    filename = "W_html.txt"
    site = "https://en.wikipedia.org/wiki/List_of_newspapers_in_Maryland"
    req = Request(site, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read().decode("utf-8") 
    f = open(filename,"w+")
    f.write(webpage)
    f.close()
    parse_newspapers_from_state_wikipedia_index(filename, all_paper_urls, "Maryland", './urls')

def collect_papers_California(all_paper_urls):
    filename = "W_html.txt"
    site = "https://en.wikipedia.org/wiki/List_of_newspapers_in_California"
    req = Request(site, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read().decode("utf-8") 
    f = open(filename,"w+")
    f.write(webpage)
    f.close()
    parse_newspapers_from_state_wikipedia_index(filename, all_paper_urls, "California", './urls')

def collect_papers_Maine(all_paper_urls):
    filename = "W_html.txt"
    site = "https://en.wikipedia.org/wiki/List_of_newspapers_in_Maine"
    req = Request(site, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read().decode("utf-8") 
    f = open(filename,"w+")
    f.write(webpage)
    f.close()
    parse_newspapers_from_state_wikipedia_index(filename, all_paper_urls, "Maine", './urls')

def collect_papers_Alaska(all_paper_urls):
    filename = "X_html.txt"
    site = "https://en.wikipedia.org/wiki/List_of_newspapers_in_Alaska"
    req = Request(site, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read().decode("utf-8") 
    f = open(filename,"w+")
    f.write(webpage)
    f.close()
    parse_newspapers_from_state_wikipedia_index(filename, all_paper_urls, "Alaska", './urls')


def collect_papers_West_Virginia(all_paper_urls):
    filename = "X_html.txt"
    site = "https://en.wikipedia.org/wiki/List_of_newspapers_in_West_Virg"
    req = Request(site, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read().decode("utf-8") 
    f = open(filename,"w+")
    f.write(webpage)
    f.close()
    parse_newspapers_from_state_wikipedia_index(filename, all_paper_urls, "Alaska", './urls')


















def collect_all_us(all_paper_urls):
    site = "https://en.wikipedia.org/wiki/List_of_newspapers_in_the_United_States"

    logger.time_stamp_start_and_print("All US Newspapers Request")
    req = Request(site, headers={'User-Agent': 'Mozilla/5.0'})
    webpage_list_of_us_newspapers = urlopen(req).read().decode("utf-8") 
    logger.time_stamp_stop_and_print("All US Newspapers Request")


    parser = Collect_State_Indexes_Parser()
    parser.initialize()
    parser.feed(webpage_list_of_us_newspapers)

    dateTimeObj = datetime.now()
    dir_path = './urls_' + str(dateTimeObj.month) + '.' + str(dateTimeObj.day) + '.' + str(dateTimeObj.hour) + ':' + str(dateTimeObj.minute) + ':' + str(dateTimeObj.second)
    os.mkdir(dir_path)

    for link in parser.wiki_indexes:
        collect_papers_every_us_territory(all_paper_urls, link, dir_path)


def collect_papers_every_us_territory(all_paper_urls, url, dir_path):
    """
    This function collects urls of us newspapers and writes them too files
    in dir_path
    """
    territory_name = url.split("_in_",1)[1]
    print(territory_name)

    logger.time_stamp_start_and_print("List of Papers by State Request " + territory_name)
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage_list_of_state_newspapers = urlopen(req).read().decode("utf-8") 
    logger.time_stamp_stop_and_print("List of Papers by State Request " + territory_name)

    parse_newspapers_from_state_wikipedia_index(webpage_list_of_state_newspapers, all_paper_urls, territory_name, dir_path)




def parse_newspapers_from_state_wikipedia_index(html_string, all_paper_urls, name, path):
    """
    This function takes in the HTML of a certain type of wikipedia page -- one that displays
    an index of local newspapers pertaining to a geopraphic location -- and then writes the
    website urls of the valid newspapers to a series of files. These files are specified by
    name and path. This function also modifies the value of all_paper_urls to include all
    valid urls. 
    """

    parser = State_Newspapers_Index_Parser()
    parser.initialize()
    parser.feed(html_string)
    all_urls_from_state_index = parser.get_urls()
    parser.clear_urls()
    # for url in all_urls_from_state_index:
    #     print(url)

    all_news_urls_path = os.path.join(path + '/USA.txt')
    state_urls_path = os.path.join(path + '/', str(name) + '.txt')

    valid_state_paper_urls = parse_urls_for_actual_papers(all_urls_from_state_index)
    all_paper_urls.append(valid_state_paper_urls)

    h = open(all_news_urls_path, 'a')
    for url in valid_state_paper_urls:
        h.write(url + '\r\n')
    h.close()
    f = open(state_urls_path, 'a')
    for url in valid_state_paper_urls:
        f.write(url + '\r\n')
    f.close()

    
    

def parse_urls_for_actual_papers(all_urls_from_state_index):
    """
    This function takes in a series of urls that belong to wikipedia pages, determines
    which of those wikipedia pages belong to newspapers (as opposed to cities, publishers, ect.)
    and then returns a list of urls corresponding to the websites of those valid newspapers
    """

    valid_papers_urls = []
    wiki_papers_urls = []
    for url in all_urls_from_state_index:
        print(url)
        logger.time_stamp_start("Opening Potential Paper Wiki Url\n" + str(url))
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        wikipedia_of_potential_paper = urlopen(req).read().decode("utf-8") 
        logger.time_stamp_stop("Opening Potential Paper Wiki Url\n" + str(url))

        parser = Check_If_Actually_Paper_Parser()
        parser.initialize()
        parser.feed(wikipedia_of_potential_paper)
        if parser.is_paper():
            print("SEEMS LEGIT")
            wiki_papers_urls.append(url)
            papers_website_url = get_website_url(wikipedia_of_potential_paper)
            if papers_website_url != None:
                print("FOUND WEBSITE")
                valid_papers_urls.append(papers_website_url)

    return valid_papers_urls
    

def get_website_url(wikipedia_of_potential_paper):
    """
    This function takes in the HTML of a wikipedia site and determines whether 
    or not the page belongs to a newspaper. 
    """
    parser = Collect_Paper_Attributes_Parser()
    parser.initialize()
    parser.feed(wikipedia_of_potential_paper)

    papers_website = parser.get_website()
    if papers_website != "" and papers_website != None and papers_website != " ":
        return papers_website
    return None

    
def main():
    all_papers = []
    # collect_papers_Alabama(all_papers)
    # collect_papers_Alaska(all_papers)
    # collect_papers_Maryland(all_papers)
    # collect_papers_Michigan(all_papers)
    # collect_papers_California(all_papers)
    # collect_papers_Maine(all_papers)

    collect_all_us(all_papers) 



main()