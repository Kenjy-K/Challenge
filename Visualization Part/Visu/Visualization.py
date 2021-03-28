#%%
import pandas as pd
import json
#%%
t_Laverune = pd.read_csv('../MMM_EcoCompt_Archives/MMM_EcoCompt_X2H20042632_Archive2020.csv')
t_Berracasa = pd.read_csv('../MMM_EcoCompt_Archives/MMM_EcoCompt_X2H19070220_Archive2020.csv')
t_Celleneuve = pd.read_csv('../MMM_EcoCompt_Archives/MMM_EcoCompt_X2H20042633_Archive2020.csv')
t_Laverune = pd.read_csv('../MMM_EcoCompt_Archives/MMM_EcoCompt_X2H20042632_Archive2020.csv')
t_Lattes_2 = pd.read_csv('../MMM_EcoCompt_Archives/MMM_EcoCompt_X2H20042634_Archive2020.csv')
t_Poste = pd.read_csv('../MMM_EcoCompt_Archives/MMM_EcoCompt_X2H20063161_Archive2020.csv')
t_Lattes_1 = pd.read_csv('../MMM_EcoCompt_Archives/MMM_EcoCompt_X2H20042635_Archive2020.csv')
t_Delmas_1 = pd.read_csv('../MMM_EcoCompt_Archives/MMM_EcoCompt_X2H20063163_Archive2020.csv')
t_Gerhardt = pd.read_csv('../MMM_EcoCompt_Archives/MMM_EcoCompt_X2H20063162_Archive2020.csv')
t_Delmas_2 = pd.read_csv('../MMM_EcoCompt_Archives/MMM_EcoCompt_X2H20063164_Archive2020.csv')
t_Tanneurs = pd.read_csv('../MMM_EcoCompt_Archives/MMM_EcoCompt_XTH19101158_Archive2020.csv')
# %%
import plotly.express as px

#%%
df = t_Laverune.copy()
df = df.rename(columns={'location/coordinates/0': 'longitude', 'location/coordinates/1': 'lattitude', 'dateObserved': 'date'})

df1 = px.data.election()
#%%

fig = px.scatter_geo(data_frame = df, lat = 'lattitude', lon = 'longitude', color="laneId",
                     hover_name="id", size="intensity",
                     animation_frame="date", fitbounds='locations', basemap_visible=True)

fig.update_layout(
        title = 'Most trafficked US airports<br>(Hover for airport names)',
        geo_scope='europe',
    )

fig.show()
# %%
