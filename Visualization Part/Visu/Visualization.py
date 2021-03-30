#%%
import pandas as pd
import json
import plotly.express as px
#%%
t_Laverune = pd.read_csv('../MMM_EcoCompt_Archives/MMM_EcoCompt_X2H20042632_Archive2020.csv')
t_Berracasa = pd.read_csv('../MMM_EcoCompt_Archives/MMM_EcoCompt_X2H19070220_Archive2020.csv')
t_Celleneuve = pd.read_csv('../MMM_EcoCompt_Archives/MMM_EcoCompt_X2H20042633_Archive2020.csv')
t_Lattes_2 = pd.read_csv('../MMM_EcoCompt_Archives/MMM_EcoCompt_X2H20042634_Archive2020.csv')
t_Poste = pd.read_csv('../MMM_EcoCompt_Archives/MMM_EcoCompt_X2H20063161_Archive2020.csv')
t_Lattes_1 = pd.read_csv('../MMM_EcoCompt_Archives/MMM_EcoCompt_X2H20042635_Archive2020.csv')
t_Delmas_1 = pd.read_csv('../MMM_EcoCompt_Archives/MMM_EcoCompt_X2H20063163_Archive2020.csv')
t_Gerhardt = pd.read_csv('../MMM_EcoCompt_Archives/MMM_EcoCompt_X2H20063162_Archive2020.csv')
t_Delmas_2 = pd.read_csv('../MMM_EcoCompt_Archives/MMM_EcoCompt_X2H20063164_Archive2020.csv')
t_Tanneurs = pd.read_csv('../MMM_EcoCompt_Archives/MMM_EcoCompt_XTH19101158_Archive2020.csv')

#%%
t_Laverune.to_excel('../MMM_EcoCompt_Archives/MMM_EcoCompt_X2H20042632_Archive2020.xlsx', index = None, header=True)
t_Berracasa.to_excel('../MMM_EcoCompt_Archives/MMM_EcoCompt_X2H19070220_Archive2020.xlsx', index = None, header=True)
t_Celleneuve.to_excel('../MMM_EcoCompt_Archives/MMM_EcoCompt_X2H20042633_Archive2020.xlsx', index = None, header=True)
t_Lattes_2.to_excel('../MMM_EcoCompt_Archives/MMM_EcoCompt_X2H20042634_Archive2020.xlsx', index = None, header=True)
t_Poste.to_excel('../MMM_EcoCompt_Archives/MMM_EcoCompt_X2H20063161_Archive2020.xlsx', index = None, header=True)
t_Lattes_1.to_excel('../MMM_EcoCompt_Archives/MMM_EcoCompt_X2H20042635_Archive2020.xlsx', index = None, header=True)
t_Delmas_1.to_excel('../MMM_EcoCompt_Archives/MMM_EcoCompt_X2H20063163_Archive2020.xlsx', index = None, header=True)
t_Gerhardt.to_excel('../MMM_EcoCompt_Archives/MMM_EcoCompt_X2H20063162_Archive2020.xlsx', index = None, header=True)
t_Delmas_2.to_excel('../MMM_EcoCompt_Archives/MMM_EcoCompt_X2H20063164_Archive2020.xlsx', index = None, header=True)
t_Tanneurs.to_excel('../MMM_EcoCompt_Archives/MMM_EcoCompt_XTH19101158_Archive2020.xlsx', index = None, header=True)

#%%
df = pd.read_excel('DataVisu.xlsx')
df.sort_values('Date')
#%%
fig = px.scatter_geo(data_frame = df, lat = 'Latitude', lon = 'Longitude', color="Id", hover_name="Lane", size="Intensity", animation_frame="Date", basemap_visible=True)
fig.update_layout(
        title = 'Most trafficked US airports<br>(Hover for airport names',geo_scope='europe')
fig.show()
# %%
fig = px.density_mapbox(data_frame = df, lat = 'Latitude', lon = 'Longitude', z = 'Intensity', center = dict(lat = 43.610769, lon = 3.876716), zoom =1, hover_name= = 'Date', mapbox_style= 'stamen-watercolor', radius =10)
fig.show()
# %%
df2 = px.data.gapminder()
fig = px.scatter_geo(df2, locations="iso_alpha", color="continent",
                     hover_name="country", size="pop",
                     animation_frame="year",
                     projection="natural earth")
fig.show()
# %%
df = pd.read_excel('Berracasa.xlsx')

#%%
import pandas as pd
import numpy as np
import geoviews as gv
import geoviews.tile_sources as gvts
from geoviews import dim, opts
gv.extension('bokeh')
# %%

import plotly.express as px

df = px.data.gapminder()
fig = px.scatter(df, x="gdpPercap", y="lifeExp", animation_frame="year", animation_group="country",
           size="pop", color="continent", hover_name="country",
           log_x=True, size_max=55, range_x=[100,100000], range_y=[25,90])

fig["layout"].pop("updatemenus") # optional, drop animation buttons
fig.show()
# %%
