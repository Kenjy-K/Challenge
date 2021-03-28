#%% Packages
import pandas as pd
from datetime import datetime

#%% Datas

#Bike data
url='https://docs.google.com/spreadsheets/d/e/2PACX-1vQVtdpXMHB4g9h75a0jw8CsrqSuQmP5eMIB2adpKR5hkRggwMwzFy5kB-AIThodhVHNLxlZYm8fuoWj/pub?gid=2105854808&single=true&output=csv'
data_bike = pd.read_csv(url, sep = ',')

#Weather data
meteo_2020 = pd.read_csv('../Datasets/export-montpellier2020.csv')
meteo_2021 = pd.read_csv('../Datasets/export-montpellier2021.csv')
frames = [meteo_2020, meteo_2021]
meteo = pd.concat(frames, ignore_index = True)

#Rename and delete useless colums
data_bike.rename(columns={"Heure / Time": "Time", "Vélos depuis le 1er janvier / Grand total": "Grand Total", "Vélos ce jour / Today's total": "Today_total"}, inplace=True)
data_bike.drop(['Unnamed: 4', 'Remarque', "Grand Total"], axis=1, inplace=True)
data_bike.dropna(inplace=True)

#%% Changing time format
data_bike['Time'] = data_bike['Time'].astype('str')
data_bike['Time']
data_bike['Date'] = data_bike['Date'].astype('str')
data_bike['Date']

#%%
time_improved = pd.to_datetime(data_bike['Date'] + ' ' + data_bike['Time'], format = '%d/%m/%Y %H:%M:%S')
time_improved 


#%%
#Create correct timing format in the dataframe
data_bike['DateTime'] = time_improved

# remove useles columns
del data_bike['Date']
del data_bike['Time']

# %%
# visualize the data set now that the time is well formated:
data_bike = data_bike.set_index(['DateTime'])
data_bike = data_bike.sort_index(ascending = False)

# %%
#cumuler les données d'une journée en une seule data
for date in data_bike["DateTime"]:
    df = data_bike[data_bike['DateTime'] == date]
    Today_total = 0
    for i, days in df.iterrows():
         Today_total = Today_total + days['Today_total']
    data_final = data_final.append({'Date': date, 'Today_total': Today_total},ignore_index=True)

#%%
data_final.drop([374],inplace=True)

#%%
data_final.to_csv('../Datasets/Dataset_processed.csv', index=False, header=True)

data_final.set_index('Date', inplace=True)
meteo.set_index('DATE',inplace=True)


#%%
df = pd.concat([data_final, meteo], axis=1, join='inner')
df.reset_index(inplace=True)
df.rename(columns={'index': 'Date'},inplace=True)
data = pd.read_csv('../Datasets/Dataset_processed.csv')


#%%
date_range_2 = pd.date_range(start=datetime.strptime('2020-07-01', "%Y-%m-%d"), end=datetime.strptime('2020-08-30', "%Y-%m-%d"))

hollidayList = []
for date in date_range_2:
        hollidayList.append({'Date': date, 'hollyday': 1})

hollyday_df = pd.DataFrame(hollidayList)

df.set_index('Date',inplace=True)
hollyday_df.set_index('Date',inplace=True)
dataframe = pd.concat([df, hollyday_df], axis=1)
dataframe.reset_index(inplace=True)
dataframe.rename(columns={'index': 'Date'},inplace=True)
dataframe.fillna(0.4,inplace=True)
dataframe.drop(columns=['TEMPERATURE_MORNING_C','TEMPERATURE_NOON_C','TEMPERATURE_EVENING_C','VISIBILITY_AVG_KM','PRESSURE_MAX_MB','DEWPOINT_MAX_C','WEATHER_CODE_MORNING','WEATHER_CODE_NOON','WEATHER_CODE_EVENING','TOTAL_SNOW_MM','UV_INDEX','OPINION'],inplace=True)
print(dataframe.to_string())
dataframe.to_csv('../Datasets/Dataset_clean.csv',index=False,header=True)
# %%
