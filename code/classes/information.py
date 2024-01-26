from .station import Station
from .connection import Connection

import pandas as pd
import csv
import os

class Information:
    def __init__(self, station_data: csv, connection_data: csv) -> None:
        
        self.station_data_df = pd.read_csv(station_data)
        self.connection_data_df = pd.read_csv(connection_data)

    def create_connection(self) -> list:
        """
        Function takes dataframe and creates list of connections
        """
        connections_list = []
        for _, row in self.connection_data_df.iterrows():
            connections_list.append(Connection(row['station1'], row['station2'], row['distance']))

        return connections_list

    def create_station(self) -> list:
        """
        Function takes dataframe and creates list of stations 
        """
        stations_list = []
        for _, row in self.station_data_df.iterrows():
            stations_list.append(Station(row['station'], row['x'], row['y']))

        return stations_list
    
    def summary_experiment(self, algorithm: str, path: str, iterations: int, score: list, ridden: list) -> None:
        """
        Add file inside directory with all trials of experiment that shows information with summary of the experiment
        """
        file_name = f"{path}EXPERIMENT_SUMMARY"
        
        # Create folder if it doesn't exist
        os.makedirs(os.path.dirname(file_name), exist_ok=True)

        with open(file_name, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)

            csv_writer.writerow(["Algorithm type", algorithm])
            
            csv_writer.writerow(["Number of Trials", iterations])

            csv_writer.writerow(["Average Score", sum(score)/iterations])

            csv_writer.writerow(["Average Connections Ridden", sum(ridden)/iterations])

            csv_writer.writerow(["Maximum Score", max(score)])


