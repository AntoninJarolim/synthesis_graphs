"""
Generates graph using data in folder rate-data/
which contains collected outputs of synthesis using PAYNT.
Relevant statics from the outputs are scraped to dataframe in format:
file_name, synthesis_time, iterations
The number of iterations per second is calculated from the scraped data
and two scatterplot graphs are printed to one image
"""
__author__ = "Antonín Jarolím"
__version__ = "1.0.1"
__email__ = "xjarol06@vutbr.cz"

# Generic/Built-in
import os
import re

# Other Libs
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.patches import Circle


data = {
    'file_name': [],
    'synthesis_time': [],
    'iterations': [],
}

df = pd.DataFrame(data)

data_dir = os.path.join(os.getcwd(), "rate-data")


def get_info_from_file(file):
    text = file.read()
    synthesis_time = re.search("method: AR, synthesis time: ([0-9]+.[0-9]+)", text)
    iterations = re.search("iterations: ([0-9]+)", text)
    return synthesis_time, iterations


for filename in os.listdir(data_dir):
    with open(os.path.join(data_dir, filename), 'r') as f:
        synthesis_time, iterations = get_info_from_file(f)
        if synthesis_time is not None:
            df.loc[len(df.index)] = [filename, synthesis_time.group(1), iterations.group(1)]

df['iterations'] = pd.to_numeric(df['iterations'])
df['synthesis_time'] = pd.to_numeric(df['synthesis_time'])


def find_rate(text):
    rate_value = re.search("lambda=([0-9]+.[0-9]+)", text)
    return rate_value.group(1)


df['iterations_per_second'] = df['iterations'] / df['synthesis_time']
df['rate'] = pd.to_numeric(df['file_name'].apply(find_rate))

df = df.sort_values('rate').reset_index()
print(df)

# left graph
plot = sns.scatterplot(df, x="rate", y="synthesis_time", color="blue")
plt.ylabel("synthesis time [s]")
plt.axhline(y=2900, linestyle="--", color="blue")

# plot.set_xticks([0, 0.1, 0.2, 0.3, 0.4], labels=[1,1,1,1,1])
plot.set(xlim=(0.04, 0.42))
# Second twinx graph
plot = sns.scatterplot(df, x="rate", y="iterations_per_second",
                       ax=plot.axes.twinx(), color="red")
sns.despine(right=False)


plt.ylabel("Iterations per second")
plot.legend(handles=[Circle((0, 0), radius=1, color="b", label='synthesis time'),
                     Circle((0, 0), radius=1, color="r", label='iterations per second')],
            loc="upper center")

plt.title("iterations per second vs synthesis speed")

# plt.show()
plt.savefig("changing-rate.pdf")
