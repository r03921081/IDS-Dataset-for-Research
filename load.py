import pandas
import matplotlib.pyplot as plt

data = pandas.read_csv("unsw/UNSW_NB15_training-set.csv")

print(data.columns)
print(data.shape)

plt.hist(data["dur"])
plt.show()
