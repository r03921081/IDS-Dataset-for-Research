import pandas as pd
import numpy as np
from fp_growth import find_frequent_itemsets
import operator
import random

#---------------------------------------------------------------------------------
# Feature Score Correlation ranking value

#score_data = open("ranking/value_UNSW_attack_cat", "r")
score_data = open("ranking/value_KDD_attack_cat", "r")
score_map = {}
for line in score_data:
	token = line.split()
	score_map[token[2]] = token[0]
#---------------------------------------------------------------------------------
# Initial Background

minsup = 5000
feature = 5

attack_table = ["normal", "back", "land", "neptune", "pod", "smurf", "teardrop", "buffer_overflow", "loadmodule", "perl", "rootkit", "ftp_write", "guess_passwd", "imap", "multihop", "phf", "spy", "warezlient", "warezmaster", "ipsweep", "nmap", "satan", "portsweep"]

sNormal = {}
sDos = {}
sU2R = {}
sR2L = {}
sProbe = {}
sAbnormal = {}

dos_type = ["back", "land", "neptune", "pod", "smurf", "teardrop"]
u2r_type = ["buffer_overflow", "loadmodule", "perl", "rootkit"]
r2l_type = ["ftp_write", "guess_passwd", "imap", "multihop", "phf", "spy", "warezlient", "warezmaster"]
probe_type = ["ipsweep", "nmap", "satan", "portsweep"]

attack_score = {"normal": sNormal, "dos": sDos, "u2r": sU2R, "r2l": sR2L, "probe": sProbe, "anomaly": sAbnormal}

old_raw_train_data = pd.read_csv("nsl_kdd/New_KDD_Train_Discretization.csv", delimiter=',', encoding="utf-8-sig")
print(old_raw_train_data.shape)
raw_train_data = pd.DataFrame(index = old_raw_train_data.index, columns = old_raw_train_data.columns)
print(old_raw_train_data.ix[1000])

for feature in old_raw_train_data.columns:
	#print(feature + " " + old_raw_train_data[feature])
	if feature != "class":
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

#sample_num = int(raw_train_data.shape[0] * 0.3)
#train_data = raw_train_data.loc[random.sample(list(raw_train_data.index), sample_num)]
train_data = raw_train_data
#train_data = raw_train_data.sample(frac=0.2, replace=True)
#---------------------------------------------------------------------------------
# Compute Frequent pattern

transactions = []
for label in attack_table:
	print(label)
	temp = train_data[train_data["class"]==label]
	data = temp.drop(['class'], axis=1)
	print(data.shape)
	np_data = data.as_matrix()
	transactions = np_data.tolist()
	#print(len(transactions[0]))

	if label in dos_type:
		Attack_label = "dos"
	elif label in u2r_type:
		Attack_label = "u2r"
	elif label in r2l_type:
		Attack_label = "r2l"
	elif label in probe_type:
		Attack_label = "probe"
	else:
		Attack_label = "normal"

	print Attack_label

	minsup = data.shape[0]
	if minsup < 200:
		minsup = 200
	#minsup = int(minsup * 9 / 10)	

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
		attack_score[Attack_label][maxtrans] = maxscore
	print maxtrans
	print maxscore
print attack_score
