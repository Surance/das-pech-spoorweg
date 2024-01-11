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
    for row in connection_data_df.iterrows():
        connection.Connection(row['station1'], row['station2'], row['distance'])

def create_station(station_data_df):
    for row in station_data_df.iterrows():
        station.Station(row['station'], row['x'], row['y'])
        
def output(input):
    for traject in
    trajects = trajectMain.traject.connections_traject()
    time = trajectMain.traject.track_traject_time()


station_data = get_station_data("StationsHolland.csv")
connection_data = get_connection_data("ConnectionsHolland.csv")