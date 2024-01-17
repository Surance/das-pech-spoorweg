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
        
        # Store self.train classes in list
        self.trains = []

        # Keep track of ridden connections for all trains
        self.ridden = set()
    
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

    def add_train(self):
        """
        Adds a new train to the list of trains
        """
        first_connection = random.choice(self.total_connections)
        train_name = f"train_{len(self.trains) + 1}"
        self.train = Train(train_name)
        self.train.stations_names_list.append(first_connection.departure_station)
        self.train.stations_names_list.append(first_connection.arrival_station)
        self.current_time = 0

    def create_schedule(self):
        # TODO: put create schedule as seperate class --> its a random algorithm
        """
        Function  creates a schedule of trains, taking in account the connections and the max time
        """

        # Create a new train every iteration until all connections are passed 
        while len(self.ridden) < len(self.total_connections):
            # Start self.train somewhere randomly
            self.add_train()

            # Add new stations to train if it connects to previous station until all connections are passed or max time is met
            while self.current_time < self.max_time and len(self.ridden) < len(self.total_connections):
                
                # Check which connections are possible with the previous arrival station
                possible_connections = self.check_possible_connections()

                if len(possible_connections.keys()) == 0:
                    break
                
                # Pick a random connection from those that are possible
                connection = random.choice(list(possible_connections.keys()))

                self.valid_connection(connection, possible_connections[connection])

            self.train.total_time += self.current_time
            self.trains.append(self.train)
            
            # Break out of loop once the max number of trains has been met
            if len(self.trains) >= self.max_trains:
                break

        return self.trains, self.ridden

    def display_schedule(self, algorithm_type, experiment_number, save_each_output_as_csv=False):
        """
        Displays the schedule and score in the format as provided on ah.proglab.nl
        """
        file_name = f"experiment/{algorithm_type}/experiment_{experiment_number + 1}"

        stations_per_train = []
        for train in self.trains:
            stations = train.stations_names_list
            stations_per_train.append(stations)
                    
        # Compute score for created train schedule
        score = Quality(self.ridden, self.trains, self.total_connections).calculate_quality()

        # Create folder if it doesn't exist
        os.makedirs(os.path.dirname(file_name), exist_ok=True)

        # Save each result of each trial in a CSV file if asked for
        # TODO: put the following section in seperate function
        if save_each_output_as_csv == True:

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

        return stations_per_train, score, len(self.ridden)