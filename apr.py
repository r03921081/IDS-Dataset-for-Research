"""
Description     : Simple Python implementation of the Apriori Algorithm
Usage:
    $python apriori.py -f DATASET.csv -s minSupport  -c minConfidence
    $python apriori.py -f DATASET.csv -s 0.15 -c 0.6
"""

import sys

from itertools import chain, combinations
from collections import defaultdict
from optparse import OptionParser

import pandas as pd 
from pandas import Series, DataFrame

data = {"name":["yahoo","google","facebook"], "marks":[200,400,800], "price":[9, 3, 7]} 
f1 = DataFrame(data)
print(f1)




def dataFromFile():	
	for i in range(2):
		record = frozenset(f1[2])
		print(record)
		yield record


if __name__ == "__main__":

    optparser = OptionParser()
    optparser.add_option('-s', '--minSupport',
                         dest='minS',
                         help='minimum support value',
                         default=0.15,
                         type='float')
    optparser.add_option('-c', '--minConfidence',
                         dest='minC',
                         help='minimum confidence value',
                         default=0.6,
                         type='float')

    (options, args) = optparser.parse_args()

    inFile = dataFromFile()


    minSupport = options.minS
    minConfidence = options.minC

    print(inFile)
    print(type(inFile))

    #items, rules = runApriori(inFile, minSupport, minConfidence)

    #printResults(items, rules)
