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
    List[Dict[name, x, y]]]: A list of dictionaries where each dictionary contains 'stations' 'x' and 'y' keys containing the station names and coordinaets.
    """


    result_list = []

    for train_name, station_list in train_data:
        result = get_coordinates(station_data, station_list)
        x_coordinates, y_coordinates = zip(*result)

        # Convert coordinates to floats
        x_coordinates = [float(x) for x in x_coordinates]
        y_coordinates = [float(y) for y in y_coordinates]

        # Group x, y coordinates, and station name into a dictionary
        result_list.append({'station': station_list, 'x': x_coordinates, 'y': y_coordinates})

    return result_list

def create_map_plot(train_data: list,  coords_data:str , mapbox_style="carto-positron")-> None: 
    """
    Create a scatter plot on Mapbox for train rails and stations.

    Parameters:
        train_data (list): List of dictionaries, each containing keys 'x' and 'y' for coordinates.
        coords_data(str):A string containing station data in the format "station,y,x".
        mapbox_style (str): Style of the Mapbox map. Default is "carto-positron".

    Returns:
        A plot
    """
    # Create a list to store all the dataframes for each train
    train_dfs = []

    colors = ['yellow', 'pink', 'yellowgreen', 'lightblue', 'purple', 'darkgreen', 'darkblue', 'red', 'orange', 'coral', 'blue', 'cyan', 'magenta', 'violet', 'indigo', 'olive', 'brown', 'wheat', 'gray', 'black']
    linewidths = [15.0, 14.25, 13.5, 12.75, 12.0, 11.25, 10.5, 9.75, 9.0, 8.25, 7.5, 6.75, 6.0, 5.25, 4.5, 3.75, 3.0, 2.25, 1.5, 0.75]

    # Create a dataframe for each train and add it to the list
    for i, train in enumerate(train_data, start=1):
        train_df = pd.DataFrame(train, columns=['station','x', 'y'])
        
        # Adding a column to identify the train
        train_df['train'] = f'Train {i}'
        train_dfs.append(train_df)

    # Concatenate all dataframes into a single dataframe
    stations_df = pd.concat(train_dfs, ignore_index=True)

    # Create scatter plot on Mapbox
    fig = px.scatter_mapbox(coords_data, lat='y', lon='x', 
                            mapbox_style=mapbox_style, title='Train Rails and Stations')
    
    # Plot all stations that are not ridden in blue
    fig.add_trace(go.Scattermapbox(
        lat=coords_data['y'],
        lon=coords_data['x'],
        mode='markers',
        marker=dict(size=5, color='blue'),  
        name='Train Stations not ridden',  
        hoverinfo='text',  
        text=coords_data['station'] 
    ))
   
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


    # Plot the train stations that are ridden
    fig.add_trace(go.Scattermapbox(
        lat=stations_df['x'],
        lon=stations_df['y'],
        mode='markers',
        marker=dict(size=5, color='black'),  
        name='Train Stations',  
        hoverinfo='text',  
        text=stations_df['station'] 
    ))
        

    # Display the plot
    fig.show()