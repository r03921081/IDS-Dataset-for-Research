import pandas
from sklearn import svm

data = pandas.read_csv("unsw/UNSW_NB15_training-set.csv", delimiter=',', index_col="id", encoding="utf-8-sig")

print(data.columns)
print(data.shape)

print(data['attack_cat'])

print(data.corr()['label'])

svc = svm.SVC(kernel='linear')

