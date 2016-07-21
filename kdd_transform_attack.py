import pandas as pd
import numpy as np

dos_type = ["back", "land", "neptune", "pod", "smurf", "teardrop"]
u2r_type = ["buffer_overflow", "loadmodule", "perl", "rootkit"]
r2l_type = ["ftp_write", "guess_passwd", "imap", "multihop", "phf", "spy", "warezclient", "warezmaster"]
probe_type = ["ipsweep", "nmap", "satan", "portsweep"]

old_raw_train_data = pd.read_csv("nsl_kdd/New_KDD_Train_Discretization_freq.csv", delimiter=',', encoding="utf-8-sig")
print(old_raw_train_data.shape)
raw_train_data = pd.DataFrame(index = old_raw_train_data.index, columns = old_raw_train_data.columns)
#print(old_raw_train_data.ix[1000])
print(old_raw_train_data.shape)

for feature in old_raw_train_data.columns:
	#print(feature + " " + old_raw_train_data[feature])
	if feature != "class":
		raw_train_data[feature] = old_raw_train_data[feature]
	else: # Class
		for i in range(len(old_raw_train_data[feature])):
			#print old_raw_train_data[feature].ix[i]
			if old_raw_train_data[feature].ix[i] in dos_type:
				raw_train_data[feature].ix[i] = "dos"
			elif old_raw_train_data[feature].ix[i] in u2r_type:
				raw_train_data[feature].ix[i] = "u2r"
			elif old_raw_train_data[feature].ix[i] in r2l_type:
				raw_train_data[feature].ix[i] = "r2l"
			elif old_raw_train_data[feature].ix[i] in probe_type:
				raw_train_data[feature].ix[i] = "probe"
			elif old_raw_train_data[feature].ix[i] == "normal":
				raw_train_data[feature].ix[i] = "normal"	
			else:
				print "Bad word: " + old_raw_train_data[feature].ix[i]
#print(raw_train_data.ix[1000])
print(raw_train_data.shape)

raw_train_data.to_csv("nsl_kdd/New_KDD_Train_Discretization_freq_five.csv", sep=',', encoding='utf-8-sig')
