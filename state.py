"""
Generates graph using data in file states-times.csv
which contains collected data from PAYNT about each family in format:
'nr_states,analysis_time'
Data are used to generate boxplot for 'nr_states' size
to analyze the deviation and distribution of analysis times
"""
__author__ = "Antonín Jarolím"
__version__ = "1.0.1"
__email__ = "xjarol06@vutbr.cz"

# Generic/Built-in
import datetime
import math

# Other Libs
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import statistics

columns = ['mdp_size', 'time']
df = pd.read_csv("states-times.csv", header=None, names=columns)
df['time'] = df['time'].astype('timedelta64[ns]', copy=True)

df['category'] = 0
df.loc[df['mdp_size'] > 32, 'category'] = 1
df.loc[df['mdp_size'] > 2 ** 14, 'category'] = 2

sum = sum(df['time'], datetime.timedelta())

df['time_sec'] = df['time'] / datetime.timedelta(seconds=1)
# df.where(df['mdp_size'] == 4, inplace=True)

over_second_sum = np.sum(df.loc[df['time_sec'] > 1, 'time_sec'])
no_second_sum = np.sum(df.loc[df['time_sec'] < 1, 'time_sec'])

p_var = statistics.pvariance(df['time_sec'])
standard_deviation = math.sqrt(p_var)
mean = statistics.mean(df['time_sec'])

plot = sns.boxplot(data=df, x="mdp_size", y="time_sec", )
sns.despine()
plt.yscale('log')

plt.axhline(y=1, linestyle=":")

plt.title("Time distributions regarding MDP size.")

plt.xlabel("number of states in MDP")
plt.ylabel("time [s]")

# plt.show()
plt.savefig("mdp-size-distributions.pdf")
