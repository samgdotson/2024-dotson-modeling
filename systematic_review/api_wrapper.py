"""
Code inspired by and borrowed from PyScopus https://github.com/zhiyzuo/python-scopus
"""

import requests
import json
import pandas as pd


SEARCH = "http://api.elsevier.com/content/search/scopus"
SEARCH_AUTHOR = "http://api.elsevier.com/content/search/author"
AUTHOR = "http://api.elsevier.com/content/author/author_id"
ABSTRACT = "http://api.elsevier.com/content/abstract/scopus_id"
CITATION = "http://api.elsevier.com/content/abstract/citations"
SERIAL_SEARCH = "https://api.elsevier.com/content/serial/title"
SERIAL_RETRIEVAL = "https://api.elsevier.com/content/serial/title/issn/"
AFFL_RETRIEVAL = "https://api.elsevier.com/content/affiliation/affiliation_id/"


with open("es-api-key.txt", "r") as file:
    api_key = file.readlines()[0]


def search_scopus(query, return_type='dataframe', view="STANDARD", index=0, key=api_key):
    '''
        Search Scopus database using key as api key, with query.

        Parameters
        ----------
        key : string
            Elsevier api key. Get it here: https://dev.elsevier.com/index.html
        query : string
            Search query. See more details here:
            http://api.elsevier.com/documentation/search/SCOPUSSearchTips.htm
        view : string
            Returned result view (i.e., return fields). Can only be STANDARD for
            author search.
        index : int
            Starting index of view. "STANDARD" views have 25 results per page,
            so multiple requests will need to be made

        Returns
        -------
        pandas DataFrame
    '''

    par = {'apikey': key, 'query': query, 'start': index,
           'httpAccept': 'application/json', 'view': view}
    
    r = requests.get(SEARCH, params=par)

    results = r.json()

    total_count = int(results['search-results']['opensearch:totalResults'])
    if index==0:
        print(f"Total number of entries: {total_count}")
        
    if return_type.lower() == 'dataframe':
        entries = results['search-results']['entry']

        result_df = pd.DataFrame([parse_article(entry) for entry in entries])

        return result_df
    
    elif return_type.lower() == 'json':
        return results


def parse_article(entry):
    try:
        scopus_id = entry['dc:identifier'].split(':')[-1]
    except:
        scopus_id = None
    try:
        title = entry['dc:title']
    except:
        title = None
    try:
        publicationname = entry['prism:publicationName']
    except:
        publicationname = None
    try:
        issn = entry['prism:issn']
    except:
        issn = None
    try:
        isbn = entry['prism:isbn']
    except:
        isbn = None
    try:
        eissn = entry['prism:eIssn']
    except:
        eissn = None
    try:
        volume = entry['prism:volume']
    except:
        volume = None
    try:
        pagerange = entry['prism:pageRange']
    except:
        pagerange = None
    try:
        coverdate = entry['prism:coverDate']
    except:
        coverdate = None
    try:
        doi = entry['prism:doi']
    except:
        doi = None
    try:
        citationcount = int(entry['citedby-count'])
    except:
        citationcount = None
    try:
        affiliation = _parse_affiliation(entry['affiliation'])
    except:
        affiliation = None
    try:
        aggregationtype = entry['prism:aggregationType']
    except:
        aggregationtype = None
    try:
        sub_dc = entry['subtypeDescription']
    except:
        sub_dc = None
    try:
        author_entry = entry['author']
        author_id_list = [auth_entry['authid'] for auth_entry in author_entry]
    except:
        author_id_list = list()
    try:
        link_list = entry['link']
        full_text_link = None
        for link in link_list:
            if link['@ref'] == 'full-text':
                full_text_link = link['@href']
    except:
        full_text_link = None

    return pd.Series({'scopus_id': scopus_id, 'title': title, 'publication_name':publicationname,\
            'issn': issn, 'isbn': isbn, 'eissn': eissn, 'volume': volume, 'page_range': pagerange,\
            'cover_date': coverdate, 'doi': doi,'citation_count': citationcount, 'affiliation': affiliation,\
            'aggregation_type': aggregationtype, 'subtype_description': sub_dc, 'authors': author_id_list,\
            'full_text': full_text_link})