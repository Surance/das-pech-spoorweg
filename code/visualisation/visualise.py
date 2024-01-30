import matplotlib.pyplot as plt
import pandas as pd

coords_data= pd.read_csv("data/StationsNationaal.csv")

def get_coordinates(station_data: str, station_list: list) -> list:
    """
    Extracts coordinates for station names from station data.

    Parameters:
        station_data (str): A string containing station data in the format "station,y,x".
        station_list (list): A list of station names for which coordinates need to be extracted.

    Returns:
        list: A list of tuples containing (y, x) coordinates corresponding to the station names.
    """
    coordinates = []

    for station_name in station_list:
            station_info = station_data[station_data['station'] == station_name]
            if not station_info.empty:
                coordinates.append((station_info.iloc[0]['y'], station_info.iloc[0]['x']))

    return coordinates

def process_input(input_list: list) -> list:
    """
    Process a list of train routes and clean the data.

    Parameters:
        input_list (list): A list of train routes, where each route is represented
        as a list of stations.

    Returns:
        list: A list of tuples containing cleaned train data, where each tuple
        consists of a train name and a list of cleaned stations.
    """
    train_data = []
    
     # Iterate over the input_list with enumeration to get index and route
    for i, route in enumerate(input_list, start=1):
        train_name = f"Train {i}"
        
        # Remove leading/trailing whitespaces from each station in the route
        cleaned_route = [station.strip() for station in route]  

        # Append a tuple containing train name and cleaned route to train_data
        train_data.append((train_name, cleaned_route))

    return train_data

def plot_trains(station_data: str, train_data: list, figure_size: tuple[int, int]=(10, 8)) -> None:
    """
    Plots rails and stations for multiple trains.

    Parameters:
        station_data (str): A string containing station data in the format "station,y,x".
        train_data (list): A list of tuples where each tuple contains a train name and a list of station names.
    """

    # Create a new figure with the specified size
    plt.figure(figsize=figure_size)

    # colors = ['yellow', 'pink', 'yellowgreen', 'lightblue', 'purple', 'darkgreen', 'darkblue']
    # linewidths = [10, 8.5, 7, 5.5, 4, 2.5, 1]
    colors = ['yellow', 'pink', 'yellowgreen', 'lightblue', 'purple', 'darkgreen', 'darkblue', 'red', 'orange', 'coral', 'blue', 'cyan', 'magenta', 'violet', 'indigo', 'olive', 'brown', 'wheat', 'gray', 'black']
    linewidths = [15.0, 14.25, 13.5, 12.75, 12.0, 11.25, 10.5, 9.75, 9.0, 8.25, 7.5, 6.75, 6.0, 5.25, 4.5, 3.75, 3.0, 2.25, 1.5, 0.75]



    for i, (train_name, station_list) in enumerate (train_data):
        result = get_coordinates(station_data, station_list)
        y_coords, x_coords = zip(*result)

        # Get the corresponding color, linewidth and zorder
        color = colors[i % len(colors)]
        linewidth = linewidths [i % len(linewidths)]

        # Using zorder to create a plotting order and plotting the thicker lines first
        zorder = i

        # Plot the rails
        plt.plot(x_coords, y_coords, label=f"{train_name} Route", color = color, zorder = zorder, linewidth= linewidth)

        # Plot the train stations
        plt.scatter(x_coords, y_coords, s=50)

        # Plot station names
        for i, station_name in enumerate(station_list):
            plt.text(x_coords[i], y_coords[i], station_name, rotation=20, rotation_mode='anchor', fontsize=5, ha='left', va='bottom', zorder=zorder + 1)

    plt.title("Train Rails and Stations")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.legend()
    plt.show()

