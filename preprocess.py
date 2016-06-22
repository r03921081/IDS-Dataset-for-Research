import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction import DictVectorizer as dv
from sklearn.cross_validation import train_test_split

raw_data = pd.read_csv("unsw/UNSW_NB15_training-set.csv", delimiter=',', encoding="utf-8-sig")
#raw_data = pd.read_csv("unsw/UNSW_Discretize.csv", delimiter=',', encoding="utf-8-sig")
print(raw_data.columns)
print(raw_data.shape)
#print(raw_data)
#print(data[(data['proto']=='tcp') and (data['service']=='http')])
#print(data[data['service']=='http'])
#print(raw_data['label'])
#print(data.corr()['label'])

old_data = raw_data.drop(['id', 'attack_cat'], axis=1)
#print(old_data)
pre_data = old_data.T.to_dict().values()
vectorizer = dv(sparse = False)
dv_data = vectorizer.fit_transform(pre_data)
#print(dv_data)


#encode_data = pd.get_dummies(raw_data['state'])
#print(encode_data)

new_data = raw_data.drop(['id', 'proto', 'service', 'state', 'attack_cat', 'label'], axis=1)
new_target = raw_data['label']
#print(new_data.shape)
#print(new_data)

np_data = new_data.as_matrix()
np_target = new_target.as_matrix()


# NaiveBayes
model = GaussianNB()
model.fit(dv_data, np_target)
print(model)

expected = np_target
predicted = model.predict(dv_data)

print(metrics.classification_report(expected, predicted))
print(metrics.confusion_matrix(expected, predicted))

model = GaussianNB()
model.fit(np_data, np_target)
print(model)

expected = np_target
predicted = model.predict(np_data)

print(metrics.classification_report(expected, predicted))
print(metrics.confusion_matrix(expected, predicted))

# DecisionTree
model = DecisionTreeClassifier()
model.fit(dv_data, np_target)
print(model)

expected = np_target
predicted = model.predict(dv_data)

print(metrics.classification_report(expected, predicted))
print(metrics.confusion_matrix(expected, predicted))

model = DecisionTreeClassifier()
model.fit(np_data, np_target)
print(model)

expected = np_target
predicted = model.predict(np_data)

print(metrics.classification_report(expected, predicted))
print(metrics.confusion_matrix(expected, predicted))



