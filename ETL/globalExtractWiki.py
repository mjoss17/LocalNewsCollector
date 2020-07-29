"""
globalExtractTesting.py
Author: Peter Gish
Created On: 7/19/20
Last Modified: 7/22/20
Description: ETL attempts to pull data from wikipedias 'Global Newspapers' page.
            Current strategy is to use Python's request library to visit each 
            webpage then use BeautifulSoup to parse the page and extract 
            relevant data into a dictionary. This dictionary is then reformatted 
            and converted into a pandas DataFrame for effecient data manipulation 
            and transformation. Only stores data from newspaper sites with
            an "infobox" 

Output: A CSV file containing the scraped data with the name assigned to
        "OUTPUT_FILE"

Dependencies:
    - BeautifulSoup4
    - lxml
    - Pandas

TESTING: Currently the program is capped at TEST_LIMIT sub-region per 
        region. Alternatively TARGET_MODE can be used to only parse a specific
        region/subregion/state. Each "filter level" can also be set to "all".
        Details for valid parameters can be found in `validWikiFilters.json`

TODO: 
    - Handle more exceptions
        - Check US states accuracy (for ex. US Virgin Islands isn't parsed &
                                    Utah brings in location data)
        - Currently only parse US Newspapers in the "by state/territory" section.
    - Handle repeate subregions (causes unnecessary parsing)
    - Increase accuracy of newspaper-collection pages --> extracting newspapers
    - Improve newspaper-specific page parsing
"""

# Built-in Modules
import requests
import re
import json # temp storage

# 3rd-Party Modules
from bs4 import BeautifulSoup, NavigableString, Tag
import pandas as pd

## Global Variables
ENTRY_URL = 'https://en.wikipedia.org/wiki/Lists_of_newspapers'
BASE_URL = 'https://en.wikipedia.org'
USER_HEADER = (f'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                f'(KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36')
HEADERS = {'User-Agent': USER_HEADER}

OUTPUT_FILE = 'dump.csv'

# Australia might need to go in here too + China
EXCEPTIONS = {'United States': 'UnitedStates'} # store titles + method names
EXCLUDE_TABLES = ('Contents', 'See_also', 'References', 'Bibliography', 
                    'External_links', 'Further_reading')

INDEX_LEVEL_NAMES = ('Region', 'Subregion', 'State/Territory', 'Newspaper')

PAPER_SPECS = ('Type', 'Format', 'Industry', 'Founded', 'Headquarters', 'Owner',
                'Owner(s)', 'Founder', 'Founder(s)', 'Number of employees', 'Circulation', 
                'Language', 'Publisher', 'Editor', 'Political alignment', 'Country', 
                'ISSN', 'Launched', 'City', 'Editor-in-chief', 'President',
                'Managing editors', 'Opinion editor', 'Sports editor', 'Photo editor',
                'Staff writers', 'Sister newspapers', 'General manager', 
                'Ceased publication', 'Campus editor', 'Metro editor', 
                'Readership', 'First issue', 'Based in', 'Frequency', 'Year founded',
                'Established', 'Key people')

NULL_SEQ = 'NULL'
GLOBAL_COLLECTION = {}
EXTERNAL_SITE_TAG = Tag(name='a')
EXTERNAL_SITE_TAG.string = 'External site'
TABLE_REGEX = re.compile(r'^(wikitable)(\s\w*)*')
PAPER_INFO_REGEX = re.compile(r'(infobox vcard)|(infobox hproduct)')
PAPER_URL_EXTRACT = re.compile(r'([Tt]he)|\s|_|(#.*)|\(\w*\)')

# Purely for testing
TESTING_LIMIT = 3 # loop cap for extract
TARGET_MODE = False

""" 
For valid Regions / Subregions / States refer to `validWikiFilters.json`
"""
# Can use 'all' keyword to get all values (will override TESTING LIMIT)
# WARNING: 'all' will most likely take a long time to execute
# WARNING: no check for validity of REGION <--> SUBREGION <--> STATE relationship
TARGET_REGION = 'all'
TARGET_SUBREGION = 'United States' 
TARGET_STATE = 'Puerto Rico' 
DUMP = True


## Global Functions
def filterPaperTags(tag):
    """Used to extract paper names on sub-region page tables. 
    
    Skip pages that don't exist.
    
    params:
        - tag (bs4.Tag): Current tag being inspected
    returns:
        - bool indicating pass/fail of filter
    """
    if tag.name == 'a' and tag.has_attr('href'):
        if tag.has_attr('title') and tag.string:
            if tag.parent.name in ('i', 'li', 'td') and \
                        'page does not exist' not in tag['title']:
                tag_title = re.sub(PAPER_URL_EXTRACT, '', tag['title']).casefold()
                tag_string = re.sub(PAPER_URL_EXTRACT, '', tag.string).casefold()
                return tag_title in tag_string or tag_string in tag_title
                # return re.sub(PAPER_URL_EXTRACT, '', tag['title']).casefold() ==\
                #      re.sub(PAPER_URL_EXTRACT, '', tag['href']).casefold()[len('/wiki/'):]
                     
        elif tag.has_attr('class'):
            return tag['class'] in (['external', 'text'], ['external', 'free'],
                                    ['external', 'autonumber'])

    return False


def formatData(collection_dict):
    """Format the dictionary created when aggregating data during scraping.

    First step is extracting data from tags then it's necessary to reformat
    the nested dictionary in preperation for transformation into a DataFrame.
    
    params:
        - collection_dict (dict): dictionary created during scraping
    returns:
        - reformatted dictionary with no Tag datatypes and only single level
    """
    for region in collection_dict.values():
        for sub_region_key, sub_region_val in region.items():
            for state in sub_region_val.values():
                for paper in state.values():
                    for attribute in paper:
                        # Extract data based on stored tag
                        if attribute in PAPER_SPECS: 
                            # TODO: This isn't parsing properly. Might need to break
                            # up group of PAPER_SPECS with individual/subgroup conditions
                            if len(paper[attribute].contents) > 1:
                                # not sure if this is sustainable
                                primary_element = paper[attribute].contents[0] 
                                if primary_element.string:
                                    paper[attribute] = primary_element.string
                                elif primary_element.title:
                                    paper[attribute] = primary_element.title
                                elif primary_element.has_attr('href'):
                                    paper[attribute] = primary_element['href']
                                elif primary_element.ul:
                                    if val := primary_element.ul.find('li'):
                                        paper[attribute] = val.string
                                else: # Throw away data
                                    # print(f'Unrecognized format: {attribute}, {paper[attribute]}')
                                    paper[attribute] = None
                            else:
                                paper[attribute] = paper[attribute].string
                        elif attribute == 'Website':
                            if tag := paper[attribute].find(class_='external text'):
                                paper[attribute] = tag.get('href', None)
                            elif tag := paper[attribute].find(class_='external free'):
                                paper[attribute] = tag.get('href', None)
                            elif tag := paper[attribute].find(class_='external autonumber'):
                                paper[attribute] = tag.get('href', None)
                            elif tag := paper[attribute].find(class_='mw-redirect'):
                                paper[attribute] = tag.get('href', None)
                            elif tag := paper[attribute].get('href', None):
                                paper[attribute] = tag
                            elif paper[attribute].string:
                                paper[attribute] = paper[attribute].string
                        elif attribute == 'Free online archives':
                            if tag := paper[attribute].find('a'):
                                paper[attribute] = tag.get('href', None)
                            else:
                                paper[attribute] = paper[attribute].string
                        elif attribute == None:
                            # need to delete somehow...
                            paper[attribute] = None
                        else: # Throw away data
                            # print(f'Unknown attribute: {attribute}, {paper[attribute]}')
                            paper[attribute] = None
    
    # Flatten dictionary (phat boi, I don't like this) 
    # NOTE: maybe look into using numpy arrays instead of nested dict.
    # cause this is gross
    return {(region_key, sub_region_key, state_key, paper_key): paper_data for 
                    region_key, sub_region_dict in collection_dict.items() for 
                    sub_region_key, states_dict in sub_region_dict.items() for
                    state_key, papers_dict in states_dict.items() for
                    paper_key, paper_data in papers_dict.items()}


def parseIndividualPaper(newspaper_tag):
    """ Parse a specific newspaper's webpage for all specs in the pages "infobox".

    If the page does not have an "infobox", function returns None, None

    params:
        - newspaper_tag (bs4.Tag): tag containing the href for the newspaper's
                                    wiki page
    returns:
        - paper_name, paper_info_tags (tuple): a tuple of the paper's name and
                                                a dict of all parsed specs 
    """
    paper_info_tags = {}
    page = requests.get(f"{BASE_URL}{newspaper_tag['href']}", 
                            headers=HEADERS, allow_redirects=False)

    page_soup = BeautifulSoup(page.content, 'lxml', from_encoding='utf-8')

    # NOTE: attempt to catch redirect, not sure if this means that the redirected
    # page is invalid 100% of the time. could be dropping data unintentionally
    page_link = re.sub(PAPER_URL_EXTRACT, '', page_soup.find('link', 
                        attrs={'rel': 'canonical'})['href']).casefold()\
                        [len(BASE_URL + '/wiki/'):]
    page_url = re.sub(PAPER_URL_EXTRACT, '', page.url).casefold()\
                        [len(BASE_URL + '/wiki/'):]
 
    if not (page_link in page_url or page_url in page_link):
        return None, None

    info_table = page_soup.find('table', attrs={'class': PAPER_INFO_REGEX})
    if info_table and info_table.tbody:
        for row in [tag for tag in info_table.tbody.children if isinstance(tag, Tag)]:
            if row.th and row.th.has_attr('scope') and row.th['scope'] == 'row': 
                key = row.th.string
                if key == 'Website' and row.td.span:
                    val = row.td.span
                else:
                    val = row.td
                paper_info_tags[key] = val
    else:
        return None, None
    paper_header = page_soup.find(id='firstHeading')
    if paper_header.i:
        paper_name = paper_header.i.string
    else:
        paper_name = paper_header.string

    return paper_name, paper_info_tags


def parsePaperCollectionPage(collection_tag):
    """Parse a newspaper collection page for all newspaper tags.

    params:
        - collection_tag (bs4.Tag): tag containing href of collections page
    return:
        - standard_paper_tags, external_sites (tuple): tuple containing list of 
                                                    scraped newspaper tags and
                                                    list of external sites tags
    """

    page = requests.get(f"{BASE_URL}{collection_tag['href']}", 
                            headers=HEADERS)
    page_soup = BeautifulSoup(page.content, 'lxml', 
                                        from_encoding='utf-8')
    paper_tags = []
    external_sites = []

    # Inspect all tables
    for table in page_soup.find_all('table', attrs={'class': TABLE_REGEX}):
        for row in table.tbody.children:
            if isinstance(row, Tag):
                if row.contents:
                    first_entry = row.contents[1]
                    if tag := first_entry.find(filterPaperTags):
                        if tag.has_attr('class') and tag['class'] in \
                                (['external', 'text'], ['external', 'free'],
                                ['external', 'autonumber']):
                            external_sites.append(tag)
                        else:
                            paper_tags.append(tag)

    # Inspect all lists
    for list_ in page_soup.find_all('ul'):
        valid = False
        # print(list_.parent.get('class', None))
        if sib_header := list_.find_previous('h2'):
            if header_tag := sib_header.find('span'):
                if header_tag.has_attr('id') and header_tag['id'] not in EXCLUDE_TABLES:
                    valid = True
    
        elif list_.parent.get('class', None) == ['mw-parser-output']:
            valid = True

        if valid:
            for row in [element for element in list_.find_all('li') if isinstance(element, Tag)]:
                first_entry = row.find('i')
                if not isinstance(first_entry, Tag):
                    first_entry = row.find('a')
                # print(first_entry)
                if tag := first_entry.find(filterPaperTags):
                    # print(tag)
                    if tag.has_attr('class') and tag['class'] in \
                        (['external', 'text'], ['external', 'free'],
                        ['external', 'autonumber']):
                        external_sites.append(tag)
                    else:
                        paper_tags.append(tag)

    return paper_tags, external_sites


def handleStandardPaperCollection(locations_dict, region, subregion=None, limit=None):
    """"Governor" function to collect newspaper-data from a list of location tags. 

    Delegates parsing of each location webpage to parsePaperCollectionPage().
    Uses parseIndividualPaper() to extract significant data from each paper
    gathered by the initial parsing. Store extracted newspaper date in 
    the global dictionary, GLOBAL_COLLECTION.

    params:
        - locations_dict (dict): dictionary of location names + 
                                    associated tags.
        - region (str): name of region containing all subregions in 
                        locations_dict.
        - subregion (str): name of subregion containing states in 
                            locations_dict.
        - limit (int): loop cap for testing - represents number of subregions to 
                        explore.
    """

    if subregion:
        subregion_key = subregion
        state_key = None
    else:
        subregion_key = None
        # need to fill in "state/territory" index, use NULL_SEQ --> ewwwwwww
        state_key = NULL_SEQ 

    if not limit:
        limit = len(locations_dict)
    elif limit > len(locations_dict):
        limit = len(locations_dict)
    elif limit <= 0:
        return

    count_iter = 0 # For limiting queries when testing

    for location_name, location_tag in locations_dict.items():
        if count_iter == limit:
            break # Purely to cap loop during testing
        
        if state_key == NULL_SEQ:
            subregion_key = location_name
        else:
            state_key = location_name
        GLOBAL_COLLECTION[region][subregion_key] = {state_key: {}}

        subregional_papers, external_sites = parsePaperCollectionPage(location_tag)

        for paper in subregional_papers:
            paper_name, paper_info_tags = parseIndividualPaper(paper)
            if paper_name:
                GLOBAL_COLLECTION[region][subregion_key][state_key][paper_name] \
                    = paper_info_tags
                print(f'stashed Paper: {paper_name}\tfrom {location_name} in {region}')
        
        for site in external_sites:
            if site.has_attr('href'):
                GLOBAL_COLLECTION[region][subregion_key][state_key][site.string] \
                        = {'Type': EXTERNAL_SITE_TAG, 'Website': site}
                print(f'stashed External: {site.string}\tfrom {location_name} in {region}')

        count_iter += 1


def handleUnitedStates(us_landing_tag, limit=None):
    """Exception to "standard collection".
    
    Visit and scrape each state's newspaper-collection webpage. Pass
    states tags to handleStandardPaperCollection()

    params:
        - us_landing_tag (bs4.Tag): tag contains href of United States 
                                    newspapers web page.
        - limit (int): loop cap for testing - represents number of regions to 
                        explore. (will be overridden by TARGET MODE params)
    """

    # Collect individual states' tags
    page = requests.get(f"{BASE_URL}{us_landing_tag['href']}", 
                            headers=HEADERS)
    page_soup = BeautifulSoup(page.content, 'lxml', from_encoding='utf-8')
    states_list = page_soup.find('div', class_='div-col columns column-width')

    states_tags = {}
    for state in states_list.find_all('a'):
        states_tags[state.string] = state
    
    if TARGET_MODE:
        if TARGET_STATE == 'all':
            limit = len(states_tags)
        elif TARGET_STATE in states_tags:
            states_tags = {TARGET_STATE: states_tags[TARGET_STATE]}
        else:
            return
    
    handleStandardPaperCollection(states_tags, 'North America', 
                                    'United States', limit=limit)


## Main 
# Visit entry webpage
entry_page = requests.get(ENTRY_URL, headers=HEADERS)
if entry_page.status_code != 200:
    print(f"""ERROR: Could not download global newspapers page. 
    Status code {entry_page.status_code}.
    Exiting...""")
    exit(1)
entry_soup = BeautifulSoup(entry_page.content, 'lxml', from_encoding='utf-8')

# Collect names of regions and drop "See Also" section
region_headers = entry_soup.find_all('span', class_='mw-headline')[:-1]

# Apply TARGET MODE 
if TARGET_MODE:
    if TARGET_REGION == 'all':
        pass
    elif TARGET_REGION in [tag.string for tag in region_headers]:
        region_headers = [entry_soup.find('span', id=TARGET_REGION.replace(' ', '_'))]
    else:
        region_headers.clear()


# Collect sub-region names + urls
title_regex = re.compile(r'^(List of newspapers in)( *\w ?)+(?<!\(page does not exist\))$')
for region in region_headers:
    GLOBAL_COLLECTION[region.string] = {}
    standard_subregion_urls = {}
    exception_subregion_urls = {}

    label = f"List_of_newspapers_in_{region['id']}"
    for tag in entry_soup.find_all('div', class_='navbox', 
                                                attrs={'aria-labelledby': label}):
        target_elements = [element for element in tag.find_all('a', 
                                                    attrs={'title': title_regex}) 
                            if element.parent.name == 'li']
        for element in target_elements:
            if element.string not in EXCEPTIONS:
                standard_subregion_urls[element.string.strip()] = element
            else:
                exception_subregion_urls[element.string.strip()] = element

    # Parse each subregions newspapers' webpage
    if TARGET_MODE:
        if TARGET_SUBREGION == 'all':
            pass
        elif TARGET_SUBREGION in standard_subregion_urls:
            standard_subregion_urls = {TARGET_SUBREGION: 
                                        standard_subregion_urls[TARGET_SUBREGION]}
            exception_subregion_urls.clear()

        elif TARGET_SUBREGION in exception_subregion_urls:
            exception_subregion_urls = {TARGET_SUBREGION:
                                        exception_subregion_urls[TARGET_SUBREGION]}
            standard_subregion_urls.clear()
        else:
            standard_subregion_urls.clear()
            exception_subregion_urls.clear()

    handleStandardPaperCollection(standard_subregion_urls, region.string, 
                                                        limit=TESTING_LIMIT)
    for subregion, tag in exception_subregion_urls.items():
        if fn := globals()[f"handle{EXCEPTIONS[subregion]}"]:
            fn(tag, limit=TESTING_LIMIT)

if DUMP:
    # Format global dictionary to be easily imported as pandas df
    formatted_dict = formatData(GLOBAL_COLLECTION)

    df = pd.DataFrame(formatted_dict).T
    if len(df.index.names) == len(INDEX_LEVEL_NAMES):
        df.index.names = INDEX_LEVEL_NAMES
        # Default is utf-8 encoding, will look weird in Excel, designed to be imported
        # by pandas in Jupyter Notebook
        print('dumping data')
        df.to_csv(OUTPUT_FILE)

    else:
        print('Empty collection')


