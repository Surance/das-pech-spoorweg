from .train import Train
from .quality import Quality

import random
import os
import csv

class Schedule:
    def __init__(self, max_trains, max_time, total_connections):
        self.max_trains = max_trains 
        self.max_time = max_time
        self.total_connections = total_connections
        
        # Store train classes in list
        self.trains = []

        # Keep track of ridden connections for all trains
        self.ridden = set()

    def copy_schedule(self):
        """
        Create a copy of the current schedule.
        """
        new_schedule = Schedule(self.max_trains, self.max_time, self.total_connections)
        new_schedule.trains = [train.copy_train() for train in self.trains]
        new_schedule.ridden = self.ridden.copy()
        new_schedule.current_time = self.current_time
        return new_schedule
    
    def check_possible_connections(self):
        """
        Function checks which connections are possible and returns list of valid connecctions
        """
        possible_connections = {}
        for connection_to_check in self.total_connections:
            if self.train.stations_names_list[-1] == connection_to_check.arrival_station and self.train.stations_names_list[-2] != connection_to_check.departure_station: 
                possible_connections[connection_to_check] = connection_to_check.departure_station
        
            elif self.train.stations_names_list[-1] == connection_to_check.departure_station:
                possible_connections[connection_to_check] = connection_to_check.arrival_station
        
        return possible_connections
                         
    def valid_connection(self, connection, station_to_add):
        """
        Function adds connections and stations to list
        """
        self.train.connections_list.append(connection)
        self.train.stations_names_list.append(station_to_add)
        self.current_time += connection.travel_time
                    
        self.ridden.add(connection)

    def add_train(self, first_connection=None):
        """
        Adds a new train to the list of trains
        """
        if first_connection == None:
            first_connection = random.choice(self.total_connections)
        
        train_name = f"train_{len(self.trains) + 1}"
        self.train = Train(train_name)
        self.train.stations_names_list.append(first_connection.departure_station)
        self.train.stations_names_list.append(first_connection.arrival_station)
        self.current_time = 0

    def save_outputs_csv(self, file_name, score):
        """
        Function saves each output per trial as a csv in the experiment folder
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

    def display_schedule(self, file_name, save_each_output_as_csv=False):
        """
        Displays the schedule and score in the format as provided on ah.proglab.nl
        """

        stations_per_train = []
        for train in self.trains:
            stations = train.stations_names_list
            stations_per_train.append(stations)
                    
        # Compute score for created train schedule
        score = Quality(self.ridden, self.trains, self.total_connections).calculate_quality()

        # Create folder if it doesn't exist
        os.makedirs(os.path.dirname(file_name), exist_ok=True)

        # Save each result of each trial in a CSV file if asked for
        if save_each_output_as_csv == True:
            self.save_outputs_csv(file_name, score)

        return stations_per_train, score, len(self.ridden)