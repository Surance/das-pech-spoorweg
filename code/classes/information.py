from .station import Station
from .connection import Connection

import pandas as pd
import csv

class Information:
    def __init__(self, station_data, connection_data):
        
        self.station_data_df = pd.read_csv(station_data)
        self.connection_data_df = pd.read_csv(connection_data)

    def create_connection(self):
        """
        Function takes dataframe and creates list of connections
        """
        connections_list = []
        for _, row in self.connection_data_df.iterrows():
            connections_list.append(Connection(row['station1'], row['station2'], row['distance']))

        return connections_list

    def create_station(self):
        """
        Function takes dataframe and creates list of stations 
        """
        stations_list = []
        for _, row in self.station_data_df.iterrows():
            stations_list.append(Station(row['station'], row['x'], row['y']))

        return stations_list
    
    def summary_experiment(self, algorithm, path, iterations, score, N_ridden):
        """
        Add file inside directory with all trials of experiment that shows information with summary of the experiment
        """
        file_name = f"{path}/EXPERIMENT_SUMMARY"

        with open(file_name, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)

            csv_writer.writerow(["Algorithm type", algorithm])
            
            csv_writer.writerow(["Number of Trials", iterations])

            csv_writer.writerow(["Average Score", score/iterations])

            csv_writer.writerow(["Average Connections Ridden", N_ridden/iterations])