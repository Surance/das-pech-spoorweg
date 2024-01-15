from code.classes.station import Station
from code.classes.connection import Connection
from code.classes.schedule import Schedule
import os
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
    """
    Function takes dataframe and creates list of connections
    """
    connections_list = []
    for _, row in connection_data_df.iterrows():
       connections_list.append(Connection(row['station1'], row['station2'], row['distance']))
    return connections_list

def create_station(station_data_df):
    """
    Function takes dataframe and creates list of stations 
    """
    stations_list = []
    for _, row in station_data_df.iterrows():
        stations_list.append(Station(row['station'], row['x'], row['y']))
    return stations_list

if __name__ == "__main__":
    # Input csv's
    station_data = get_station_data("data/StationsHolland.csv")
    connection_data = get_connection_data("data/ConnectionsHolland.csv")

    # Create objects
    all_stations = create_station(station_data)
    all_connections = create_connection(connection_data)

    # Create schedule & display in output
    max_trajects = 7
    max_time = 120  # 2 hours
    schedule = Schedule(max_trajects, max_time, all_connections)

    stations_trajects = schedule.create_schedule()
    schedule.display_schedule()