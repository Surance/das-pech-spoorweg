import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


# Create dataset
# For now this is a simple dataset created for the function
data = {
    'y_1': [4.46888876, 4.900277615, 4.638333321, 4.481666565],
    'x_1': [51.92499924, 52.37888718, 52.38777924, 52.16611099],
    'y_2': [4.761111259, 4.66833353, 4.704444408, 4.761944294],
    'x_2': [52.95527649, 51.80722046, 52.01750183, 52.30944443]
}

# Create dataframe
stations_df = pd.DataFrame(data)

# Create scatter plot on Mapbox
# mapbox_style="open-street-map", for color
fig = px.scatter_mapbox(stations_df, lat='x_1', lon='y_1',
                        mapbox_style="carto-positron", title='Train Rails and Stations')

# Add another scatter plot on Mapbox
fig.add_trace(go.Scattermapbox(
    lat=stations_df['x_2'],
    lon=stations_df['y_2'],
    mode='markers',
    name='Train 2'
))

fig.add_trace(go.Scattermapbox(
    lat=stations_df['x_2'],
    lon=stations_df['y_2'],
    mode='lines'
))

# Create Line plot
fig.add_trace(go.Scattermapbox(
    lat=stations_df['x_1'],
    lon=stations_df['y_1'],
    mode='lines',
    name='Train 1'
))

# Display the plot
fig.show()