# Das Pech, Spoorweg
import station
import connection
import random
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

def calculate_quality(ridden, trajects, all_connections):
    # TODO: make into behaviour class? so you dont loop over same list 3484583838 times 
    p = len(ridden) / len(all_connections)
    T = len(trajects)
    Min = sum([traject.total_time for traject in trajects])
    K = p * 10000 - (T * 100 + Min)
    return K

def create_schedule(stations, connections, max_trajects, max_time):
    """
    Function that creates a schedule of trains, taking in account the connections and the max time
    """
    trajects = []
    # Keep track of ridden connections for all trajects
    ridden_connections = []

    while len(ridden_connections) < len(connections):
        # Start traject somewhere randomly 
        previous_connection = random.choice(connections)
        traject_name = f"train_{len(trajects) + 1}"
        traject = trajectMain.Traject(traject_name)
        current_time = 0

        while current_time < max_time and len(ridden_connections) < len(connections):
            connection = random.choice(connections)
            departure_station = connection.departure_station
            arrival_station = connection.arrival_station
            
            # Only add new connection to traject if connection is possible with previous station
            # if departure_station == previous_connection.arrival_station or arrival_station == previous_connection.arrival_station or departure_station == previous_connection.departure_station or arrival_station == previous_connection.departure_station:
            traject.connections_list.append(connection)
            # BUG: will now add both departure and arrival station names to list of stations, meaning some stations will be 2x in a row
            traject.stations_names_list.extend([connection.departure_station, connection.arrival_station])
            current_time += connection.travel_time

            previous_connection = connection
            ridden_connections.append(connection)

        traject.total_time += current_time
        trajects.append(traject)
        
        if len(trajects) >= max_trajects:
            break

    return trajects, ridden_connections

def display_schedule(trajects, ridden, total_connections):
    """
    Displays the schedule and score in the format as provided on ah.proglab.nl
    """
    stations_per_traject = []
    for traject_connections in trajects:
        stations = traject_connections.stations_names_list
        stations_per_traject.append(stations)
        print(f"{traject_connections.traject_name},\"{stations}\"")
    score = calculate_quality(ridden, trajects, total_connections)
    print(f"score,{score}")

    return stations_per_traject

# Input csv's
station_data = get_station_data("StationsHolland.csv")
connection_data = get_connection_data("ConnectionsHolland.csv")

# Create objects
all_stations = create_station(station_data)
all_connections = create_connection(connection_data)

# Create schedule
max_trajects = 7
max_time = 120  # 2 hours
schedule, ridden_connections = create_schedule(all_stations, all_connections, max_trajects, max_time)

# Output schedule
stations_trajects = display_schedule(schedule, ridden_connections, all_connections)

station_data = get_station_data("StationsHolland.csv")
connection_data = get_connection_data("ConnectionsHolland.csv")