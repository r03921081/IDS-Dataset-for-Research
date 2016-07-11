import pandas as pd
import numpy as np
from fp_growth import find_frequent_itemsets
import operator
import random
from sklearn import metrics
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction import DictVectorizer as dv
from sklearn.cross_validation import train_test_split
from sklearn import linear_model

minsup = 5000
feature = 5

attack_table = ["normal", "back", "land", "neptune", "pod", "smurf", "teardrop", "buffer_overflow", "loadmodule", "perl", "rootkit", "ftp_write", "guess_passwd", "imap", "multihop", "phf", "spy", "warezlient", "warezmaster", "ipsweep", "nmap", "satan", "portsweep"]

fNormal = {}
fDos = {}
fU2R = {}
fR2L = {}
fProbe = {}
fAbnormal = {}

dos_type = ["back", "land", "neptune", "pod", "smurf", "teardrop"]
u2r_type = ["buffer_overflow", "loadmodule", "perl", "rootkit"]
r2l_type = ["ftp_write", "guess_passwd", "imap", "multihop", "phf", "spy", "warezlient", "warezmaster"]
probe_type = ["ipsweep", "nmap", "satan", "portsweep"]

attack_feature = {"normal": fNormal, "dos": fDos, "u2r": fU2R, "r2l": fR2L, "probe": fProbe, "anomaly": fAbnormal}

raw_train_data = pd.read_csv("nsl_kdd/New_KDD_Train_Discretization.csv", delimiter=',', encoding="utf-8-sig")

#raw_train_data = raw_data.drop(["ct_dst_sport_ltm"], axis=1)

#print(raw_train_data.columns)
print(raw_train_data.shape)

category = {}
for feature in raw_train_data.columns:
	#print(feature)
	for item in raw_train_data[feature].values:
		if item not in category:
			category[item] = feature

#sample_num = int(raw_train_data.shape[0] * 0.8)
#train_data = raw_train_data.loc[random.sample(list(raw_train_data.index), sample_num)]

msk = np.random.rand(len(raw_train_data)) < 0.8
train_data = raw_train_data[msk]
test_data = raw_train_data[~msk]

#train_data = raw_train_data.sample(frac=0.2, replace=True)
transactions = []

for label in attack_table:
	print(label)
	temp = train_data[train_data["class"]==label]
	data = temp.drop(['class'], axis=1)
	print(data.shape)
	np_data = data.as_matrix()
	transactions = np_data.tolist()

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
			#print(rule[0])
			num = num + 1
			max_rule.append(rule[0])
		elif num < 10:
			#print(rule[0])
			num = num + 1
			max_rule.append(rule[0])
	for token in max_rule:
		for take_feature in token.split(","):
			#print(take_feature)
			if take_feature not in attack_feature[Attack_label]:
				attack_feature[Attack_label][take_feature] = 0
			else:
				attack_feature[Attack_label][take_feature] = int(attack_feature[Attack_label][take_feature]) + 1
			if label != "normal":
				if take_feature not in attack_feature["anomaly"]:
					attack_feature["anomaly"][take_feature] = 0
				else:
					attack_feature["anomaly"][take_feature] = int(attack_feature["anomaly"][take_feature]) + 1
	#print(attack_feature[Attack_label])
	print("Count " + str(count))

print(attack_feature)

for print_rule in attack_feature:
	print("")
	print(print_rule)
	choose_feature = sorted(attack_feature[print_rule].items(), key=operator.itemgetter(1), reverse=True)
	print(choose_feature)

print("")
normal_feature = attack_feature["normal"].keys()
abnormal_feature = attack_feature["anomaly"].keys()
#print(normal_feature)
#print(abnormal_feature)

#print("Union")
#print(list(set(normal_feature).union(set(abnormal_feature))))

print("Difference")
print("normal")
print(list(set(normal_feature).difference(set(abnormal_feature))))
print("abnormal")
print(list(set(abnormal_feature).difference(set(normal_feature))))

#print("And")
#print(list((set(normal_feature)&(set(abnormal_feature)))))

normal_feature = ["protocol_type"]


#-----------------------------------------------------------------------------
feature = ["num_access_files", "num_file_creations", "service", "num_compromised", "flag", "hot", "num_root", "duration", "num_failed_logins", "protocol_type"]
#feature = list(set(abnormal_feature).difference(set(normal_feature)))

proto_table = {"tcp": 1, "udp": 2, "icmp": 3}
service_table = {"ftp_data": 70, "other": 1, "private": 2, "http": 3, "remote_job": 4, "name": 5, "netbios_ns": 6, "eco_i": 7, "mtp": 8, "telnet": 9, "finger": 10, "domain_u": 11, "supdup": 12, "uucp_path": 13, "Z39_50": 14, "smtp": 15, "csnet_ns": 16, "uucp": 17, "netbios_dgm": 18, "urp_i": 19, "auth": 20, "domain": 21, "ftp": 22, "bgp": 23, "ldap": 24, "ecr_i": 25, "gopher": 26, "vmnet": 27, "systat": 28, "http_443": 29, "efs": 30, "whois": 31, "imap4": 32, "iso_tsap": 33, "echo": 34, "klogin": 35, "link": 36, "sunrpc": 37, "login": 38, "kshell": 39, "sql_net": 40, "time": 41, "hostnames": 42, "exec": 43, "ntp_u": 44, "discard": 45, "nntp": 46, "courier": 47, "ctf": 48, "ssh": 49, "daytime": 50, "shell": 51, "netstat": 52, "pop_3": 53, "nnsp": 54, "IRC": 55, "pop_2": 56, "printer": 57, "tim_i": 58, "pm_dump": 59, "red_i": 60, "netbios_ssn": 61, "rje": 62, "X11": 63, "urh_i": 64, "http_8001": 65, "aoi": 66, "http_2784": 67, "tffp_u": 68, "harvest": 69}
flag_table = {"SF": 11, "S0": 1, "REJ": 2, "RSTR": 3, "SH": 4, "RSTO": 5, "S1": 6, "RSTOS0": 7, "S3": 8, "S2": 9, "OTH": 10}

cat_train = pd.DataFrame(index = train_data.index, columns = ["protocol_type", "service", "flag"])
cat_test = pd.DataFrame(index = test_data.index, columns = ["protocol_type", "service", "flag"])

real_train = pd.DataFrame(index = train_data.index, columns = feature)
real_test = pd.DataFrame(index = test_data.index, columns = feature)

for i in train_data.index:
	if train_data["protocol_type"][i] in proto_table:
		cat_train["protocol_type"][i] = proto_table[train_data["protocol_type"][i]]
	else:
		cat_train["protocol_type"][i] = 0
	if train_data["service"][i] in service_table:
		cat_train["service"][i] = service_table[train_data["service"][i]]
	else:
		cat_train["service"][i] = 0
	if train_data["flag"][i] in flag_table:
		cat_train["flag"][i] = flag_table[train_data["flag"][i]]
	else:
		cat_train["flag"][i] = 0

for i in test_data.index:
	if test_data["protocol_type"][i] in proto_table:
		cat_test["protocol_type"][i] = proto_table[test_data["protocol_type"][i]]
	else:
		cat_test["protocol_type"][i] = 0
	if test_data["service"][i] in service_table:
		cat_test["service"][i] = service_table[test_data["service"][i]]
	else:
		cat_test["service"][i] = 0
	if test_data["flag"][i] in flag_table:
		cat_test["flag"][i] = flag_table[test_data["flag"][i]]
	else:
		cat_test["flag"][i] = 0

for item in feature:
	if item == "protocol_type":
		real_train[item] = cat_train[item]
		real_test[item] = cat_test[item]
	elif item == "service":
		real_train[item] = cat_train[item]
		real_test[item] = cat_test[item]
	elif item == "flag":
		real_train[item] = cat_train[item]
		real_test[item] = cat_test[item]
	else:
		real_train[item] = train_data[item]
		real_test[item] = test_data[item]

train_target = train_data['class']
test_target = test_data['class']

feature_train_data = real_train.as_matrix()
feature_train_target = train_target.as_matrix()

feature_test_data = real_test.as_matrix()
feature_test_target = test_target.as_matrix()

# NaiveBayes
model = GaussianNB()
model.fit(feature_train_data, feature_train_target)
print(model)

expected = feature_test_target
predicted = model.predict(feature_test_data)
print(expected)
print(predicted)
print("NaiveBayes GaussianNB")
print(metrics.classification_report(expected, predicted))
print(metrics.confusion_matrix(expected, predicted))


#-----------------------------------------------------------------------------
true_positive = 0
false_positive = 0
true_negative = 0
false_negative = 0
for i in range(len(expected)):
	if expected[i] == "normal" and predicted[i] == "normal":
		true_positive = true_positive + 1
	elif expected[i] == "anomaly" and predicted[i] == "normal":
		false_positive = false_positive + 1
	elif expected[i] == "anomaly" and predicted[i] == "anomaly":
		true_negative = true_negative + 1
	else: # if expected[i] == 0 && predicted[i] == 1
		false_negative = false_negative + 1

print("")
print("Truth Table")
print(str(true_positive) + "\t" + str(false_positive))
print(str(false_negative) + "\t" + str(true_negative))
print("")

prediction_mother = true_positive + false_positive
#print(prediction_mother)
#print(true_positive)
prediction = float(true_positive) / float(prediction_mother)
print prediction

recall = float(true_positive) / (true_positive + false_negative)
print recall

predict_normal = 0
predict_abnormal = 0

for i in range(len(predicted)):
	if predicted[i] == "normal":
		predict_normal = predict_normal + 1
	else:
		predict_abnormal = predict_abnormal + 1
print("")
print(predict_normal)
print(predict_abnormal)


