import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import re

from .visualise import get_coordinates

coords_data= pd.read_csv("data/StationsNationaal.csv")

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

def create_map_plot(train_data: list, station_name: list, mapbox_style="carto-positron")-> None: 
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

    # colors = ['yellow', 'pink', 'yellowgreen', 'lightblue', 'purple', 'darkgreen', 'darkblue']
    # linewidths = [10, 8.5, 7, 5.5, 4, 2.5, 1]

    colors = ['yellow', 'pink', 'yellowgreen', 'lightblue', 'purple', 'darkgreen', 'darkblue', 'red', 'orange', 'green', 'blue', 'cyan', 'magenta', 'violet', 'indigo', 'turquoise', 'brown', 'wheat', 'gray', 'black']
    linewidths = [15.0, 14.25, 13.5, 12.75, 12.0, 11.25, 10.5, 9.75, 9.0, 8.25, 7.5, 6.75, 6.0, 5.25, 4.5, 3.75, 3.0, 2.25, 1.5, 0.75]


#     # Create a dataframe for each train and add it to the list
#    for i, (train, station_names_list) in enumerate(train_data, station_name, start=1):
#         train_df = pd.DataFrame(train, columns=['x', 'y'])

#         # Adding a column to identify the train
#         train_df['train'] = f'Train {i}'
#         print(station_names_list)
#         train_df['name'] = station_names_list
#         # train_df['name'] = station_name
#         train_dfs.append(train_df)
    
    # for i, (train, station_names_list) in enumerate(train_data, start=1):
    #     # Assuming x and y values are not provided, you can create dummy values or use station names as x and y
    #     train_df = pd.DataFrame({'name': station_names_list})
    #     train_df['x'] = train_df['name']
    #     train_df['y'] = train_df['name']
    #     train_df['train'] = f'Train {i}'
    #     train_dfs.append(train_df)

    # for i, ((train, station_names_list), station) in enumerate(zip(train_data, station_name), start=1):
    #     train_df = pd.DataFrame(train, columns=['x', 'y'])
    #     train_df['train'] = f'Train {i}'
    #     train_df['name'] = station_names_list


    # Create a dataframe for each train and add it to the list
    for i, train in enumerate(train_data, start=1):
        train_df = pd.DataFrame(train, columns=['x', 'y'])
        
        # Adding a column to identify the train
        train_df['train'] = f'Train {i}'
        train_dfs.append(train_df)

    # for station_names_list in enumerate(station_name):
    #         stations = station_names_list[1]
    #          train_df['name'] = stations

    # for (station_name, train), i in enumerate(zip(station_name, train_data), start=1):
    #     stations = station_name[1]  # Extracting stations from station_name tuple

    #     # Create DataFrame for each train
    #     train_df = pd.DataFrame(train, columns=['x', 'y'])

    #     # Adding columns to identify the train and stations
    #     train_df['station'] = stations
    #     train_df['train'] = f'Train {i}'

    #     train_dfs.append(train_df)  # Adding DataFrame to the list


    # Concatenate all dataframes into a single dataframe
    stations_df = pd.concat(train_dfs, ignore_index=True)

    # Create scatter plot on Mapbox
    fig = px.scatter_mapbox(stations_df, lat='x', lon='y',
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
    # Plot the train stations
    fig.add_trace(go.Scattermapbox(
        lat=stations_df['x'],
        lon=stations_df['y'],
        mode='markers',
        marker=dict(size=5, color='black'),  # Adjust marker size and color as needed
        name='Train Stations'  # Name for the train stations trace
    ))

    # Display the plot
    fig.show()