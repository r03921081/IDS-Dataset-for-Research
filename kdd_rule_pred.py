import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction import DictVectorizer as dv
from sklearn.cross_validation import train_test_split
from sklearn import linear_model

# Anomaly Feature
feature = ["num_shells", "num_access_files", "num_file_creations", "is_guest_login", "root_shell", "hot", "su_attempted", "duration", "num_failed_logins"]

# Union Feature
feature = ["num_shells", "num_access_files", "src_bytes", "num_compromised", "urgent", "su_attempted", "duration", "num_file_creations", "is_host_login", "land", "wrong_fragment", "root_shell", "num_failed_logins", "num_outbound_cmds", "is_guest_login", "hot", "num_root", "dst_bytes"]

proto_table = {"tcp": 0, "udp": 1, "icmp": 2}
service_table = {"ftp_data": 0, "other": 1, "private": 2, "http": 3, "remote_job": 4, "name": 5, "netbios_ns": 6, "eco_i": 7, "mtp": 8, "telnet": 9, "finger": 10, "domain_u": 11, "supdup": 12, "uucp_path": 13, "Z39_50": 14, "smtp": 15, "csnet_ns": 16, "uucp": 17, "netbios_dgm": 18, "urp_i": 19, "auth": 20, "domain": 21, "ftp": 22, "bgp": 23, "ldap": 24, "ecr_i": 25, "gopher": 26, "vmnet": 27, "systat": 28, "http_443": 29, "efs": 30, "whois": 31, "imap4": 32, "iso_tsap": 33, "echo": 34, "klogin": 35, "link": 36, "sunrpc": 37, "login": 38, "kshell": 39, "sql_net": 40, "time": 41, "hostnames": 42, "exec": 43, "ntp_u": 44, "discard": 45, "nntp": 46, "courier": 47, "ctf": 48, "ssh": 49, "daytime": 50, "shell": 51, "netstat": 52, "pop_3": 53, "nnsp": 54, "IRC": 55, "pop_2": 56, "printer": 57, "tim_i": 58, "pm_dump": 59, "red_i": 60, "netbios_ssn": 61, "rje": 62, "X11": 63, "urh_i": 64, "http_8001": 65, "aoi": 66, "http_2784": 67, "tffp_u": 68, "harvest": 69}
flag_table = {"SF": 0, "S0": 1, "REJ": 2, "RSTR": 3, "SH": 4, "RSTO": 5, "S1": 6, "RSTOS0": 7, "S3": 8, "S2": 9, "OTH": 10}

raw_train_data = pd.read_csv("nsl_kdd/KDD_Train.csv", delimiter=',', encoding="utf-8-sig")
raw_test_data = pd.read_csv("nsl_kdd/KDD_Test.csv", delimiter=',', encoding="utf-8-sig")

cat_train = pd.DataFrame(index = raw_train_data.index, columns = ["protocol_type", "service", "flag"])
cat_test = pd.DataFrame(index = raw_test_data.index, columns = ["protocol_type", "service", "flag"])

train_data = pd.DataFrame(index = raw_train_data.index, columns = feature)
test_data = pd.DataFrame(index = raw_test_data.index, columns = feature)

for i in range(raw_train_data.shape[0]):
	if raw_train_data["protocol_type"][i] in proto_table:
		cat_train["protocol_type"][i] = proto_table[raw_train_data["protocol_type"][i]]
	else:
		cat_train["protocol_type"][i] = 0
	if raw_train_data["service"][i] in service_table:
		cat_train["service"][i] = service_table[raw_train_data["service"][i]]
	else:
		cat_train["service"][i] = 0
	if raw_train_data["flag"][i] in flag_table:
		cat_train["flag"][i] = flag_table[raw_train_data["flag"][i]]
	else:
		cat_train["flag"][i] = 0

for i in range(raw_test_data.shape[0]):
	if raw_test_data["protocol_type"][i] in proto_table:
		cat_test["protocol_type"][i] = proto_table[raw_test_data["protocol_type"][i]]
	else:
		cat_test["protocol_type"][i] = 0
	if raw_test_data["service"][i] in service_table:
		cat_test["service"][i] = service_table[raw_test_data["service"][i]]
	else:
		cat_test["service"][i] = 0
	if raw_test_data["flag"][i] in flag_table:
		cat_test["flag"][i] = flag_table[raw_test_data["flag"][i]]
	else:
		cat_test["flag"][i] = 0

for item in feature:
	if item == "protocol_type":
		train_data[item] = cat_train[item]
		test_data[item] = cat_test[item]
	elif item == "service":
		train_data[item] = cat_train[item]
		test_data[item] = cat_test[item]
	elif item == "flag":
		train_data[item] = cat_train[item]
		test_data[item] = cat_test[item]
	else:
		train_data[item] = raw_train_data[item]
		test_data[item] = raw_test_data[item]

train_target = raw_train_data['class']
test_target = raw_test_data['class']

feature_train_data = train_data.as_matrix()
feature_train_target = train_target.as_matrix()

feature_test_data = test_data.as_matrix()
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
#-----------------------------------------------------------------------------

second_index = []
for i in range(len(predicted)):
	if predicted[i] == "normal": # Into next term
		second_index.append(i+1)
second_index_num = len(second_index)

second_data = raw_test_data.ix[second_index]

print len(second_index)
print second_data.shape

#second_data.to_csv("unsw/second_turn.csv", sep=',', encoding='utf-8-sig')

#-----------------------------------------------------------------------------











