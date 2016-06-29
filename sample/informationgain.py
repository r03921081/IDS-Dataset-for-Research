import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction import DictVectorizer as dv
from sklearn.cross_validation import train_test_split
from sklearn import linear_model

feature = ["service", "ct_state_ttl", "dttl"]#, "state", "sttl"] # proto

proto_table = {"udp": 1, "arp": 2, "tcp": 3, "igmp": 4, "ospf": 5, "sctp": 6, "gre": 7, "ggp": 8, "ip": 9, "ipnip": 10, "st2": 11, "argus": 12, "chaos": 13, "egp": 14, "emcon": 15, "nvp": 16, "pup": 17, "xnet": 18, "mux": 19, "dcn": 20, "hmp": 21, "prm": 22, "trunk-1": 23, "trunk-2": 24, "xns-idp": 25, "leaf-1": 26, "leaf-2": 27, "irtp": 28, "rdp": 29, "netblt": 30, "mfe-nsp": 31, "merit-inp": 32, "3pc": 33, "idpr": 34, "ddp": 35, "idpr-cmtp": 36, "tp++": 37, "ipv6": 38, "sdrp": 39, "ipv6-frag": 40, "ipv6-route": 41, "idrp": 42, "mhrp": 43, "i-nlsp": 44, "rvd": 45, "mobile": 46, "narp": 47, "skip": 48, "tlsp": 49, "ipv6-no": 50, "any": 51, "ipv6-opts": 52, "cftp": 53, "sat-expak": 54, "ippc": 55, "kryptolan": 56, "sat-mon": 57, "cpnx": 58, "wsn": 59, "pvp": 60, "br-sat-mon": 61, "sun-nd": 62, "wb-mon": 63, "vmtp": 64, "ttp": 65, "vines": 66, "nsfnet-igp": 67, "dgp": 68, "eigrp": 69, "tcf": 70, "sprite-rpc": 71, "larp": 72, "mtp": 73, "ax.25": 74, "ipip": 75, "aes-sp3-d": 76, "micp": 77, "encap": 78, "pri-enc": 79, "gmtp": 80, "ifmp": 81, "pnni": 82, "qnx": 83, "scps": 84, "cbt": 85, "bbn-rcc": 86, "igp": 87, "bna": 88, "swipe": 89, "visa": 90, "ipcv": 91, "cphb": 92, "iso-tp4": 93, "wb-expak": 94, "sep": 95, "secure-vmtp": 96, "xtp": 97, "il": 98, "rsvp": 99, "unas": 100, "fc": 101, "iso-ip": 102, "etherip": 103, "pim": 104, "aris": 105, "a/n": 106, "ipcomp": 107, "snp": 108, "compaq-peer": 109, "ipx-n-ip": 110, "pgm": 111, "vrrp": 112, "l2tp": 113, "zero": 114, "ddx": 115, "iatp": 116, "stp": 117, "srp": 118, "uti": 119, "sm": 120, "smp": 121, "isis": 122, "ptp": 123, "fire": 124, "crtp": 125, "crudp": 126, "sccopmce": 127, "iplt": 128, "pipe": 129, "sps": 130, "ib": 131}
service_table = {"-": 1, "http": 2, "ftp": 3, "ftp-data": 4, "smtp": 5, "pop3": 6, "dns": 7, "snmp": 8, "ssl": 9, "dhcp": 10, "irc": 11, "radius": 12, "ssh": 13}
state_table = {"INT": 1, "FIN": 2, "REQ": 3, "ACC": 4, "CON": 5, "RST": 6, "CLO": 7}

raw_train_data = pd.read_csv("../unsw/UNSW_NB15_training-set.csv", delimiter=',', encoding="utf-8-sig")
#print(raw_train_data.shape)
category_data = pd.DataFrame(index = raw_train_data.index, columns = ["proto", "service", "state"])
#print(category_data.shape)
train_data = pd.DataFrame(index = raw_train_data.index, columns = feature)

for i in range(82332):
	if raw_train_data["proto"][i] in proto_table:
		category_data["proto"][i] = proto_table[raw_train_data["proto"][i]]
	else:
		category_data["proto"][i] = 0
	if raw_train_data["service"][i] in service_table:
		category_data["service"][i] = service_table[raw_train_data["service"][i]]
	else:
		category_data["service"][i] = 0
	if raw_train_data["state"][i] in state_table:
		category_data["state"][i] = state_table[raw_train_data["state"][i]]
	else:
		category_data["state"][i] = 0

for item in feature:
	if item == "proto" or item == "state" or item == "service":
		train_data[item] = category_data[item]
	else:
		train_data[item] = raw_train_data[item]

train_target = raw_train_data['label']

data = train_data.as_matrix()
target = train_target.as_matrix()

np_train_data, np_test_data, np_train_target, np_test_target = train_test_split(data, target, test_size = 0.33)


# LogisticRegression
model = linear_model.SGDClassifier()
model.fit(np_train_data, np_train_target)
print(model)

expected = np_test_target
predicted = model.predict(np_test_data)

print("LogisticRegression")
print(metrics.classification_report(expected, predicted))
print(metrics.confusion_matrix(expected, predicted))

# NaiveBayes
model = GaussianNB()
model.fit(np_train_data, np_train_target)
print(model)

expected = np_test_target
predicted = model.predict(np_test_data)

print("NaiveBayes GaussianNB")
print(metrics.classification_report(expected, predicted))
print(metrics.confusion_matrix(expected, predicted))

# DecisionTree
model = DecisionTreeClassifier()
model.fit(np_train_data, np_train_target)
print(model)

expected = np_test_target
predicted = model.predict(np_test_data)

print("DecisionTree")
print(metrics.classification_report(expected, predicted))
print(metrics.confusion_matrix(expected, predicted))
