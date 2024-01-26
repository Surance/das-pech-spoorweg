import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import re

from .visualise import get_coordinates


def format_coordinates(train_data: list, station_data:str)-> list: 
    """
    Formats coordinates from station data based on train data.

    Parameters:
    train_data (list): List of dictionaries, each containing keys 'x' and 'y' for coordinates.
    station_data (str): A string containing station data in the format "station,y,x".

    Returns:
    List[Dict[str, List[float]]]: A list of dictionaries where each dictionary contains 'x' and 'y' keys corresponding to lists of x and y coordinates.
    """


    result_list = []

    for train_name, station_list in train_data:
        result = get_coordinates(station_data, station_list)
        x_coordinates, y_coordinates = zip(*result)

        # Convert coordinates to floats
        x_coordinates = [float(x) for x in x_coordinates]
        y_coordinates = [float(y) for y in y_coordinates]

        # Group x and y coordinates into a dictionary
        result_list.append({'x': x_coordinates, 'y': y_coordinates})

    return result_list

def create_map_plot(train_data: list, mapbox_style="carto-positron")-> None: 
    """
    Create a scatter plot on Mapbox for train rails and stations.

    Parameters:
        train_data (list): List of dictionaries, each containing keys 'x' and 'y' for coordinates.
        station_names (list): List of station names corresponding to the coordinates in train_data.
        mapbox_style (str): Style of the Mapbox map. Default is "carto-positron".

    Returns:
        A plot
    """
    # Create a list to store all the dataframes for each train
    train_dfs = []

    colors = ['yellow', 'pink', 'yellowgreen', 'lightblue', 'purple', 'darkgreen', 'darkblue']
    linewidths = [10, 8.5, 7, 5.5, 4, 2.5, 1]

    # Create a dataframe for each train and add it to the list
    for i, train in enumerate(train_data, start=1):
        train_df = pd.DataFrame(train, columns=['x', 'y'])

         # Adding a column to identify the train
        train_df['train'] = f'Train {i}'
        train_dfs.append(train_df)

    # Concatenate all dataframes into a single dataframe
    stations_df = pd.concat(train_dfs, ignore_index=True)

    # Create scatter plot on Mapbox
    fig = px.scatter_mapbox(stations_df, lat='x', lon='y', color='train', 
                            mapbox_style=mapbox_style, title='Train Rails and Stations')
    

    # Create separate Line plots for each train
    for i, train_df in enumerate(train_dfs, start=1):
        # Get the corresponding color and linewidth
        color = colors[i- 1]
        linewidth = linewidths [i - 1]

        fig.add_trace(go.Scattermapbox(
            lat=train_df['x'],
            lon=train_df['y'],
            mode='lines',
            line=dict(width=linewidth),
            line_color=color,

            # Use the train name as the trace name
            name=train_df['train'].iloc[0]
        ))

    # Display the plot
    fig.show()