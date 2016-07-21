import pandas as pd
import numpy as np
from fp_growth import find_frequent_itemsets
import operator
import random

#---------------------------------------------------------------------------------
# Initial Background

minsup = 0
feature = 5

flower_table = ["Iris-setosa", "Iris-versicolor", "Iris-virginica"]

setosa = {}
versicolor = {}
virginica = {}

flower_feature = {"Iris-setosa": setosa, "Iris-versicolor": versicolor, "Iris-virginica": virginica}

old_raw_train_data = pd.read_csv("iris/iris_discretize.csv", delimiter=',', encoding="utf-8-sig")
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
#---------------------------------------------------------------------------------
# Compute Frequent pattern

transactions = []

for label in flower_table:
	print(label)
	temp = train_data[train_data["class"]==label]
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
			if take_feature not in flower_feature[label]:
				flower_feature[label][take_feature] = 1
			else:
				flower_feature[label][take_feature] = int(flower_feature[label][take_feature]) + 1
	print(flower_feature[label])
	print("Count " + str(count))

print(flower_feature)

for print_rule in flower_feature:
	print("")
	print(print_rule)
	choose_feature = sorted(flower_feature[print_rule].items(), key=operator.itemgetter(1), reverse=True)
	print(choose_feature)
#---------------------------------------------------------------------------------
# Print Results

print("")
setosa_feature = flower_feature["Iris-setosa"].keys()
versicolor_feature = flower_feature["Iris-versicolor"].keys()
virginica_feature = flower_feature["Iris-virginica"].keys()

print setosa_feature
print versicolor_feature
print virginica_feature

#print("Union")
#print(list(set(normal_feature).union(set(abnormal_feature))))
