import json
import re
from collections import defaultdict
import operator 
import heapq
import random
import itertools
from sklearn.utils import murmurhash3_32
from html.parser import HTMLParser
from urllib.request import Request, urlopen
import urllib.request


section_open = False
list_of_countries = []

class Country():
    name = ""
    url_with_cities_list = ""
    cities = []

    def __init__(self, name_in):
        self.name = name_in

    def __str__(self):
        return self.name

class Cities():
    name = ""
    population = 0
    papers = []
    
    def __init__(self, name_in):
        self.name = name_in

    def __str__(self):
        return self.name

class Newspaper():
    name = ""
    url = ""

    def __init__(self, url_in):
        self.url = url_in


class NP_by_State_Parser(HTMLParser):

    # def __init__(self):
    urls = []
    data_type = ""
    span = False
    look_for_lists = False

    def handle_starttag(self, tag, attrs):
        if tag == "h2":
            if self.look_for_lists == True:
                self.look_for_lists = False
            self.data_type = "h2"
        if tag == "span":
            self.span = True
        if tag == "a":
            if self.look_for_lists == True:
                for attr in attrs:
                    if attr[0] == 'href':
                        if "/wiki/" in attr[1]:
                            self.urls.append("https://en.wikipedia.org" + attr[1])
                            
    def handle_endtag(self, tag):
        self.data_type = ""
        self.span = False

    def handle_data(self, data):
        # if data_type == "h2":
            # print(data)

        if self.span:
            if "newspapers" in data or "Newspapers" in data:
                if "daily" in data or "daily" in data or "weekly" in data or "weekly" in data:
                    self.look_for_lists = True

    def get_urls(self):
        return self.urls


class Check_Actually_Paper_Parser(HTMLParser):
    paragraph_count = 0
    p_open = False
    is_newspaper = False

    def handle_starttag(self, tag, attrs):
        if tag == "p" and self.paragraph_count < 3:
            self.p_open = True
            self.paragraph_count += 1


    def handle_endtag(self, tag):
        if tag == "p":
            self.p_open = False

    def handle_data(self, data):
        if self.p_open:
            if "newspaper" in data or "Newspaper" in data:
                self.is_newspaper = True
    
    def is_paper(self):
        return self.is_newspaper


class Paper_Attributes_Parser(HTMLParser):

    table_open = False
    url_open = False
    website_url = ""

    def handle_starttag(self, tag, attrs):
        if tag == "table" and ('class', 'infobox vcard') in attrs:
                self.table_open = True
        if self.table_open and tag == "span":
            if ('class', 'url') in attrs:
                self.url_open = True
        if self.url_open and tag == "a":
            for attr in attrs:
                if attr[0] == 'href':
                    self.website_url = attr[1]

    def handle_endtag(self, tag):
        if tag == "table" and self.table_open == True:
            self.table_open == False
        if tag == "span" and self.url_open:
            self.url_open = False 


    def handle_data(self, data):
        return

    def get_website(self):
        return self.website_url





def collect_papers_Michigan(all_paper_urls):
    filename = "Wikipedia_newspapers_in_Michigan.txt"
    req = Request("https://en.wikipedia.org/wiki/List_of_newspapers_in_Michigan", headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read().decode("utf-8") 
    f = open(filename,"w+")
    f.write(webpage)
    f.close()

    parse_newspapers_from_state_Wikipedia(filename, all_paper_urls)

def collect_papers_Alabama(all_paper_urls):
    filename = "Wikipedia_newspapers_in_Alabama.txt"
    req = Request("https://en.wikipedia.org/wiki/List_of_newspapers_in_Alabama", headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read().decode("utf-8") 
    f = open(filename,"w+")
    f.write(webpage)
    f.close()

    parse_newspapers_from_state_Wikipedia(filename, all_paper_urls)


def collect_papers_Maryland(all_paper_urls):
    filename = "Wikipedia_newspapers_in_Maryland.txt"
    req = Request("https://en.wikipedia.org/wiki/List_of_newspapers_in_Maryland", headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read().decode("utf-8") 
    f = open(filename,"w+")
    f.write(webpage)
    f.close()

    parse_newspapers_from_state_Wikipedia(filename, all_paper_urls)

    
def parse_newspapers_from_state_Wikipedia(filename, all_paper_urls):
    f = open(filename, "r")
    contents = f.read()
    parser = NP_by_State_Parser()
    parser.feed(contents)
    parse_urls(parser, all_paper_urls)

def parse_urls(parser, all_paper_urls):
    # print(parser.get_urls())
    wiki_paper_urls = []
    for url in parser.urls:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read().decode("utf-8") 

        f = open("test1.txt","w+")
        f.write(webpage)
        f.close()
        f = open("test1.txt", "r")
        contents = f.read()
        parser = Check_Actually_Paper_Parser()
        parser.feed(contents)
        if parser.is_paper():
            wiki_paper_urls.append(url)
            get_website_url(url, all_paper_urls)

    # print(wiki_paper_urls)

def get_website_url(wiki_url, all_paper_urls):
    filename = "test2.txt"
    req = Request(wiki_url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read().decode("utf-8") 
    f = open(filename,"w+")
    f.write(webpage)
    f.close()
    f = open("test1.txt", "r")
    contents = f.read()
    parser = Paper_Attributes_Parser()
    parser.feed(contents)
    website = parser.get_website()
    if website != "" and website != None and website != " ":
        if website not in all_paper_urls:
            print(website)
            all_paper_urls.append(website)





def main():
    all_paper_urls = []
    collect_papers_Michigan(all_paper_urls)
    



main()