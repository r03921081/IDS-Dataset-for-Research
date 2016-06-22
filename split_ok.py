import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction import DictVectorizer as dv
from sklearn.cross_validation import train_test_split

raw_train_data = pd.read_csv("unsw/UNSW_NB15_training-set.csv", delimiter=',', encoding="utf-8-sig")
#raw_data = pd.read_csv("unsw/UNSW_Discretize.csv", delimiter=',', encoding="utf-8-sig")
print(raw_train_data.columns)
print(raw_train_data.shape)
#print(raw_data)
#print(data[(data['proto']=='tcp') and (data['service']=='http')])
#print(data[data['service']=='http'])
#print(raw_data['label'])
#print(data.corr()['label'])
raw_test_data = pd.read_csv("unsw/UNSW_NB15_testing-set.csv", delimiter=',', encoding="utf-8-sig")
print(raw_test_data.columns)
print(raw_test_data.shape)

frames = [raw_train_data, raw_test_data]
raw_data = pd.concat(frames, keys=['train', 'test'])

vectorizer = dv(sparse = False)

old_raw_data = raw_data.drop(['id', 'attack_cat', 'label'], axis=1)
pre_raw_data = old_raw_data.T.to_dict().values()
dv_raw_data = vectorizer.fit_transform(pre_raw_data)
print(vectorizer.get_feature_names())

#old_train_data = raw_train_data.drop(['id', 'attack_cat', 'label'], axis=1)
#pre_train_data = old_train_data.T.to_dict().values()
#dv_train_data = vectorizer.fit_transform(pre_train_data)
#dv_train_target = raw_train_data['label']

#old_test_data = raw_test_data.drop(['id', 'attack_cat', 'label'], axis=1)
#pre_test_data = old_test_data.T.to_dict().values()
#dv_test_data = vectorizer.fit_transform(pre_test_data)
#dv_test_target = raw_test_data['label']

new_train_data = raw_train_data.drop(['id', 'proto', 'service', 'state', 'attack_cat', 'label'], axis=1)
new_train_target = raw_train_data['label']
new_test_data = raw_test_data.drop(['id', 'proto', 'service', 'state', 'attack_cat', 'label'], axis=1)
new_test_target = raw_test_data['label']

np_train_data = new_train_data.as_matrix()
np_train_target = new_train_target.as_matrix()
np_test_data = new_test_data.as_matrix()
np_test_target = new_test_target.as_matrix()
#print(np_train_data[1])
#print(np_test_data[1])

# NaiveBayes
#model = GaussianNB()
#model.fit(dv_train_data, dv_train_target)
#print(model)

#expected = dv_test_target
#predicted = model.predict(dv_test_data)

#print(metrics.classification_report(expected, predicted))
#print(metrics.confusion_matrix(expected, predicted))

model = GaussianNB()
model.fit(np_train_data, np_train_target)
print(model)

expected = np_test_target
predicted = model.predict(np_test_data)


print(metrics.classification_report(expected, predicted))
print(metrics.confusion_matrix(expected, predicted))

# DecisionTree
#model = DecisionTreeClassifier()
#model.fit(dv_train_data, dv_train_target)
#print(model)

#expected = dv_test_target
#predicted = model.predict(dv_test_data)

#print(metrics.classification_report(expected, predicted))
#print(metrics.confusion_matrix(expected, predicted))

model = DecisionTreeClassifier()
model.fit(np_train_data, np_train_target)
print(model)

expected = np_test_target
predicted = model.predict(np_test_data)

print(metrics.classification_report(expected, predicted))
print(metrics.confusion_matrix(expected, predicted))

