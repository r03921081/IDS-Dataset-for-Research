import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction import DictVectorizer as dv
from sklearn.cross_validation import train_test_split
from sklearn import linear_model

feature = ["ct_dst_sport_ltm"]

raw_train_data = pd.read_csv("unsw/UNSW_NB15_training-set.csv", delimiter=',', encoding="utf-8-sig")
raw_test_data = pd.read_csv("unsw/UNSW_NB15_testing-set.csv", delimiter=',', encoding="utf-8-sig")

train_data = pd.DataFrame(index = raw_train_data.index, columns = feature)
test_data = pd.DataFrame(index = raw_test_data.index, columns = feature)

for item in feature:
	train_data[item] = raw_train_data[item]
	test_data[item] = raw_test_data[item]

train_target = raw_train_data['label']
test_target = raw_test_data['label']

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

print("NaiveBayes GaussianNB")
print(metrics.classification_report(expected, predicted))
print(metrics.confusion_matrix(expected, predicted))

