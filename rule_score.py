import pandas as pd
import numpy as np
from fp_growth import find_frequent_itemsets
import operator
import random

#---------------------------------------------------------------------------------
# Feature Score Correlation ranking value

score_data = open("ranking/value_UNSW_attack_cat", "r")
#score_data = open("ranking/ig_UNSW_attack_cat", "r")
score_map = {}
for line in score_data:
	token = line.split()
	score_map[token[2]] = token[0]
#---------------------------------------------------------------------------------
# Initial Background

minsup = 5000
feature = 5

attack_table = ["Normal", "Reconnaissance", "Backdoor", "DoS", "Exploits", "Analysis", "Fuzzers", "Worms", "Shellcode", "Generic"]

sNormal = {}
sReconnaissance = {}
sBackdoor = {}
sDoS = {}
sExploits = {}
sAnalysis = {}
sFuzzers = {}
sWorms = {}
sShellcode = {}
sGeneric = {}
sAbnormal = {}

attack_score = {"Normal": sNormal, "Reconnaissance": sReconnaissance, "Backdoor": sBackdoor, "DoS": sDoS, "Exploits": sExploits, "Analysis": sAnalysis, "Fuzzers": sFuzzers, "Worms": sWorms, "Shellcode": sShellcode, "Generic": sGeneric, "Abnormal": sAbnormal}

old_raw_train_data = pd.read_csv("unsw/UNSW_Discretize.csv", delimiter=',', encoding="utf-8-sig")
print(old_raw_train_data.shape)
raw_train_data = pd.DataFrame(index = old_raw_train_data.index, columns = old_raw_train_data.columns)
print(old_raw_train_data.ix[1000])

for feature in old_raw_train_data.columns:
	#print(feature + " " + old_raw_train_data[feature])
	if feature != "attack_cat":
		raw_train_data[feature] = feature + " " + old_raw_train_data[feature]
	else:
		raw_train_data[feature] = old_raw_train_data[feature]
print(raw_train_data.ix[1000])
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
train_data = raw_train_data.loc[random.sample(list(raw_train_data.index), sample_num)]
#train_data = raw_train_data.sample(frac=0.2, replace=True)
#---------------------------------------------------------------------------------
# Compute Frequent pattern

transactions = []
#for loop in range(5):
for label in attack_table:
	print(label)
	temp = train_data[train_data["attack_cat"]==label]
	data = temp.drop(['attack_cat'], axis=1)
	print(data.shape)
	np_data = data.as_matrix()
	transactions = np_data.tolist()

	#minsup = data.shape[0]

	#if minsup < 500:
	#	minsup = 500

	if label == "Normal":
		minsup = data.shape[0]
	elif label == "Reconnaissance":
		minsup = data.shape[0]
	elif label == "Backdoor":
		minsup = data.shape[0]
	elif label == "DoS":
		minsup = data.shape[0]
	elif label == "Exploits":
		minsup = data.shape[0]
	elif label == "Analysis":
		minsup = data.shape[0]
	elif label == "Fuzzers":
		minsup = data.shape[0]
	elif label == "Worms":
		minsup = data.shape[0]
	elif label == "Shellcode":
		minsup = data.shape[0]
	elif label == "Generic":
		minsup = data.shape[0]

	label_item = {}
	new_itemset = []
	count = 0
	num = 0
	maxscore = 0.0

	for itemset, sup in find_frequent_itemsets(transactions, minsup, True):
		score = 0.0
		count = count + 1
		trans_item = []
		for token in itemset:
			trans_item.append(category[token])
			score = score + float(score_map[category[token]])
		str_itemset = ','.join(trans_item)
		label_item[str_itemset] = score/len(trans_item)
		if score > maxscore:
			maxscore = score
			maxtrans = []
			maxtrans = str_itemset
	#new_itemset = sorted(label_item.items(), key=operator.itemgetter(1), reverse=True)
	if maxscore == 0.0:
		maxtrans = []
	else:
		attack_score[label][maxtrans] = maxscore
	print maxtrans
	print maxscore
print attack_score
