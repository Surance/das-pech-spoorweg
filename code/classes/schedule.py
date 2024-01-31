from code.classes.connection import Connection
from code.classes.station import Station
from .train import Train
from ..functions.quality import calculate_quality
from typing import Union
from typing_extensions import Self

import random
import os
import csv

class Schedule:
    """
    Represents a schedule of multiple trains

    Attributes:
        max_trains (int): The maximum number of trains allowed in the schedule.
        max_time (int): The maximum time allowed for the schedule.
        total_connections (List[Connection]): The list of all important connections in the Netherlands.
        current_time (int): The current time in the schedule takes with the trains it has
        trains (List[Train]): The list of trains that make up the schedule.
        ridden (set): A set of connections that have been ridden by the trains.
    """

    def __init__(self, max_trains: int, max_time: int, total_connections: list) -> None:
        """
        Initializes a new Schedule object with the provided maximum number of trains, maximum time, and total connections.

        Args:
            max_trains (int): The maximum number of trains allowed in the schedule.
            max_time (int): The maximum time allowed for the schedule.
            total_connections (List[Connection]): The list of all possible connections in the network.
        """
        self.max_trains = max_trains 
        self.max_time = max_time
        self.total_connections = total_connections
        self.current_time = 0
        
        # Store train classes in list
        self.trains = []

        # Keep track of ridden connections for all trains
        self.ridden = set()

    def copy_schedule(self) -> 'Schedule':
        """
        Function creates a copy of the current schedule and all objects inside.
        
        Returns:
            Schedule: A copy of the current schedule.
        """
        new_schedule = Schedule(self.max_trains, self.max_time, self.total_connections)
        new_schedule.trains = [train.copy_train() for train in self.trains]
        new_schedule.ridden = self.ridden.copy()
        new_schedule.current_time = self.current_time
        
        return new_schedule
    
    def check_possible_connections(self) -> dict[Connection, str]:
        """
        Function checks which connections are possible and adds to dictionary
        
        Returns:
            dict[Connection, str]: A dictionary of valid connections with the corresponding station name
        """
        possible_connections = {}
    
        for connection_to_check in self.total_connections:
            if self.train.stations_names_list[-1] == connection_to_check.arrival_station and self.train.stations_names_list[-2] != connection_to_check.departure_station: 
                possible_connections[connection_to_check] = connection_to_check.departure_station
        
            elif self.train.stations_names_list[-1] == connection_to_check.departure_station:
                possible_connections[connection_to_check] = connection_to_check.arrival_station
        
        return possible_connections
                         
    def valid_connection(self, connection: Connection, station_to_add: Station) -> None:
        """
        Function adds connections and stations to list and increases the time according to new connections time 

        Args:
            connection (Connection): The connection to add to the train in the schedule
            station_to_add (Station): The station to add to the train in the schedule
        """
        self.train.connections_list.append(connection)
        self.train.stations_names_list.append(station_to_add)
        self.current_time += connection.travel_time
                    
        self.ridden.add(connection)

    def add_train(self, first_connection: Union[None, Connection]=None) -> None:
        """
        Function adds a new train to the list of trains, picking a random connection if none is provided.

        Args:
            first_connection (Union[None, Connection]): The first connection for the new train, picked randomly if not provided.
        """
        if first_connection == None:
            first_connection = random.choice(self.total_connections)
        
        train_name = f"train_{len(self.trains) + 1}"
        self.train = Train(train_name)
        self.train.stations_names_list.append(first_connection.departure_station)
        self.train.stations_names_list.append(first_connection.arrival_station)
        self.current_time = 0

    def rename_trains(self) -> None:
        """
        Function renames trains in schedule so that they are in ascending order again
        """
        for count, train in enumerate(self.trains): 
            train.train_name = f"train_{count + 1}"

    def save_outputs_csv(self, file_name: str, score: float) -> None:
        """
        Function saves each result per trial as a csv in the experiment folder
        
        Args:
            file_name (str): The path and name of the file to save.
            score (float): The score of the schedule.
        """
        with open(file_name, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            
            # Write headers
            csv_writer.writerow(["train", "stations"])

            # Write data
            for train in self.trains:
                csv_writer.writerow([train.train_name, train.stations_names_list])

            # Write score
            csv_writer.writerow(["Score", score])

            # Write connection information
            csv_writer.writerow(["Connections Ridden", len(self.ridden)])
            csv_writer.writerow(["Total Connections", len(self.total_connections)])

    def display_schedule(self, file_name: str, save_each_output_as_csv: bool=False) -> tuple[list, float, int]:
        """
        Function displays the schedule and score in the appropriate format
        
        Args:
            file_name (str): The path and name of the file to save.
            save_each_output_as_csv (bool): Whether to save each individual result as a CSV file in experiment folder. 

        Returns:
            tuple: A tuple containing a list of stations per train, the score, and the number of connections ridden.
        """

        # Create list of stations in schedules trains
        stations_per_train = [train.stations_names_list for train in self.trains]
                    
        # Compute score for created train schedule
        score = calculate_quality(self.ridden, self.trains, self.total_connections)

        # Create folder if it doesn't exist
        os.makedirs(os.path.dirname(file_name), exist_ok=True)

        # Save each result of each trial in a CSV file if asked for
        if save_each_output_as_csv == True:
            self.save_outputs_csv(file_name, score)

        return stations_per_train, score, len(self.ridden)