import pandas as pd
import numpy as np
from sklearn import svm
#raw_data = pd.read_csv("unsw/UNSW_NB15_training-set.csv", delimiter=',', encoding="utf-8-sig")
raw_data = pd.read_csv("unsw/UNSW_Discretize.csv", delimiter=',', encoding="utf-8-sig")
print(raw_data.columns)
print(raw_data.shape)
print(raw_data)
#print(data[(data['proto']=='tcp') and (data['service']=='http')])
#print(data[data['service']=='http'])
#print(data['attack_cat'])
#print(data.corr()['label'])
#svc = svm.SVC(kernel='linear')

#new_data = data.drop(['id', 'proto', 'service', 'state'], axis=1)
#print(new_data.shape)
#print(new_data)
