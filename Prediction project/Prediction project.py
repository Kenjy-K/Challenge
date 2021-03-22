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

#%% Remove nan values
bike_df.dropna(inplace=True)

#%%
#Delete useless column
# removing useless feature
bike_df = bike_df.drop(['Unnamed: 4' , 'Remarque'], axis=1)
bike_df.rename(columns = {'Vélos depuis le 1er janvier / Grand total': 'Grand total', "Vélos ce jour / Today's total": "Today's total", 'Heure / Time':'Time'}, inplace = True)

#%%
#Check types
bike_df.dtypes
#Check Info
bike_df.info()
bike_df.describe()

#%% Changing time format
bike_df['Time'] = bike_df['Time'].astype('str')
bike_df['Time']
#%%
print(df.to_string())
for j, day in df.iterrows():
    df['Date'].loc[j] = datetime.strptime(day['Date'],"%d/%m/%Y")

#%%
# Create figure and plot space
fig, ax = plt.subplots(figsize=(10, 10))

# Add x-axis and y-axis
ax.plot(df['Time'],
        df["Today's total"],
        color='purple')

# Set title and labels for axes
ax.set(xlabel="Date",
       ylabel="Precipitation (inches)",
       title="Daily Total Precipitation\nBoulder, Colorado in July 2018")

plt.show()

# %%

