import pandas as pd
import statistics
import matplotlib.pyplot as plt

df = pd.read_csv("mountains_db.tsv", sep='\t', header=None)
df_valid = df.dropna(subset=[1])
df_valid[1] = df_valid[1].astype(int)

#exercise 1
print(f"Sunt {len(df[3].unique())} tari in baza de date")
array = df[1].dropna().astype(int).tolist()

#exercise 2
missing_count = df[1].isna().sum()
print(f"Pentru {missing_count} munti lipseste informatia de alittudine")

#exercise 3
print(f"Min mountain: {min(array)}; Max mountain: {max(array)}")
print(f"Mean of the sequence: {statistics.mean(array)}")
print(f"Median of the sequence: {statistics.median(array)}")
print(f"Standard Deviation of the sequence: {statistics.stdev(array)}")

#exercise 4
n = int(input("Enter the N value"))
print(f"The Top{n} highest mountains in the world are:\n")
df.sort_values(by=[1])
for i in range(0, n):
  print(df.loc[i].tolist())

#exercise 5
plt.figure(figsize=(8, 4))
plt.title("Bar chart of countries (x) and their mountains (y)")
plt.xlabel("Country ISO")
plt.ylabel("Number of Mountains")
country_counts = df[3].value_counts()
plt.bar(country_counts.index, country_counts.values)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#exercise 6
max_altitudes = df_valid.groupby(2)[1].max().sort_values(ascending=False)
plt.figure(figsize=(8, 4))
plt.title("Bar chart of countries (x) and their max alitude reached by their mountains (y)")
plt.xlabel("Country")
plt.ylabel("Max Altitude")
plt.bar(max_altitudes.index, max_altitudes.values)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#exercise 7
plt.figure(figsize=(4, 6))
plt.title("Distribution of the altitudes of the mountains")
plt.ylabel("values distribution")
all_altitudes = df_valid[1].tolist()
plt.boxplot(all_altitudes, whis=[0, 100])
plt.show()

#exercise 8
grouped_altitudes = df_valid.groupby(2)[1].apply(list)
countries = grouped_altitudes.index.tolist()
data = grouped_altitudes.tolist()
plt.figure(figsize=(max(10, len(countries) * 0.5), 6))
plt.boxplot(data, labels=countries, whis=[0, 100])
plt.xticks(rotation=90)
plt.xlabel("Country")
plt.ylabel("Altitude (m)")
plt.title("Min, Median, Max, and Distribution of Mountain Altitudes per Country")
plt.tight_layout()
plt.show()
