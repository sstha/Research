"Reads the file with AS to country mapping into a dictionary"

import itertools
import csv
asncndict={}

def asndict():
    with open ('/Users/shwetashrestha/research/research/allascn.csv','r') as fasn:
        reader=csv.DictReader(fasn)
        for lines in reader:
            asncndict.update({lines['asn']:lines['country']})
            #asncndict={lines['asn']:lines['country']}
        return asncndict

