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

class CountriesHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        global section_open
        global list_of_countries
        if (tag == "span" and ('class', 'mw-headline') in attrs):
            for item in attrs:
                if item[0] == 'id':
                    if len(item[1]) > 1: # make sure we're still looking at the cities section
                        section_open = False 
                        return
                    else:
                        print("SECTION: " + item[1])
                        section_open = True
        if(tag == 'a' and section_open):
            for item in attrs:
                if item[0] == 'title' and "List of cities in " in item[1]:
                    new_country = Country(item[1].split("List of cities in ",1)[1])
                    for attr in attrs:
                        if attr[0] == 'href':
                            new_country.url_with_cities_list = attr[1]
                    list_of_countries.append(new_country)
                    

    def handle_endtag(self, tag):
        # print("Encountered an end tag :", tag)
        # if (tag == "title"):
        #     self.titleOpen = 0
        return

    def handle_data(self, data):
        # print("Encountered some data  :", data)
        # if (self.titleOpen == 1):
        #     title = data.split(":")[0]
        #     title = title.replace(" ", "")
        #     title = title.strip("#")
        #     trendsByHour.append(title)
        return


def parse_country_list(filename, city_names):
    f = open(filename,"r")
    contents = f.read()
    parser = CountriesHTMLParser()
    parser.feed(contents)

def collect_city_names():
    filename = "List_of_cities_by_country_wikipedia.txt"

    req = Request("https://en.wikipedia.org/wiki/Lists_of_cities_by_country", headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read().decode("utf-8") 
    f = open(filename,"w+")
    f.write(webpage)
    f.close()
    
    city_names = []
    parse_country_list(filename, city_names)

def main():
    collect_city_names()
    for item in list_of_countries:
        print(item)


main()