# Das Pech, Spoorweg
import station
import connection
import trajectMain
import pandas as pd

def get_station_data(input_file):
    """
    Function that creates a pd dataframe from csv file with station info and coordinates
    """
    station_data_df = pd.read_csv(input_file)
    return station_data_df

def get_connection_data(input_file):
    """
    Function that creates a pd dataframe from csv file with connection info and time
    """
    connection_data_df = pd.read_csv(input_file)
    return connection_data_df

def create_connection(connection_data_df):
    connections_list = []
    for _, row in connection_data_df.iterrows():
       connections_list.append(connection.Connection(row['station1'], row['station2'], row['distance']))
    return connections_list

def create_station(station_data_df):
    stations_list = []
    for _, row in station_data_df.iterrows():
        stations_list.append(station.Station(row['station'], row['x'], row['y']))
    return stations_list


def calculate_quality(bereden, trajects):
    p = bereden / len(trajects)
    T = len(trajects)
    Min = sum([traject.total_time for traject in trajects])
    K = p * 10000 - (T * 100 + Min)
    return K

def create_schedule(stations, connections, max_trajects, max_time):
    trajects = []
    bereden = 0

    while bereden < len(connections):
        traject_name = f"train_{len(trajects) + 1}"
        traject = Traject(traject_name)
        current_time = 0

        while current_time < max_time and bereden < len(connections):
            connection = random.choice(connections)
            if connection.departure_station in traject.stations or connection.arrival_station in traject.stations:
                continue

            traject.connections.append(connection)
            traject.stations.extend([connection.departure_station, connection.arrival_station])
            current_time += connection.travel_time
            bereden += 1

        traject.total_time = current_time
        trajects.append(traject)

        if len(trajects) >= max_trajects:
            break

    return trajects

def output_schedule(trajects):
    for traject in trajects:
        stations = ', '.join(traject.stations)
        print(f"{traject.name},\"[{stations}]\"")
    score = calculate_quality(len(trajects), trajects)
    print(f"score,{score}")

# Input files
station_data = get_station_data("StationsHolland.csv")
connection_data = get_connection_data("ConnectionsHolland.csv")

# Create objects
stations = create_station_objects(station_data)
connections = create_connection_objects(connection_data)

# Create schedule
max_trajects = 7
max_time = 120  # 2 hours
schedule = create_schedule(stations, connections, max_trajects, max_time)

# Output schedule
output_schedule(schedule)

def output(trajects):
    for traject in trajects:
        traject_names = traject.traject_stations()
        connections = traject.connections_traject()
        time = traject.track_traject_time()




station_data = get_station_data("StationsHolland.csv")
connection_data = get_connection_data("ConnectionsHolland.csv")



