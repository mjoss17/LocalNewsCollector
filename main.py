import json
import re
from collections import defaultdict
import operator 
import heapq
import random
import itertools
from html.parser import HTMLParser
from urllib.request import Request, urlopen
import urllib.request
import os
from datetime import datetime

class Paper():
    def __init__(self):
        self.url = ""
        self.name = ""
        self.location = ""
    
    def __str__(self):
        return self.name

    



class State_Newspapers_Index_Parser(HTMLParser):

    urls = []
    span = False
    h2_open = True
    look_for_lists = False

    def handle_starttag(self, tag, attrs):
        if tag == 'h2':
            self.h2_open = True
        if tag == "span":
            self.span = True
        if tag == "a":
            if self.look_for_lists == True:
                for attr in attrs:
                    if attr[0] == 'href':
                        if "/wiki/" in attr[1]:
                            self.urls.append("https://en.wikipedia.org" + attr[1])
                            
    def handle_endtag(self, tag):
        if tag == 'span':
            self.span = False
        if tag == 'h2':
            self.h2_open = False

    def handle_data(self, data):
        if self.span:
            if self.h2_open == True:
                if "newspapers" in data or "Newspapers" in data:
                    if "daily" in data or "Daily" in data or "weekly" in data or "Weekly" in data:
                        self.look_for_lists = True
                if "See also" in data or "Refrences" in data or "refrences" in data:
                    self.look_for_lists = False

    def get_urls(self):
        return self.urls


class Check_If_Actually_Paper_Parser(HTMLParser):
    paragraph_count = 0
    p_open = False
    is_newspaper = False
    publisher = False

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
    def is_publisher(self):
        return self.is_publisher


class Collect_Paper_Attributes_Parser(HTMLParser):

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


class Collect_State_Indexes_Parser(HTMLParser):
    
    h2_open = False
    span_open = False
    collecting_sites = False
    wiki_indexes = []

    def handle_starttag(self, tag, attrs):
        if tag == 'h2' and self.h2_open == False:
            self.h2_open = True
        if tag == 'span' and self.h2_open == True: 
            for attr in attrs:
                self.span_open = True
        if tag == 'a' and self.collecting_sites == True:
            for attr in attrs:
                if attr[0] == 'href':
                    if attr[1] not in self.wiki_indexes:
                        if attr[1][:6] == "/wiki/":
                            self.wiki_indexes.append("https://en.wikipedia.org/" + attr[1])
        return
    
    def handle_endtag(self, tag):
        if tag == 'h2':
            self.h2_open = False
        if tag == 'span':
            self.span_open = False
        return

    def handle_data(self, data):
        if self.h2_open == True and self.span_open == True:
            if data == "By state and territory":
                self.collecting_sites = True

        if self.h2_open == True and self.span_open == True:
            if data == "Other lists of U.S. newspapers":
                self.collecting_sites = False
        return

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

def collect_papers_every_us_territory(all_paper_urls, url, dir_path):
    html_filename = "W_html.txt"
    territory_name = url.split("_in_",1)[1]
    print(territory_name)
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read().decode("utf-8") 
    f = open(html_filename,"w+")
    f.write(webpage)
    f.close()
    parse_newspapers_from_state_wikipedia_index(html_filename, all_paper_urls, territory_name, dir_path)

    




def parse_newspapers_from_state_wikipedia_index(html_filename, all_paper_urls, name, path):
    f = open(html_filename, "r")
    contents = f.read()
    parser = State_Newspapers_Index_Parser()
    parser.feed(contents)
    all_urls = parser.get_urls()
    f.close()

    all_news_urls_path = os.path.join(path + '/USA.txt')
    state_urls_path = os.path.join(path + '/', str(name) + '.txt')
    f = open(state_urls_path, 'w+')
    h = open(all_news_urls_path, 'w+')
    parse_urls(all_urls, all_paper_urls, f, h)
    h.close()
    

def parse_urls(all_urls, all_paper_urls, state_file, everything_file):

    wiki_paper_urls = []
    for url in all_urls:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            webpage = urlopen(req).read().decode("utf-8") 
        except:
            print("URL Error: " + url)
            continue

        f = open("temp1.txt","w+")
        f.write(webpage)
        f.close()

        f = open("temp1.txt", "r")
        contents = f.read()
        parser = Check_If_Actually_Paper_Parser()
        parser.feed(contents)
        if parser.is_paper():
            wiki_paper_urls.append(url)
            site_url = get_website_url(url, all_paper_urls)
            if site_url != None:
                state_file.write(str(site_url) + '\n')
                everything_file.write(str(site_url) + '\n')

        
        # all_news_urls_path = os.path.join(path + '/USA.txt')
        # h = open(all_news_urls_path, "w+")
        # for website in all_paper_urls:
        #     state_file.write(str(website) + '\n')
            # h.write(str(website) + '\n')
    state_file.close()
        # h.close()

def get_website_url(wiki_url, all_paper_urls):
    req = Request(wiki_url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read().decode("utf-8") 
    f = open("temp1.txt","w+")
    f.write(webpage)
    f.close()

    f = open("temp1.txt", "r")
    contents = f.read()
    parser = Collect_Paper_Attributes_Parser()
    parser.feed(contents)

    website = parser.get_website()
    if website != "" and website != None and website != " ":
        if website not in all_paper_urls:
            all_paper_urls.append(website)
            print(website)
            return website
    return None


def collect_all_us(all_papers):
    filename = "W_html.txt"
    site = "https://en.wikipedia.org/wiki/List_of_newspapers_in_the_United_States"
    req = Request(site, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read().decode("utf-8") 
    f = open(filename,"w+")
    f.write(webpage)
    f.close()


    f = open(filename, "r")
    contents = f.read()
    parser = Collect_State_Indexes_Parser()
    parser.feed(contents)

    dateTimeObj = datetime.now()
    dir_path = './urls_' + str(dateTimeObj.month) + '.' + str(dateTimeObj.day) + '.' + str(dateTimeObj.hour) + ':' + str(dateTimeObj.minute)
    os.mkdir(dir_path)

    for link in parser.wiki_indexes:
        collect_papers_every_us_territory(all_papers, link, dir_path)


    
def main():
    all_papers = []
    # collect_papers_Alabama(all_papers)
    # collect_papers_Maryland(all_papers)
    # collect_papers_Michigan(all_papers)
    # collect_papers_California(all_papers)
    # collect_papers_Maine(all_papers)

    collect_all_us(all_papers) 



main()