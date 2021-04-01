#%%
#Import of packages
#I decided to use the plotly package that allows to plot beautiful maps

import numpy as np                   # for multi-dimensional containers 
import pandas as pd                  # for DataFrames
import plotly.graph_objects as go    # for data visualisation
import plotly.express as px
import plotly

#%%

#It's necessary to use my token to operate the mapbox function
access_token = "pk.eyJ1Ijoia2VuZ29za3kiLCJhIjoiY2ttdXBlM3k3MTN0OTJxcGJhd2M1dWt5MyJ9.XYDo0Boq2GU80rtXNQiwyA"
px.set_mapbox_access_token(access_token)

#%%

# we import our data from the xlsx file
df = pd.read_excel('DataVisu.xlsx')
df.head()
print(df.columns.values)

#delete nan values
df = df.dropna()

#%%

#we create a mask for this data column
df_mask  = df['Date'] == df['Date'].max()
df_mask 
# %%

#we plot the figure using px.scatter_mapbox function
# Different options can be chosen such as latitude, longitude of our spots, the range color, the title, zoom, ...
fig = px.scatter_mapbox(
    df[df_mask], 
    lat="Latitude", 
    lon="Longitude",
    size="Intensity", 
    size_max=50,
    color="Intensity", 
    color_continuous_scale=px.colors.sequential.Viridis,
    hover_name="Id",           
    mapbox_style='open-street-map', 
    zoom=11,
    title= 'Evolution du traffic de vélos aux bornes de comptage à Montpellier (see https://github.com/Kenjy-K/Challenge)'
)

fig.layout.coloraxis.showscale = True

fig.show()

#%%

# Now, we add an animation frame which is a slidr in order to make time go by
fig = px.scatter_mapbox(
    df, 
    lat="Latitude", 
    lon="Longitude",
    size="Intensity", 
    size_max=50,
    color="Intensity", 
    color_continuous_scale=px.colors.sequential.Viridis,
    hover_name="Id",           
    mapbox_style='outdoors', 
    zoom=11,
    title= 'Evolution du traffic de vélos aux bornes de comptage à Montpellier (see https://github.com/Kenjy-K/Challenge)',
    animation_frame="Date", 
    animation_group="Id"
)

fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 200
fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 200
fig.layout.coloraxis.showscale = True
fig.layout.sliders[0].pad.t = 10
fig.layout.updatemenus[0].pad.t= 10

#Now we can plot the figure
fig.show()

# %%
#we export the file using a html page
plotly.offline.plot(fig, filename = 'index.html', auto_open=False)

# %%
