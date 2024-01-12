import matplotlib.pyplot as plt


def get_coordinates(station_data, station_list):
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

            if station_name== parts[0]:
                # Append coordinates to the result list
                coordinates.append((float(parts[1]), float(parts[2])))

    return coordinates

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

def plot_trains(station_data, train_data, figure_size=(10, 8)):
    """
    Plots rails and stations for multiple trains.

    Parameters:
        station_data (str): A string containing station data in the format "station,y,x".
        train_data (list): A list of tuples where each tuple contains a train name and a list of station names.

    Returns:
        A plot
    """
    # Create a new figure with the specified size
    plt.figure(figsize=figure_size)

    # Plot the rails and stations for each train
    for train_name, station_list in train_data:
        result = get_coordinates(station_data, station_list)
        y_coords, x_coords = zip(*result)

        # Plot the rails
        plt.plot(x_coords, y_coords, label=f"{train_name} Route")

        # Plot the train stations
        plt.scatter(x_coords, y_coords)

        # Plot station names
        for i, station_name in enumerate(station_list):
            plt.text(x_coords[i], y_coords[i], station_name, rotation = 20, rotation_mode='anchor', fontsize=8, ha='right', va='bottom')

    plt.title("Train Rails and Stations")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.legend()
    plt.show()

train_data = [
    ("Train 1", ["Beverwijk", "Castricum", "Alkmaar", "Hoorn", "Zaandam"]),
    ("Train 2", ["Amsterdam Sloterdijk", "Amsterdam Centraal", "Amsterdam Amstel", "Amsterdam Zuid", "Schiphol Airport"]),
    ("Train_3", ["Rotterdam Alexander", "Gouda", "Alphen a/d Rijn", "Leiden Centraal", "Schiphol Airport", "Amsterdam Zuid"])
]

plot_trains(coords_data, train_data)