import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction import DictVectorizer as dv
from sklearn.cross_validation import train_test_split
from sklearn import linear_model

feature = ["sttl", "ct_dst_ltm", "is_ftp_login", "ct_srv_src", "djit"]

raw_train_data = pd.read_csv("unsw/UNSW_Discretize.csv", delimiter=',', encoding="utf-8-sig")

train_data = pd.DataFrame(index = raw_train_data.index, columns = feature)

for item in feature:
	train_data[feature] = raw_train_data[feature]

train_target = raw_train_data['attack_cat']

data = train_data.as_matrix()
target = train_target.as_matrix()

np_train_data, np_test_data, np_train_target, np_test_target = train_test_split(data, target, test_size = 0.33)


# LogisticRegression
model = linear_model.SGDClassifier()
model.fit(np_train_data, np_train_target)
print(model)

expected = np_test_target
predicted = model.predict(np_test_data)

print(metrics.classification_report(expected, predicted))
print(metrics.confusion_matrix(expected, predicted))

# NaiveBayes
model = GaussianNB()
model.fit(np_train_data, np_train_target)
print(model)

expected = np_test_target
predicted = model.predict(np_test_data)

print(metrics.classification_report(expected, predicted))
print(metrics.confusion_matrix(expected, predicted))

# DecisionTree
model = DecisionTreeClassifier()
model.fit(np_train_data, np_train_target)
print(model)

expected = np_test_target
predicted = model.predict(np_test_data)

print(metrics.classification_report(expected, predicted))
print(metrics.confusion_matrix(expected, predicted))
