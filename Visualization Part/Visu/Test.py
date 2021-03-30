#%%
import numpy as np                   # for multi-dimensional containers 
import pandas as pd                  # for DataFrames
import plotly.graph_objects as go    # for data visualisation
import plotly.express as px

#%%
data_url = 'https://shahinrostami.com/datasets/time-series-19-covid-combined.csv'
data = pd.read_csv(data_url)
data.head()
print(data.columns.values)
# %%
missing_states = pd.isnull(data['Province/State'])
data.loc[missing_states,'Province/State'] = data.loc[missing_states,'Country/Region']
# %%
data['Active'] = data['Confirmed'] - data['Recovered'] - data['Deaths']
data = data.dropna()
date_mask = data['Date'] == data['Date'].max()
date_mask
# %%
fig = px.scatter_mapbox(
    data[date_mask], lat="Lat", lon="Long",
    size="Confirmed", size_max=50,
    color="Deaths", color_continuous_scale=px.colors.sequential.Pinkyl,
    hover_name="Province/State",           
    mapbox_style='dark', zoom=1
)
fig.layout.coloraxis.showscale = False
fig.show()
# %%
fig = px.scatter_mapbox(
    data, lat="Lat", lon="Long",
    size="Active", size_max=50,
    color="Deaths", color_continuous_scale=px.colors.sequential.Pinkyl,
    hover_name="Province/State",           
    mapbox_style='dark', zoom=1,
    animation_frame="Date", animation_group="Province/State"
)
fig.show()
# %%
fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 200
fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 200
fig.layout.coloraxis.showscale = False
fig.layout.sliders[0].pad.t = 10
fig.layout.updatemenus[0].pad.t= 10
# %%
fig.show()

#%%
plotly.offline.plot(fig, filename = 'filename.html', auto_open=False)