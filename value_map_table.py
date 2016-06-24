import pandas as pd
import numpy as np

raw_train_data = pd.read_csv("unsw/UNSW_Discretize.csv", delimiter=',', encoding="utf-8-sig")
#print(raw_train_data.columns)
print(raw_train_data.shape)

category = {}



for feature in raw_train_data.columns:
	print(feature)
	for item in raw_train_data[feature].values:
		if item not in category:
			category[item] = feature
print(category)



