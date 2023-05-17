
# Generic/Built-in
import datetime
import math

# Other Libs
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import statistics

columns = ['family_size', 'time']
df = pd.read_csv("family-times.csv", header=None, names=columns)
df['time'] = df['time'].astype('timedelta64[ns]', copy=True)

df['category'] = 0
df.loc[df['family_size'] > 32, 'category'] = 1
df.loc[df['family_size'] > 2 ** 14, 'category'] = 2

sum = sum(df['time'], datetime.timedelta())

df['time_sec'] = df['time'] / datetime.timedelta(seconds=1)
# df.where(df['family_size'] == 4, inplace=True)

df['time'] = df['time'].dt.seconds
pd.to_pickle(df, "family-sizes.pickle")

p_var = statistics.pvariance(df['time_sec'])
standard_deviation = math.sqrt(p_var)
mean = statistics.mean(df['time_sec'])

plot = sns.boxplot(data=df, x="family_size", y="time_sec")
sns.despine()
plt.yscale('log')
plt.xticks(rotation=40)

plt.axhline(y=1, linestyle=":")

plt.subplots_adjust(bottom=0.2)

plt.xlabel("size of the family")
plt.ylabel("time [s]")

plt.title("Time distributions regarding family size.")

# plt.show()
plt.savefig("family-size-distributions.pdf")

