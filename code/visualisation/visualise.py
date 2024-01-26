import matplotlib.pyplot as plt

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
        
        # Iterate through each line in the station data (without the header)
        for line in station_data.split('\n')[1:]:
            parts = line.split(',')

            # Append coordinates to the result list
            if station_name == parts[0]:
                coordinates.append((float(parts[1]), float(parts[2])))

    return coordinates

def process_input(input_list: list) -> list:
    """
    Process a list of train routes and clean the data.

    Args:
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

    colors = ['yellow', 'pink', 'yellowgreen', 'lightblue', 'purple', 'darkgreen', 'darkblue']
    linewidths = [10, 8.5, 7, 5.5, 4, 2.5, 1]

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
            plt.text(x_coords[i], y_coords[i], station_name, rotation=20, rotation_mode='anchor', fontsize=8, ha='left', va='bottom')

    plt.title("Train Rails and Stations")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.legend()
    plt.show()

coords_data = """station,y,x
Alkmaar,52.63777924,4.739722252
Alphen a/d Rijn,52.12444305,4.657777786
Amsterdam Amstel,52.34666824,4.917778015
Amsterdam Centraal,52.37888718,4.900277615
Amsterdam Sloterdijk,52.38888931,4.837777615
Amsterdam Zuid,52.338889,4.872356
Beverwijk,52.47833252,4.656666756
Castricum,52.54583359,4.658611298
Delft,52.00666809,4.356389046
Den Haag Centraal,52.08027649,4.324999809
Den Helder,52.95527649,4.761111259
Dordrecht,51.80722046,4.66833353
Gouda,52.01750183,4.704444408
Haarlem,52.38777924,4.638333321
Heemstede-Aerdenhout,52.35916519,4.606666565
Hoorn,52.64472198,5.055555344
Leiden Centraal,52.16611099,4.481666565
Rotterdam Alexander,51.95194626,4.553611279
Rotterdam Centraal,51.92499924,4.46888876
Schiedam Centrum,51.92124381,4.408993721
Schiphol Airport,52.30944443,4.761944294
Zaandam,52.43888855,4.813611031"""
