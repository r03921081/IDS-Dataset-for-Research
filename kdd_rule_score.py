import pandas as pd
import numpy as np
from fp_growth import find_frequent_itemsets
import operator
import random

#---------------------------------------------------------------------------------
# Feature Score Correlation ranking value

score_data = open("ranking/value_KDD_attack_cat", "r")
score_map = {}
for line in score_data:
	token = line.split()
	score_map[token[2]] = token[0]
#---------------------------------------------------------------------------------
# Initial Background

minsup = 5000
feature = 5

#attack_table = ["normal", "back", "land", "neptune", "pod", "smurf", "teardrop", "buffer_overflow", "loadmodule", "perl", "rootkit", "ftp_write", "guess_passwd", "imap", "multihop", "phf", "spy", "warezlient", "warezmaster", "ipsweep", "nmap", "satan", "portsweep"]
attack_table = ["normal", "dos", "u2r", "r2l", "probe"]

dos_type = ["back", "land", "neptune", "pod", "smurf", "teardrop"]
u2r_type = ["buffer_overflow", "loadmodule", "perl", "rootkit"]
r2l_type = ["ftp_write", "guess_passwd", "imap", "multihop", "phf", "spy", "warezclient", "warezmaster"]
probe_type = ["ipsweep", "nmap", "satan", "portsweep"]

sNormal = {}
sDos = {}
sU2R = {}
sR2L = {}
sProbe = {}
sAbnormal = {}

attack_score = {"normal": sNormal, "dos": sDos, "u2r": sU2R, "r2l": sR2L, "probe": sProbe, "anomaly": sAbnormal}

fNormal = {}
fDos = {}
fU2R = {}
fR2L = {}
fProbe = {}
fAbnormal = {}

attack_feature = {"normal": fNormal, "dos": fDos, "u2r": fU2R, "r2l": fR2L, "probe": fProbe, "anomaly": fAbnormal}

break_old_raw_train_data = pd.read_csv("nsl_kdd/New_KDD_Train_Discretization_five.csv", delimiter=',', encoding="utf-8-sig")
#print break_old_raw_train_data.columns
old_raw_train_data = break_old_raw_train_data.drop(["Unnamed: 0"], axis=1)
print(old_raw_train_data.shape)
raw_train_data = pd.DataFrame(index = old_raw_train_data.index, columns = old_raw_train_data.columns)
#print(old_raw_train_data.ix[1000])
print(old_raw_train_data.shape)

for feature in old_raw_train_data.columns:
	#print(feature + " " + old_raw_train_data[feature])
	if feature != "class":
		raw_train_data[feature] = feature + " " + old_raw_train_data[feature]
	else: # Class
		raw_train_data[feature] = old_raw_train_data[feature]
#print(raw_train_data.ix[1000])
print(raw_train_data.shape)
#print(old_raw_train_data["class"])
#print(raw_train_data["class"])

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
#train_data = raw_train_data
#train_data = raw_train_data.sample(frac=0.2, replace=True)
#---------------------------------------------------------------------------------
# Compute Frequent pattern

transactions = []

for i in range(5):
	for label in attack_table:
		print(label)
		temp = train_data[train_data["class"]==label]
		data = temp.drop(['class'], axis=1)
		print(data.shape)
		np_data = data.as_matrix()
		transactions = np_data.tolist()
		#print(len(transactions[0]))

		minsup = data.shape[0]
		if minsup < 200:
			minsup = 200
		print minsup
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
			score = score/len(trans_item)
			str_itemset = ','.join(trans_item)
			if score > maxscore:
				maxscore = score
				label_item[str_itemset] = score
		new_itemset = sorted(label_item.items(), key=operator.itemgetter(1), reverse=True)

		max_rule = []

		for rule in new_itemset:
			print rule
			if float(rule[1]) == maxscore:
				print rule
				num = num + 1
				max_rule.append(rule[0])
		print maxscore
		print max_rule
#---------------------------------------------------------------------------------
# Count Feature's numbers

		for token in max_rule:
			for take_feature in token.split(","):
				#print(take_feature)
				if take_feature not in attack_feature[label]:
					attack_feature[label][take_feature] = 0
				else:
					attack_feature[label][take_feature] = int(attack_feature[label][take_feature]) + 1
				if label != "normal":
					if take_feature not in attack_feature["anomaly"]:
						attack_feature["anomaly"][take_feature] = 0
					else:
						attack_feature["anomaly"][take_feature] = int(attack_feature["anomaly"][take_feature]) + 1
		#print(attack_feature[label])
		print("Count " + str(count))

print(attack_feature)

for print_rule in attack_feature:
	print("")
	print(print_rule)
	choose_feature = sorted(attack_feature[print_rule].items(), key=operator.itemgetter(1), reverse=True)
	print(choose_feature)
#---------------------------------------------------------------------------------
# Print Results

print("")
normal_feature = attack_feature["normal"].keys()
abnormal_feature = attack_feature["anomaly"].keys()
print(normal_feature)
print(abnormal_feature)

print("Union")
print(list(set(normal_feature).union(set(abnormal_feature))))

print("Difference")
print("normal")
print(list(set(normal_feature).difference(set(abnormal_feature))))
print("abnormal")
print(list(set(abnormal_feature).difference(set(normal_feature))))

print("And")
print(list((set(normal_feature)&(set(abnormal_feature)))))