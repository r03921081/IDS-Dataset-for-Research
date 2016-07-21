import pandas as pd
import numpy as np
from fp_growth import find_frequent_itemsets
import operator
import random
#---------------------------------------------------------------------------------
# Initial Background

minsup = 0
feature = 5

wine_table = ["1", "2", "3"]

one = {}
two = {}
three = {}

wine_feature = {"1": one, "2": two, "3": three}

old_raw_train_data = pd.read_csv("wine/wine_discretize.csv", delimiter=',', encoding="utf-8-sig")
print(old_raw_train_data.shape)
raw_train_data = pd.DataFrame(index = old_raw_train_data.index, columns = old_raw_train_data.columns)
#print(old_raw_train_data.ix[1000])

for feature in old_raw_train_data.columns:
	#print(feature + " " + old_raw_train_data[feature])
	if feature != "class":
		raw_train_data[feature] = feature + " " + old_raw_train_data[feature]
	else:
		raw_train_data[feature] = old_raw_train_data[feature]
#print(raw_train_data.ix[1000])
#print raw_train_data
#---------------------------------------------------------------------------------
# Discretize value map to category feature name

category = {}
for feature in raw_train_data.columns:
	#print(feature)
	for item in raw_train_data[feature].values:
		if item not in category:
			category[item] = feature
#---------------------------------------------------------------------------------
# Sampling

sample_num = int(raw_train_data.shape[0] * 0.3)
print sample_num
train_data = raw_train_data.loc[random.sample(list(raw_train_data.index), sample_num)]
#train_data = raw_train_data.sample(frac=0.2, replace=True)
#print train_data
#---------------------------------------------------------------------------------
# Compute Frequent pattern

transactions = []

#print train_data["class"]

for label in wine_table:
	print(label)
	temp = train_data[train_data["class"]==int(label)]
	#print temp
	data = temp.drop(['class'], axis=1)
	print(data.shape)
	np_data = data.as_matrix()
	transactions = np_data.tolist()

	#minsup = data.shape[0]
	minsup = 10

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
			print rule
			num = num + 1
			max_rule.append(rule[0])
		elif num < 10:
			print rule
			num = num + 1
			max_rule.append(rule[0])
#---------------------------------------------------------------------------------
# Count Feature's numbers

	for token in max_rule:
		for take_feature in token.split(","):
			#print(take_feature)
			if take_feature not in wine_feature[label]:
				wine_feature[label][take_feature] = 1
			else:
				wine_feature[label][take_feature] = int(wine_feature[label][take_feature]) + 1
	print(wine_feature[label])
	print("Count " + str(count))

print(wine_feature)

for print_rule in wine_feature:
	print("")
	print(print_rule)
	choose_feature = sorted(wine_feature[print_rule].items(), key=operator.itemgetter(1), reverse=True)
	print(choose_feature)
#---------------------------------------------------------------------------------
# Print Results

print("")
one_feature = wine_feature["1"].keys()
two_feature = wine_feature["2"].keys()
three_feature = wine_feature["3"].keys()

print one_feature
print two_feature
print three_feature


