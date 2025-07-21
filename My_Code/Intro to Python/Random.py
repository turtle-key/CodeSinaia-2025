import random
import pandas as pd
count = 0
minvalue = 0
maxvalue = 0

count = int(input("Enter the number of numbers you want to generate:"))
minvalue = int(input("Enter the minvalue:"))
maxvalue = int(input("Enter the maxvalue: "))
print(f"Start generating {count} random numbers, between {minvalue} and {maxvalue}") 

freq_count = {}
mean = 0
stddev = 0
for i in range(0, count):
    number= random.randint(minvalue, maxvalue)
    print(f"The generated number is {number}")
    if number not in freq_count:
        freq_count[number] = []
    freq_count[number].append(i)
    mean = mean + number
mean = mean / count
pd.std()
with open("dataset.txt", "w") as data:
    for i in freq_count.keys():
        data.write(f"{i} {freq_count[i]}\n")
print(f"There are {len(freq_count)} distinct numbers")
print(f"The mean is {mean} and the standard deviation is {stddev}")
