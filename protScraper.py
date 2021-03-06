#! /usr/bin/env python
import sys
from os import path
from bs4 import BeautifulSoup
import copy
import requests
import re

def uniprotFromGeneID(geneID):
    html = requests.get("http://www.ncbi.nlm.nih.gov/gene/" + str(geneID))
    bs = BeautifulSoup(html.text, 'lxml')
    search = bs.find_all(id="proteinTblId")[1].tbody.tr.find("a", href=re.compile("http://www.uniprot.org/entry/*")).get("href")
    uniprotURL = None if not search else search
    return uniprotURL

def relatedStructuresFromUniprot(uniprotURL):
    html = requests.get(uniprotURL)
    bs = BeautifulSoup(html.text, 'lxml')
    table = next(bs.find_all(class_="databaseTable STRUCTURE")[0].children).find_all("td")[1].table
    rows = table.find_all("tr")
    columns = []
    # Here we extract the column headers for use in our default dictionary.
    for i in rows[0].find_all("td"):
        columns.append(i.text.strip().lower())
    # We've handled the first row, now we work on the rest.
    rows = rows[1:]
    collected = []
    for i in rows:
        newRow = []
        for j in i.find_all("td"):
            newRow.append(j.text)
        collected.append(newRow)
    ret = []
    for i in collected:
        ret.append(dict(zip(columns, i)))
    return ret

def numProteinInteractions(uniprotID):
    html = requests.get("http://www.uniprot.org/uniprot/%s" % uniprotID)
    bs = BeautifulSoup(html.text, 'lxml')
    # Ask at your own risk.
    return int(bs.find_all(class_="databaseTable INTERACTION")[0].tr.find_all('td')[1].text.split('.')[1].strip().split(' ')[0])



def main(argv):
    try:
        with open(path.abspath(path.join(argv[1], "a.txt")), 'w') as f:
            relatedStructures = relatedStructuresFromUniprot(uniprotFromGeneID(argv[0]))
            for i in relatedStructures:
                for j in i['chain'].split("/"):
                    try:
                        f.write(i['entry'].lower() + ":" + j + "\n")
                    except:
                        pass
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

if __name__ == "__main__":
    main(sys.argv[1:])






