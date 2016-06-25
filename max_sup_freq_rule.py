import pandas as pd
import numpy as np
from fp_growth import find_frequent_itemsets
import operator

minsup = 5000
feature = 5

attack_table = ["Normal", "Reconnaissance", "Backdoor", "DoS", "Exploits", "Analysis", "Fuzzers", "Worms", "Shellcode", "Generic"]

raw_train_data = pd.read_csv("unsw/UNSW_Discretize.csv", delimiter=',', encoding="utf-8-sig")
#print(raw_train_data.columns)
print(raw_train_data.shape)

category = {}
for feature in raw_train_data.columns:
	#print(feature)
	for item in raw_train_data[feature].values:
		if item not in category:
			category[item] = feature
#print(category)

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
		str_itemset = ', '.join(trans_item)
		label_item[str_itemset] = sup
		if sup > maxsup:
			maxsup = sup
	new_itemset = sorted(label_item.items(), key=operator.itemgetter(1), reverse=True)
	
	for rule in new_itemset:
		if int(rule[1]) == maxsup:
			num = num + 1
			print(rule)
		elif num < 10:
			num = num + 1
			print(rule)
		#if num < 10:
		#	num = num + 1
		#	print(rule)
		#else:
		#	break

	print("Count " + str(count))
