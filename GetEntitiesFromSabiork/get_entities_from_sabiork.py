#! /usr/bin/env python

# disclaimer: I am not quite clear about the coding conventions of python
# I try to be consistent within this one file.
# I try to make things readable
#

# Import the required modules
import json
from urllib.request import urlopen

import xmltodict

# FIXME two types of request libraries.
# works for the moment, needs to be changed.
import requests

import time

def get_json_for_pubmed_id( pubmed_id ):
    response = urlopen('https://sabiork.h-its.org/testSabio/entry/getJSONentriesByPubMedId?pubmedId=%s' % pubmed_id)

    if response.getcode() == 200:
        # Parse JSON in Python
        all_result = response.read()
        print(all_result)

        data = json.loads(all_result.decode('utf-8'))

        return data
    return None

# data = get_json_for_pubmed_id( 7437446 )


# Heavily based on example code available at: 
# https://sabiork.h-its.org/layouts/content/docuRESTfulWeb/searchPython.gsp

def get_sbml_for_entry_id( entry_id ):

    response = urlopen('http://sabiork.h-its.org/testSabio/sabioRestWebServices/kineticLaws/%d' % entry_id)

    print(response)
    if response.getcode() == 200:

        all_result = response.read()
        print(all_result)

        data = all_result.decode('utf-8')
        return data
    return None


def get_all_entry_ids():

    ENTRYID_QUERY_URL = 'http://sabiork.h-its.org/testSabio/sabioRestWebServices/searchKineticLaws/entryIDs'
    PARAM_QUERY_URL = 'http://sabiork.h-its.org/testSabio/entry/exportToExcelCustomizable'
    entryIDs = []


    # ask SABIO-RK for all EntryIDs matching a query
    # (/ 50000 3600) would take 13 hours for 50k entries

    query_dict = {"Organism":'*'}
    query_string = ' AND '.join(['%s:%s' % (k,v) for k,v in query_dict.items()])
    query = {'format':'txt', 'q':query_string}


    # make GET request

    request = requests.get(ENTRYID_QUERY_URL, params = query)
    request.raise_for_status() # raise if 404 error


    # each entry is reported on a new line

    entryIDs = [int(x) for x in request.text.strip().split('\n')]
    print('%d matching entries found.' % len(entryIDs))

    print(entryIDs)

    return entryIDs

entry_ids = get_all_entry_ids();

for entry_id in entry_ids:

    recount = 3

    while(recount > 0):
        try:
            j = get_sbml_for_entry_id( entry_id )

            f = open("JsonEntries/entry%06d.json" % entry_id,"w")


            print(j)

            entry = xmltodict.parse(j)

            json.dump(entry,f,indent=4)
            print(json.dumps(entry,indent=4))

            f.close()
            time.sleep(0.3)
            # first try was successful
            recount = 0
        except:
            # try again
            recount = recount - 1
            print("Failure, retrying after wait %d" % entry_id)
            time.sleep(2)

