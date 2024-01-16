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

    def valid_connection(self, connection, station_to_add):
        """
        Function adds connections and stations to list if it is a valid next connection
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
        # TODO: put create schedule into different seperate functions not one big 
        """
        Function  creates a schedule of trains, taking in account the connections and the max time
        """

        # Create a new train every iteration until all connections are passed 
        while len(self.ridden) < len(self.total_connections):
            # Start self.train somewhere randomly
            self.add_train()

            # Add stations to train if it connects to previous station until all connections are passed and max time is met
            # BUG: Change to: look at possible connections and choose a random one
            while self.current_time < self.max_time and len(self.ridden) < len(self.total_connections):
                connection = random.choice(self.total_connections)
                departure_station = connection.departure_station
                arrival_station = connection.arrival_station

                # BUG: sorry ff heel lelijk maar anders blijft ie hangen
                if self.train.stations_names_list[-1] == "Den Helder":
                    break

                # Only add new connection to train if connection is possible with previous station
                if self.train.stations_names_list[-1] == arrival_station and self.train.stations_names_list[-2] != departure_station: 
                    # TODO: create into function
                    self.valid_connection(connection, departure_station)
                
                # Only add new connection to train if connection is possible with previous station
                elif self.train.stations_names_list[-1] == departure_station: 
                    self.valid_connection(connection, arrival_station)

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