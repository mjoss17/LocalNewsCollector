from html.parser import HTMLParser


class State_Newspapers_Index_Parser(HTMLParser):

    
    
    def initialize(self):
        self.urls = []
        self.span = False
        self.h2_open = True
        self.look_for_lists = False

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

    def clear_urls(self):
        self.urls = []


class Check_If_Actually_Paper_Parser(HTMLParser):

    def initialize(self):
        self.paragraph_count = 0
        self.p_open = False
        self.is_newspaper = False
        self.publisher = False

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


    def initialize(self):
        self.table_open = False
        self.url_open = False
        self.website_url = ""

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
    
    def initialize(self):
        self.h2_open = False
        self.span_open = False
        self.collecting_sites = False
        self.wiki_indexes = []

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