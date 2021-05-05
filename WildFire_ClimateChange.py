#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 09:00:56 2021

@author: rfarahani
"""

# importing libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import numpy as np

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
plt.legend(col)
axes.set_title('Time series plots')
axes.set_xlabel('Months from Jan1850 to Dec2015')
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
sns.distplot(df[col[0]], ax = axes)
fig.savefig('LandAverageTemperature_monthly_displot.png', bbox_inches = 'tight')


#Convert monthly to yearly data
df['dt'] = pd.to_datetime(df['dt'])
yearly_group = df.groupby(pd.Grouper(key="dt", freq="1Y")).mean()

#LandAverageTemperature yearly histogram
fig = plt.figure(figsize = (10, 10))
axes = fig.add_axes([0, 0, 1, 1])
sns.distplot(yearly_group[col[0]], ax = axes)
fig.savefig('LandAverageTemperature_yearly_displot.png', bbox_inches = 'tight')

#Lag plots
f, ax = plt.subplots()
pd.plotting.lag_plot(df[col[0]], ax=ax)
pd.plotting.lag_plot(df[col[1]], ax=ax, c='k')
pd.plotting.lag_plot(df[col[2]], ax=ax, c='r')
pd.plotting.lag_plot(df[col[3]], ax=ax, c='y')
plt.legend(col)
plt.savefig('lagplot_all.png')

f, ax = plt.subplots()
pd.plotting.lag_plot(df[col[0]])
plt.title('LandAverageTemperature')
plt.savefig('lagplot_LandAvTemp.png')


f, ax = plt.subplots()
pd.plotting.lag_plot(df[col[1]])
plt.title('LandMaxTemperature')
plt.savefig('lagplot_LandMaxTemp.png')
f, ax = plt.subplots()
pd.plotting.lag_plot(df[col[2]])
plt.title('LandMinTemperature')
plt.savefig('lagplot_LandMinTemp.png')
f, ax = plt.subplots()
pd.plotting.lag_plot(df[col[3]])
plt.title('LandOceanAvg')
plt.savefig('lagplot_LandOceanAvgTemp.png')

#Looking at city informations
df_city = pd.read_csv('/Users/rfarahani/Documents/ML_general/climate_change_research/berkely_archive/GlobalLandTemperaturesByCity.csv', header=0, parse_dates=True, squeeze=True)
df_city.dropna(inplace = True)
df_city = df_city.reset_index(drop=True)
df_city.columns


df_city =df_city.loc[df_city['City'] == 'Berkeley']
df_city['dt'] = pd.to_datetime(df_city['dt'])


#lag profile for Berkely
f, ax = plt.subplots()
pd.plotting.lag_plot(df_city[df_city.columns[1]])
plt.title('AverageTemperature_Berkeley')
plt.savefig('lagplot_AvTemp_Berkeley.png')


#Read Fire history shapefile
Fires_gdf = gpd.read_file("/Users/rfarahani/Documents/ML_general/climate_change_research/Fire_statistics/mtbs_perims_DD/mtbs_perims_DD.shp")
Fires_df = pd.DataFrame(Fires_gdf)

Fires_df['Ig_Date'] = pd.to_datetime(Fires_df['Ig_Date'])
Fires_df = Fires_df[Fires_df['Incid_Type'] == 'Wildfire']

#Groupby year
Fires_df=Fires_df.groupby(Fires_df['Ig_Date'].map(lambda x: x.year)).mean().reset_index()


min_date=Fires_df['Ig_Date'].min()
max_date=Fires_df['Ig_Date'].max()
sns.set(style="whitegrid")
sns.set_color_codes("pastel")
_, ax=plt.subplots(figsize=(10, 6))

plt.plot(Fires_df['Ig_Date'], Fires_df['BurnBndAc'], color='black')
plt.xlim(min_date, max_date)
ax.set_title('Burn areas')
plt.savefig('Burn_areas_yearly.png')
