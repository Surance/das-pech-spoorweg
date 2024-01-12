import matplotlib.pyplot as plt
from main import stations_trajects

def get_coordinates(station_data, station_list):
    coordinates = []

    for station_name in station_list:
        for line in station_data.split('\n')[1:]:
            parts = line.split(',')

            if station_name == parts[0]:
                coordinates.append((float(parts[1]), float(parts[2])))

    return coordinates

def process_input(input_list):
    train_data = []

    for i, route in enumerate(input_list, start=1):
        train_name = f"Train {i}"
        cleaned_route = [station.strip() for station in route]  # Remove leading/trailing whitespaces

        train_data.append((train_name, cleaned_route))

    return train_data

def plot_trains(station_data, train_data, figure_size=(10, 8)):
    plt.figure(figsize=figure_size)

    for train_name, station_list in train_data:
        result = get_coordinates(station_data, station_list)
        y_coords, x_coords = zip(*result)

        plt.plot(x_coords, y_coords, label=f"{train_name} Route")
        plt.scatter(x_coords, y_coords)

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

input_list = stations_trajects

train_data = process_input(input_list)

plot_trains(coords_data, train_data)