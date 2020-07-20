## ETL of Wikipedia
Documentation for the current ETL process of Wikipedia-provided local newspapers

### Extract
This is accomplished by the `globalExtractWiki.py` script. The algorithm works
by descending the hierarchy provided by Wikipedia's newspaper collection page:
https://en.wikipedia.org/wiki/Lists_of_newspapers. It pulls the HTML data from
each site it visits, starting with simply descending to individual newspaper's
Wikipedia pages. When it reaches this destination it will scrape all data
Wikipedia provides on the specific newspaper (specifically the data found in the
pages `v-infobox` HTML element). This data is collected in memory and after scraping,
parsed/interpretted to remove all HTML. (*NOTE*: currently the script will zero-out 
unrecognized attributes/tags which may result in lots of empty columns. This is 
a work in progress and will depend upon what attributes are deemed significant.)
Finally the interpretted data is exported as a CSV file into the working directory.

The script currenty supports two modes,**Limit** and **Target** mode. 
**Limit** mode will scan each *region*, *subregion*, and *state/territory* used 
in Wikipedia's heirarchical organization and select a set number of the lowest 
viable category (i.e. if the subregion doesn't have states/territories, it will 
simply move on to the next subregion. But if it does have states, then the 
algorithm will select the set number of states from that subregion). In **Target** mode, the user can specify the exact region/subregion/ state (or territory) 
they're interested in. The keyword `all` may also be used to select every 
option possible from that specific level. For example, a query may look like:
```python
TARGET_REGION = 'all'
TARGET_SUBREGION = 'United States' 
TARGET_STATE = 'Puerto Rico' 
```

*See `dump.csv` for reference dump.*

### Transform
Still under construction, will depend significantly upon what newspaper attributes
are deemed significant. The current structure uses a Jupyter Notebook, 
`globalTransformWiki.ipynb` to import the dumped CSV from `globalExtractWiki.py`.
The data is imported into a `pandas` DataFrame for manipulation. The current
pipeline is as follows:
1. Drop unnecessary columns
2. Bin categorical data
3. Convert datatypes 
4. Load/Export data

There will most likely be more detail in this process once the data features are
determined.

### Load
In progress. Currently the final data can be uploaded to a server or simply exported locally. 

*See `clean_data.csv` for reference output.*
