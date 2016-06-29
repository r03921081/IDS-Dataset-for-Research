import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction import DictVectorizer as dv
from sklearn.cross_validation import train_test_split
from sklearn import linear_model

#feature = ["is_sm_ips_ports", "dloss", "response_body_len", "dmean", "ct_dst_ltm", "is_ftp_login", "sbytes", "ackdat", "ct_dst_sport_ltm", "sloss", "trans_depth", "dload", "synack", "dpkts", "sttl", "tcprtt", "ct_srv_src", "ct_flw_http_mthd", "spkts", "dbytes"]

feature = ["is_sm_ips_ports", "dloss", "response_body_len", "dmean", "ct_dst_ltm", "is_ftp_login", "sbytes", "ackdat", "ct_dst_sport_ltm", "sloss", "trans_depth", "dload", "synack", "dpkts", "sttl", "tcprtt", "ct_srv_src", "ct_flw_http_mthd", "spkts", "dbytes", "djit", "sjit", "sinpkt", "dinpkt"]

print(len(feature))

raw_train_data = pd.read_csv("unsw/UNSW_NB15_training-set.csv", delimiter=',', encoding="utf-8-sig")

train_data = pd.DataFrame(index = raw_train_data.index, columns = feature)

for item in feature:
	train_data[item] = raw_train_data[item]

train_target = raw_train_data['label']

data = train_data.as_matrix()
target = train_target.as_matrix()

np_train_data, np_test_data, np_train_target, np_test_target = train_test_split(data, target, test_size = 0.33)


# LogisticRegression
model = linear_model.SGDClassifier()
model.fit(np_train_data, np_train_target)
print(model)

expected = np_test_target
predicted = model.predict(np_test_data)

print("LogisticRegression")
print(metrics.classification_report(expected, predicted))
print(metrics.confusion_matrix(expected, predicted))

# NaiveBayes
model = GaussianNB()
model.fit(np_train_data, np_train_target)
print(model)

expected = np_test_target
predicted = model.predict(np_test_data)

print("NaiveBayes GaussianNB")
print(metrics.classification_report(expected, predicted))
print(metrics.confusion_matrix(expected, predicted))

# DecisionTree
model = DecisionTreeClassifier()
model.fit(np_train_data, np_train_target)
print(model)

expected = np_test_target
predicted = model.predict(np_test_data)

print("DecisionTree")
print(metrics.classification_report(expected, predicted))
print(metrics.confusion_matrix(expected, predicted))
