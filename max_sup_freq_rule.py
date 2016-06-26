import pandas as pd
import numpy as np
from fp_growth import find_frequent_itemsets
import operator

minsup = 5000
feature = 5

attack_table = ["Normal", "Reconnaissance", "Backdoor", "DoS", "Exploits", "Analysis", "Fuzzers", "Worms", "Shellcode", "Generic"]

fNormal = {}
fReconnaissance = {}
fBackdoor = {}
fDoS = {}
fExploits = {}
fAnalysis = {}
fFuzzers = {}
fWorms = {}
fShellcode = {}
fGeneric = {}

attack_feature = {"Normal": fNormal, "Reconnaissance": fReconnaissance, "Backdoor": fBackdoor, "DoS": fDoS, "Exploits": fExploits, "Analysis": fAnalysis, "Fuzzers": fFuzzers, "Worms": fWorms, "Shellcode": fShellcode, "Generic": fGeneric}

raw_train_data = pd.read_csv("unsw/UNSW_Discretize.csv", delimiter=',', encoding="utf-8-sig")
#print(raw_train_data.columns)
print(raw_train_data.shape)

category = {}
for feature in raw_train_data.columns:
	#print(feature)
	for item in raw_train_data[feature].values:
		if item not in category:
			category[item] = feature

train_data = raw_train_data.sample(frac=0.1, replace=True)
#print(train_data)
transactions = []

for label in attack_table:
	print(label)
	temp = train_data[train_data["attack_cat"]==label]
	data = temp.drop(['attack_cat'], axis=1)
	print(data.shape)
	np_data = data.as_matrix()
	transactions = np_data.tolist()

	minsup = data.shape[0]
	if minsup < 500:
		minsup = 500
	#print(minsup)
	if label == "Generic":
		minsup = 3000

	label_item = {}
	new_itemset = []
	count = 0
	num = 0
	maxsup = 0

	for itemset, sup in find_frequent_itemsets(transactions, minsup, True):
		count = count + 1
		trans_item = []
		for token in itemset:
			trans_item.append(category[token])
		str_itemset = ','.join(trans_item)
		label_item[str_itemset] = sup
		if sup > maxsup:
			maxsup = sup
	new_itemset = sorted(label_item.items(), key=operator.itemgetter(1), reverse=True)
	
	max_rule = []	

	for rule in new_itemset:
		if int(rule[1]) == maxsup:
			num = num + 1
			max_rule.append(rule[0])
		elif num < 10:
			num = num + 1
			max_rule.append(rule[0])
	for token in max_rule:
		for take_feature in token.split(","):
			#print(take_feature)
			if take_feature not in attack_feature[label]:
				attack_feature[label][take_feature] = 0
			else:
				attack_feature[label][take_feature] = int(attack_feature[label][take_feature]) + 1
	print(attack_feature[label])
	print("Count " + str(count))

print(attack_feature)

for print_rule in attack_feature:
	print("")
	print(print_rule)
	choose_feature = sorted(attack_feature[print_rule].items(), key=operator.itemgetter(1), reverse=True)
	print(choose_feature)

