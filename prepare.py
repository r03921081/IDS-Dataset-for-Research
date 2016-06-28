import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.preprocessing import OneHotEncoder
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier

raw_data = pd.read_csv("unsw/UNSW_NB15_training-set.csv", delimiter=',', encoding="utf-8-sig")
#raw_data = pd.read_csv("unsw/UNSW_Discretize.csv", delimiter=',', encoding="utf-8-sig")
print(raw_data.columns)
print(raw_data.shape)
print(raw_data[raw_data['attack_cat']=='Normal'])
#print(raw_data)
#print(data[(data['proto']=='tcp') and (data['service']=='http')])
#print(data[data['service']=='http'])
#print(raw_data['label'])
#print(data.corr()['label'])

new_data = raw_data.drop(['id', 'proto', 'service', 'state', 'attack_cat', 'label'], axis=1)
new_target = raw_data['label']
#print(new_data.shape)
#print(new_data)

np_data = new_data.as_matrix()
np_target = new_target.as_matrix()

model = GaussianNB()
model.fit(np_data, np_target)
print(model)

expected = np_target
predicted = model.predict(np_data)

print(metrics.classification_report(expected, predicted))
print(metrics.confusion_matrix(expected, predicted))

model = DecisionTreeClassifier()
model.fit(np_data, np_target)
print(model)

expected = np_target
predicted = model.predict(np_data)

print(metrics.classification_report(expected, predicted))
print(metrics.confusion_matrix(expected, predicted))
print(metrics.precision_score(expected, predicted))
