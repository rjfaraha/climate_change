#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 09:00:56 2021

@author: rfarahani
"""

# importing libraries
#import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('/Users/rfarahani/Documents/ML_general/climate_change_research/berkely_archive/GlobalTemperatures.csv', header=0, parse_dates=True, squeeze=True)
df.dropna(inplace = True)
df = df.reset_index(drop=True)

print("Columns are:", df.columns)

columns = df.columns
#Temperature values
col = [df.columns[1], df.columns[3], df.columns[5], df.columns[7]]

# time series plots
fig = plt.figure(figsize = (30, 10))
axes = fig.add_axes([0, 0, 1, 1])
axes.plot(col[0], data = df, color = 'b')
axes.plot(col[1], data = df, color = 'r')
axes.plot(col[2], data = df, color = 'y')
axes.plot(col[3], data = df, color = 'g')
axes.set_title('Time series plots')
axes.set_xlabel('Months from Jan1750 to Dec2015')
axes.set_ylabel('Temperature')
fig.savefig('Temperature.png', bbox_inches = 'tight')

#Correlation plot
df2 =df.drop('dt', axis=1)
corr = df2.corr()
fig = plt.figure(figsize = (10, 10))
ax = fig.add_axes([0, 0, 1, 1])
sns.heatmap(corr, cmap="YlGnBu",annot=True)
plt.title(f'Correlation Matrix for GlobalTemperatures', fontsize=15)
plt.show()
fig.savefig('correlation_Mtrix.png', bbox_inches = 'tight')


#LandAverageTemperature montly histogram
fig = plt.figure(figsize = (10, 10))
axes = fig.add_axes([0, 0, 1, 1])
sns.distplot(df[col[1]], ax = axes)
fig.savefig('LandAverageTemperature_monthly_displot.png', bbox_inches = 'tight')


#Convert monthly to yearly data
df['dt'] = pd.to_datetime(df['dt'])
yearly_group = df.groupby(pd.Grouper(key="dt", freq="1Y")).mean()

#LandAverageTemperature yearly histogram
fig = plt.figure(figsize = (10, 10))
axes = fig.add_axes([0, 0, 1, 1])
sns.distplot(yearly_group[col[1]], ax = axes)
fig.savefig('LandAverageTemperature_yearly_displot.png', bbox_inches = 'tight')
