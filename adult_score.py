import pandas as pd
import numpy as np
from fp_growth import find_frequent_itemsets
import operator
import random

#---------------------------------------------------------------------------------
# Feature Score Correlation ranking value

score_data = open("adult/value_adult", "r")
score_map = {}
for line in score_data:
	token = line.split()
	score_map[token[2]] = token[0]
#---------------------------------------------------------------------------------
# Initial Background

minsup = 0
feature = 5

money_table = ["<=50K", ">50K"]

small = {}
big = {}

money_feature = {"<=50K": small, ">50K": big}

old_raw_train_data = pd.read_csv("adult/training_discretize.csv", delimiter=',', encoding="utf-8-sig")
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

sample_num = int(raw_train_data.shape[0] * 0.1)
print sample_num
train_data = raw_train_data.loc[random.sample(list(raw_train_data.index), sample_num)]
#train_data = raw_train_data.sample(frac=0.2, replace=True)
#print train_data
#---------------------------------------------------------------------------------
# Compute Frequent pattern

transactions = []

#print train_data["class"]

for label in money_table:
	print(label)
	temp = train_data[train_data["class"]==label]
	#print temp
	data = temp.drop(['class'], axis=1)
	print(data.shape)
	np_data = data.as_matrix()
	transactions = np_data.tolist()

	#minsup = data.shape[0]*0.6
	minsup = 500

	label_item = {}
	new_itemset = []
	count = 0
	num = 0
	maxscore = 0

	for itemset, sup in find_frequent_itemsets(transactions, minsup, True):
		score = 0.0
		count = count + 1
		trans_item = []
		for token in itemset:
			trans_item.append(category[token])
			score = score + float(score_map[category[token]])
		score = score/len(trans_item)
		str_itemset = ','.join(trans_item)
		label_item[str_itemset] = score
		if score > maxscore:
			maxscore = score
	new_itemset = sorted(label_item.items(), key=operator.itemgetter(1), reverse=True)
	print new_itemset
	max_rule = []

	for rule in new_itemset:
		if float(rule[1]) == maxscore:
			print rule
			num = num + 1
			max_rule.append(rule[0])
#---------------------------------------------------------------------------------
# Count Feature's numbers

	for token in max_rule:
		for take_feature in token.split(","):
			#print(take_feature)
			if take_feature not in money_feature[label]:
				money_feature[label][take_feature] = 1
			else:
				money_feature[label][take_feature] = int(money_feature[label][take_feature]) + 1
	print(money_feature[label])
	print("Count " + str(count))

print(money_feature)

for print_rule in money_feature:
	print("")
	print(print_rule)
	choose_feature = sorted(money_feature[print_rule].items(), key=operator.itemgetter(1), reverse=True)
	print(choose_feature)
#---------------------------------------------------------------------------------
# Print Results

print("")
small_feature = money_feature["<=50K"].keys()
big_feature = money_feature[">50K"].keys()

print small_feature
print big_feature

print("")

print("Union")
print(list(set(small_feature).union(set(big_feature))))
print("")
print("Difference")
print("small_feature")
print(list(set(small_feature).difference(set(big_feature))))
print("")
print("big_feature")
print(list(set(big_feature).difference(set(small_feature))))
print("")
print("And")
print(list((set(small_feature)&(set(big_feature)))))

