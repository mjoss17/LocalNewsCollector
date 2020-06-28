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


class State_Newspapers_Index_Parser(HTMLParser):

    urls = []
    span = False
    look_for_lists = False

    def handle_starttag(self, tag, attrs):
        if tag == "span":
            self.span = True
        if tag == "a":
            if self.look_for_lists == True:
                for attr in attrs:
                    if attr[0] == 'href':
                        if "/wiki/" in attr[1]:
                            self.urls.append("https://en.wikipedia.org" + attr[1])
                            
    def handle_endtag(self, tag):
        self.span = False

    def handle_data(self, data):
        if self.span:
            if "newspapers" in data or "Newspapers" in data:
                if "daily" in data or "Daily" in data or "weekly" in data or "Weekly" in data:
                    self.look_for_lists = True

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
    filename = "W_html.txt"
    site = "https://en.wikipedia.org/wiki/List_of_newspapers_in_Michigan"
    req = Request(site, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read().decode("utf-8") 
    f = open(filename,"w+")
    f.write(webpage)
    f.close()
    parse_newspapers_from_state_Wikipedia(filename, all_paper_urls, "Michigan")


def collect_papers_Alabama(all_paper_urls):
    filename = "W_html.txt"
    site = "https://en.wikipedia.org/wiki/List_of_newspapers_in_Alabama"
    req = Request(site, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read().decode("utf-8") 
    f = open(filename,"w+")
    f.write(webpage)
    f.close()
    parse_newspapers_from_state_Wikipedia(filename, all_paper_urls, "Alabama")


def collect_papers_Maryland(all_paper_urls):
    filename = "W_html.txt"
    site = "https://en.wikipedia.org/wiki/List_of_newspapers_in_Maryland"
    req = Request(site, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read().decode("utf-8") 
    f = open(filename,"w+")
    f.write(webpage)
    f.close()
    parse_newspapers_from_state_Wikipedia(filename, all_paper_urls, "Maryland")

def collect_papers_California(all_paper_urls):
    filename = "W_html.txt"
    site = "https://en.wikipedia.org/wiki/List_of_newspapers_in_California"
    req = Request(site, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read().decode("utf-8") 
    f = open(filename,"w+")
    f.write(webpage)
    f.close()
    parse_newspapers_from_state_Wikipedia(filename, all_paper_urls, "California")

def collect_papers_Maine(all_paper_urls):
    filename = "W_html.txt"
    site = "https://en.wikipedia.org/wiki/List_of_newspapers_in_Maine"
    req = Request(site, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read().decode("utf-8") 
    f = open(filename,"w+")
    f.write(webpage)
    f.close()
    parse_newspapers_from_state_Wikipedia(filename, all_paper_urls, "Maine")


    
def parse_newspapers_from_state_Wikipedia(filename, all_paper_urls, name):
    f = open(filename, "r")
    contents = f.read()
    parser = State_Newspapers_Index_Parser()
    parser.feed(contents)
    parse_urls(parser, all_paper_urls, name)

def parse_urls(parser, all_paper_urls, name):
    # print(parser.get_urls())
    wiki_paper_urls = []
    for url in parser.get_urls():
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read().decode("utf-8") 
        f = open("temp1.txt","w+")
        f.write(webpage)
        f.close()

        f = open("temp1.txt", "r")
        contents = f.read()
        parser = If_()
        parser.feed(contents)
        if parser.is_paper():
            wiki_paper_urls.append(url)
            get_website_url(url, all_paper_urls)

        new_path = os.path.join('./urls/', str(name) + '.txt')
        f = open(new_path,"w+")
        for website in all_paper_urls:
            f.write(str(website) + '\n')
        f.close()

def get_website_url(wiki_url, all_paper_urls):
    req = Request(wiki_url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read().decode("utf-8") 
    f = open("temp1.txt","w+")
    f.write(webpage)
    f.close()

    f = open("temp1.txt", "r")
    contents = f.read()
    parser = Paper_Attributes_Parser()
    parser.feed(contents)

    website = parser.get_website()
    if website != "" and website != None and website != " ":
        if website not in all_paper_urls:
            all_paper_urls.append(website)
            print(website)

    
def main():
    all_paper_urls = []
    # collect_papers_Alabama(all_paper_urls)
    # collect_papers_Maryland(all_paper_urls)
    # collect_papers_Michigan(all_paper_urls)
    # collect_papers_California(all_paper_urls)
    collect_papers_Maine(all_paper_urls)


main()