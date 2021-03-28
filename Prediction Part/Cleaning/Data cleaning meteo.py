#%%
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

#%%
df = pd.read_csv("../Cleaning/df_cleaned.csv")

# %%
# Create figure and plot space
fig, axes = plt.subplots(2, 1, figsize=(30, 20), sharex=True)

# Add x-axis and y-axis
# Set title and labels for axes
axes[0].plot(df["Cumul"], '.')
axes[0].set_title("Cumul du nombre de passage de vélos chaque année")
axes[0].set_ylabel("Comptage vélo")

axes[1].plot(df['Today'])
axes[1].set_title("Nombre de vélos point de passage Montpellier")
axes[1].set_ylabel("Nombre de vélos total")

plt.show()

#%%
#Importing meteo data
df_meteo1 = pd.read_csv('../Datasets/export-montpellier2020.csv')
df_meteo2 = pd.read_csv('../Datasets/export-montpellier2021.csv')
meteo = [df_meteo1, df_meteo2]
meteo_df = pd.concat(meteo, ignore_index=True)

# %%
meteo_df['DATE'] = meteo_df['DATE'].astype('str')

#%%
time_improved = pd.to_datetime(meteo_df['DATE'], format = '%Y-%m-%d')
time_improved 

#%%
#Create correct timing format in the dataframe
meteo_df['DateTime'] = time_improved
# remove useles columns
del meteo_df['DATE']

#%%
#Remove useless columns
meteo_df.drop(['OPINION', 'TOTAL_SNOW_MM', 'WEATHER_CODE_EVENING','WEATHER_CODE_NOON','WEATHER_CODE_MORNING', 'TEMPERATURE_MORNING_C', 'TEMPERATURE_NOON_C', 'TEMPERATURE_EVENING_C','VISIBILITY_AVG_KM', 'PRESSURE_MAX_MB','DEWPOINT_MAX_C','UV_INDEX'], axis=1, inplace=True)

# %%
#%% Exporting the cleaned data meteo into csv file
meteo_df.to_csv("./df_cleaned_meteo.csv",index=False, header=True)
# %%
