#%%Packages Importation
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from download import download
from datetime import datetime

#%%Loading the Dataset and checking it's contents and the data quality
#Import data
url='https://docs.google.com/spreadsheets/d/e/2PACX-1vQVtdpXMHB4g9h75a0jw8CsrqSuQmP5eMIB2adpKR5hkRggwMwzFy5kB-AIThodhVHNLxlZYm8fuoWj/pub?gid=2105854808&single=true&output=csv'
path_target = "./data-bike.csv"
download(url, path_target, replace = True)

bike_df = pd.read_csv('data-bike.csv', sep = ',', converters = {'Time':str})
bike_df.head()
bike_df.shape
#%%
#Delete useless column
# removing useless feature
bike_df = bike_df.drop(['Unnamed: 4' , 'Remarque'], axis=1)
bike_df.rename(columns = {'Vélos depuis le 1er janvier / Grand total': 'Cumul', "Vélos ce jour / Today's total": "Today", 'Heure / Time':'Time'}, inplace = True)

#%% Remove nan values
bike_df = bike_df.dropna()

#%% Reset Indexation
bike_df.reset_index(drop=True, inplace=True)

#%% Identification of wrong accumulaton row
for i in range(len(bike_df["Cumul"])-1):
    print(bike_df.iloc[i,2] - bike_df.iloc[i+1, 2] < 0)
    print(i)

#%% Remove repetitive rows
bike_df.drop(index=[1076,1080,1413], inplace = True)

#%% Reforting the accumulation of today's total
for i in range(len(bike_df["Cumul"])-1):
    bike_df.iloc[i+1,2] = bike_df.iloc[i,2] + bike_df.iloc[i+1,3]

#%%
#Check types
bike_df.dtypes
#Check Info
bike_df.info()
bike_df.describe()

#%% Changing time format
bike_df['Time'] = bike_df['Time'].astype('str')
bike_df['Time']
bike_df['Date'] = bike_df['Date'].astype('str')
bike_df['Date']

#%%
time_improved = pd.to_datetime(bike_df['Date'] + ' ' + bike_df['Time'], format = '%d/%m/%Y %H:%M:%S')
time_improved 

#%%
#Create correct timing format in the dataframe
bike_df['DateTime'] = time_improved

# remove useles columns
del bike_df['Date']
del bike_df['Time']
#del bike_df["Grand total"]

# %%
#Not necessary
# visualize the data set now that the time is well formated:
#bike_ts = bike_df.set_index(['DateTime'])
#bike_ts = bike_ts.sort_index(ascending = False)
#bike_ts.head(12)
#bike_ts.describe()

#%% Exporting the cleaned data into csv file
bike_df.to_csv("./df_cleaned.csv",index=False, header=True)
