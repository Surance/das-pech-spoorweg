# Das Pech, Spoorweg
import station
import connection
import trajectMain
import pandas as pd

def get_station_data(input_file):
    station_data_df = pd.read_csv(input_file)
    return station_data_df

def get_connection_data(input_file):
    connection_data_df = pd.read_csv(input_file)
    return connection_data_df

def output(input):
    pass

station_data = get_station_data("StationsHolland.csv")
connection_data = get_connection_data("ConnectionsHolland.csv")

stations = [station(**data) for data in station_data]
connections = [connection(**data) for data in connection_data]

for station in stations:
    print(station.StationInfo)

for connection in connections:
    print(connection.StationInfo)

