from .train import Train
from .quality import Quality
import random

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
        # TODO: put create schedule as seperate class --> its an algorithm
        """
        Function  creates a schedule of trains, taking in account the connections and the max time
        """

        # Create a new train every iteration until all connections are passed 
        while len(self.ridden) < len(self.total_connections):
            # Start self.train somewhere randomly
            self.add_train()

            # Add new stations to train if it connects to previous station until all connections are passed or max time is met
            while self.current_time < self.max_time and len(self.ridden) < len(self.total_connections):
        
                possible_connections = self.check_possible_connections()

                if len(possible_connections.keys()) == 0:
                    break

                connection = random.choice(list(possible_connections.keys()))

                self.valid_connection(connection, possible_connections[connection])

            self.train.total_time += self.current_time
            self.trains.append(self.train)
            
            # Break out of loop once the max number of trains has been met
            if len(self.trains) >= self.max_trains:
                break

        return self.trains, self.ridden

    def display_schedule(self):
        """
        Displays the schedule and score in the format as provided on ah.proglab.nl
        """
        stations_per_train = []
        for train_connections in self.trains:
            stations = train_connections.stations_names_list
            stations_per_train.append(stations)
            print(f"{train_connections.train_name},\"{stations}\"")
        
        score = Quality(self.ridden, self.trains, self.total_connections).calculate_quality()
        print(f"score,{score}")

        # To see if all connections have been passed:
        print(f"rode {len(self.ridden)} out of {len(self.total_connections)} connections")

        # TODO: save in csv - give title that tells settings (random/not random & heuristics)

        return stations_per_train