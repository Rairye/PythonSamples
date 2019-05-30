# Data source: https://www.kaggle.com/ilayaraja97/temperature-data-seattle
# Data source license: CC0: Public Domain
# Requires pandas, numpy, and matplotlib

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


data = pd.read_csv('temps.csv', encoding='utf-8')

actualTemp = list(data["actual"])

highestAnnual = 0
lowestAnnual = 0
total = 0.0

days = []
temperatures = []

for i in range(len(actualTemp)):
    temp = round(((actualTemp[i] - 32)/1.8), 2)
    if temp > highestAnnual:
        highestAnnual = temp
        
    if lowestAnnual > temp or lowestAnnual == 0:
        lowestAnnual = temp
        
    days.append(i+1)
    temperatures.append(temp)
    total +=temp
        
print("Highest annual temperature: ", highestAnnual, "degrees Celsius")
print("Lowest annual temperature: ", lowestAnnual, "degrees Celsius")
print("Annual average temperature: ", round((total/len(actualTemp)), 2), "degrees Celsius")


plt.plot(days, temperatures)
plt.xlabel("Day")
plt.ylabel("Temperature")
plt.show()
