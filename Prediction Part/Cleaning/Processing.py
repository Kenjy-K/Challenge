#%%
from datetime import datetime
import pandas as pd
from datetime import datetime
#%%
meteo_df = pd.read_csv("../Datasets/df_cleaned_meteo.csv")
bike_df = pd.read_csv("../Datasets/df_cleaned_space.csv")

# %%
bike_df['Date'] = bike_df['Date'].astype('str')
time_improved = pd.to_datetime(bike_df['Date'], format = '%Y-%m-%d')
bike_df['Date'] = time_improved
del bike_df['DateTime']

#%%
df_final = pd.DataFrame(columns = ['Date', 'Cumul', 'Today'])

date_range = pd.date_range(start = bike_df['Date'].iloc[0], end = bike_df['Date'].iloc[-1])                              

for date in date_range:
    df = bike_df[bike_df['Date'] == date]
    Cumul = 0
    Today = 0
    for i, days in df.iterrows():
         Today  = Today + days['Today']
         Cumul = Cumul + days['Cumul']
    df_final = df_final.append({'Date': date, 'Cumul': Cumul, 'Today': Today}, ignore_index=True)

print(df_final)
# %%
for i in range( len(df_final["Today"]) -1):
    df_final.iloc[i+1,1] = df_final.iloc[i,1] + df_final.iloc[i+1,2]

df_final.iloc[0,1] = 550

#%%
df_final.to_excel("./final_bike.xls",index=False, header=True)
meteo_df.to_excel("./final_meteo.xls",index=False, header=True)
# %%
final = pd.read_excel("Final.xlsm")

# %%
final['date_ordinal'] = pd.to_datetime(final['Date']).apply(lambda date: date.toordinal())
# %%
final.to_excel("final.xls",index=False, header=True)
