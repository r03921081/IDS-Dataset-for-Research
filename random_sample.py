import pandas as pd
import numpy as np
from fp_growth import find_frequent_itemsets

minsup = 37000
feature = 5

attack_table = ["Normal", "Reconnaissance", "Backdoor", "DoS", "Exploits", "Analysis", "Fuzzers", "Worms", "Shellcode", "Generic"]

raw_train_data = pd.read_csv("unsw/UNSW_Discretize.csv", delimiter=',', encoding="utf-8-sig")
#print(raw_train_data.columns)
print(raw_train_data.shape)

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

	#count = 0
	#for itemset in find_frequent_itemsets(transactions, minsup):
	#	if len(itemset) == feature:
	#		count = count + 1
	#		#print itemset
	#print count


