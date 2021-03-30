#%%
import numpy as np                   # for multi-dimensional containers 
import pandas as pd                  # for DataFrames
import plotly.graph_objects as go    # for data visualisation
import plotly.express as px
import plotly

#%%
access_token = "pk.eyJ1Ijoia2VuZ29za3kiLCJhIjoiY2ttdXBlM3k3MTN0OTJxcGJhd2M1dWt5MyJ9.XYDo0Boq2GU80rtXNQiwyA"
px.set_mapbox_access_token(access_token)

#%%
df = pd.read_excel('DataVisu.xlsx')
df.head()
print(df.columns.values)
df = df.dropna()

#%%
df_mask  = df['Date'] == df['Date'].max()
df_mask 
# %%
fig = px.scatter_mapbox(
    df[df_mask], 
    lat="Latitude", 
    lon="Longitude",
    size="Intensity", 
    size_max=50,
    color="Intensity", 
    color_continuous_scale=px.colors.sequential.Pinkyl,
    hover_name="Id",           
    mapbox_style='open-street-map', 
    zoom=11,
    title= 'Evolution du traffic de vélos'
)

fig.layout.coloraxis.showscale = True

fig.show()

#%%
fig = px.scatter_mapbox(
    df, 
    lat="Latitude", 
    lon="Longitude",
    size="Intensity", 
    size_max=50,
    color="Intensity", 
    color_continuous_scale=px.colors.sequential.Pinkyl,
    hover_name="Id",           
    mapbox_style='open-street-map', 
    zoom=11,
    title= 'Evolution du traffic de vélos',
    animation_frame="Date", 
    animation_group="Id"
)

fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 200
fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 200
fig.layout.coloraxis.showscale = True
fig.layout.sliders[0].pad.t = 10
fig.layout.updatemenus[0].pad.t= 10

fig.show()
#%%
fig.show()
# %%
plotly.offline.plot(fig, filename = 'filename.html', auto_open=False)
# %%
