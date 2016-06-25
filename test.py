import sys

from itertools import chain, combinations
from collections import defaultdict
from optparse import OptionParser

import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction import DictVectorizer as dv
from sklearn.cross_validation import train_test_split
from sklearn import linear_model

proto_table = {"udp": 1, "arp": 2, "tcp": 3, "igmp": 4, "ospf": 5, "sctp": 6, "gre": 7, "ggp": 8, "ip": 9, "ipnip": 10, "st2": 11, "argus": 12, "chaos": 13, "egp": 14, "emcon": 15, "nvp": 16, "pup": 17, "xnet": 18, "mux": 19, "dcn": 20, "hmp": 21, "prm": 22, "trunk-1": 23, "trunk-2": 24, "xns-idp": 25, "leaf-1": 26, "leaf-2": 27, "irtp": 28, "rdp": 29, "netblt": 30, "mfe-nsp": 31, "merit-inp": 32, "3pc": 33, "idpr": 34, "ddp": 35, "idpr-cmtp": 36, "tp++": 37, "ipv6": 38, "sdrp": 39, "ipv6-frag": 40, "ipv6-route": 41, "idrp": 42, "mhrp": 43, "i-nlsp": 44, "rvd": 45, "mobile": 46, "narp": 47, "skip": 48, "tlsp": 49, "ipv6-no": 50, "any": 51, "ipv6-opts": 52, "cftp": 53, "sat-expak": 54, "ippc": 55, "kryptolan": 56, "sat-mon": 57, "cpnx": 58, "wsn": 59, "pvp": 60, "br-sat-mon": 61, "sun-nd": 62, "wb-mon": 63, "vmtp": 64, "ttp": 65, "vines": 66, "nsfnet-igp": 67, "dgp": 68, "eigrp": 69, "tcf": 70, "sprite-rpc": 71, "larp": 72, "mtp": 73, "ax.25": 74, "ipip": 75, "aes-sp3-d": 76, "micp": 77, "encap": 78, "pri-enc": 79, "gmtp": 80, "ifmp": 81, "pnni": 82, "qnx": 83, "scps": 84, "cbt": 85, "bbn-rcc": 86, "igp": 87, "bna": 88, "swipe": 89, "visa": 90, "ipcv": 91, "cphb": 92, "iso-tp4": 93, "wb-expak": 94, "sep": 95, "secure-vmtp": 96, "xtp": 97, "il": 98, "rsvp": 99, "unas": 100, "fc": 101, "iso-ip": 102, "etherip": 103, "pim": 104, "aris": 105, "a/n": 106, "ipcomp": 107, "snp": 108, "compaq-peer": 109, "ipx-n-ip": 110, "pgm": 111, "vrrp": 112, "l2tp": 113, "zero": 114, "ddx": 115, "iatp": 116, "stp": 117, "srp": 118, "uti": 119, "sm": 120, "smp": 121, "isis": 122, "ptp": 123, "fire": 124, "crtp": 125, "crudp": 126, "sccopmce": 127, "iplt": 128, "pipe": 129, "sps": 130, "ib": 131}
service_table = {"-": 1, "http": 2, "ftp": 3, "ftp-data": 4, "smtp": 5, "pop3": 6, "dns": 7, "snmp": 8, "ssl": 9, "dhcp": 10, "irc": 11, "radius": 12, "ssh": 13}
state_table = {"INT": 1, "FIN": 2, "REQ": 3, "ACC": 4, "CON": 5, "RST": 6, "CLO": 7}


# TRAINING DATA
raw_train_data = pd.read_csv("unsw/UNSW_Discretize.csv", delimiter=',', encoding="utf-8-sig")
print(raw_train_data.columns)
print(raw_train_data.shape)

train_data = raw_train_data.drop(['attack_cat'], axis=1)
train_target = raw_train_data['attack_cat']

def subsets(arr):
    """ Returns non empty subsets of arr"""
    return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])


def returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet):
    """calculates the support for items in the itemSet and returns a subset of the itemSet each of whose elements satisfies the minimum support"""
    _itemSet = set()
    localSet = defaultdict(int)

    for item in itemSet:
        for transaction in transactionList:
            if item.issubset(transaction):
                freqSet[item] += 1
                localSet[item] += 1

    for item, count in localSet.items():
        support = float(count)/len(transactionList)

        if support >= minSupport:
            _itemSet.add(item)

    return _itemSet


def joinSet(itemSet, length):
    """Join a set with itself and returns the n-element itemsets"""
    return set([i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length])


def getItemSetTransactionList(data_iterator):
    transactionList = list()
    itemSet = set()
    for record in data_iterator:
        transaction = frozenset(record)
        transactionList.append(transaction)
        for item in transaction:
            itemSet.add(frozenset([item]))
    return itemSet, transactionList


def runApriori(data_iter, minSupport, minConfidence):
    itemSet, transactionList = getItemSetTransactionList(data_iter)

    freqSet = defaultdict(int)
    largeSet = dict()
    assocRules = dict()

    oneCSet = returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet)

    currentLSet = oneCSet
    k = 2
    while(currentLSet != set([])):
        largeSet[k-1] = currentLSet
        currentLSet = joinSet(currentLSet, k)
        currentCSet = returnItemsWithMinSupport(currentLSet, transactionList, minSupport, freqSet)
        currentLSet = currentCSet
        k = k + 1

    def getSupport(item):
        """local function which Returns the support of an item"""
        return float(freqSet[item])/len(transactionList)

    toRetItems = []
    for key, value in largeSet.items():
        toRetItems.extend([(tuple(item), getSupport(item)) for item in value])

    toRetRules = []
    for key, value in largeSet.items()[1:]:
        for item in value:
            _subsets = map(frozenset, [x for x in subsets(item)])
            for element in _subsets:
                remain = item.difference(element)
                if len(remain) > 0:
                    confidence = getSupport(item)/getSupport(element)
                    if confidence >= minConfidence:
                        toRetRules.append(((tuple(element), tuple(remain)), confidence))
    return toRetItems, toRetRules


def printResults(items, rules):
    """prints the generated itemsets sorted by support and the confidence rules sorted by confidence"""
    for item, support in sorted(items, key=lambda (item, support): support):
        print "item: %s , %.3f" % (str(item), support)
    print "\n------------------------ RULES:"
    for rule, confidence in sorted(rules, key=lambda (rule, confidence): confidence):
        pre, post = rule
        print "Rule: %s ==> %s , %.3f" % (str(pre), str(post), confidence)


def dataFromFile():
    """Function which reads from the file and yields a generator"""
    for i in range(0, 82332):
        print(train_data.values[i])
        record = frozenset(train_data.values[i])
        yield record


if __name__ == "__main__":

    optparser = OptionParser()
    optparser.add_option('-s', '--minSupport', dest='minS', help='minimum support value', default=0.15, type='float')
    optparser.add_option('-c', '--minConfidence', dest='minC', help='minimum confidence value', default=0.6, type='float')
    
    (options, args) = optparser.parse_args()

    inFile = None
    inFile = dataFromFile()

    minSupport = options.minS
    minConfidence = options.minC

    items, rules = runApriori(inFile, minSupport, minConfidence)

    printResults(items, rules)
