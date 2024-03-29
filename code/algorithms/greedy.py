from collections import OrderedDict
from code.classes.schedule import Schedule
from code.classes.connection import Connection

class GreedySchedule:
    """
    Generates a schedule using a greedy algorithm. 

    The algorithm initializes trains and fills them with connections until all stations are ridden or constraints are met.
    The choice of the next connection is greedy, based on a score calculated considering distance, the number of possible
    future connections, and the number of times it has already been ridden.
    """

    def __init__(self, schedule: Schedule) -> None:
        """
        Initializes the GreedySchedule object.

        Parameters:
            schedule (Schedule): The schedule object to be filled with connections.
        """
        self.schedule = schedule
        self.connections_score = {}

        # The amount added to the connection score once it has been ridden
        self.ridden_score = 100

    def check_all_possible_connections(self) -> dict[Connection, list]:
        """
        Function creates a dictionary with each connection as key and a list of its possible connections as value.

        Returns:
            dict[Connection, list]: A dictionary containing each connection and its possible next connections.
      
        """
        total_possible_connections = {}

        for connection_1 in self.schedule.total_connections:
            connections_list = []

            # Loop over connections again to find each connections possible next connection
            for connection_2 in self.schedule.total_connections:
                
                # Append to list if either of the arrival or departure stations for connection 1 and 2 are the same
                if connection_1.arrival_station == connection_2.arrival_station or \
                   connection_1.departure_station == connection_2.departure_station or \
                   connection_1.arrival_station == connection_2.departure_station or \
                   connection_1.departure_station == connection_2.arrival_station:
                    connections_list.append(connection_2)
            
            # Add list of connection and its possible nect connections to dict 
            total_possible_connections[connection_1] = connections_list

        return total_possible_connections

    def greedy_score(self) -> None:
        """
        Function calculates a score for each connection based on its distance, the number of times already ridden,
        and the number of possible next connections.
        """
        all_possible_connections = self.check_all_possible_connections()

        # Calculate connection score for each connection
        for current_connection in self.schedule.total_connections:
            self.connections_score[current_connection] = current_connection.travel_time + len(all_possible_connections[current_connection])
    
    def find_best_score(self, possible_connections: dict) -> Connection:
        """
        Function finds the connection of possible connections with the lowest score and returns that connection. 

        Args:
            possible_connections (dict): A dictionary of possible connections.

        Returns:
            Connection: The connection with the lowest score.
        
        """
        least_score = float('inf')
        # Check which of the possible connections has the least next possible connections
        for possible_connection in possible_connections.keys():
            current_score = self.connections_score[possible_connection]

            if current_score < least_score:
                least_score = current_score
                connection_with_least = possible_connection

        return connection_with_least
    
    def fill_train(self) -> None:
        """
        Function fills initialised train until all connections are ridden. If train time is about to go over maximum time, end train.
        """ 
        # Fill until schedule rides all connections 
        while len(self.schedule.ridden) < len(self.schedule.total_connections):
            
            # Create dictionary of possible next onnections for current station
            current_possible_connections = self.schedule.check_possible_connections()

            # End train if there are no possible connections 
            if len(current_possible_connections.keys()) == 0:
                break
            
            # Get connections with best score 
            connection_with_least = self.find_best_score(current_possible_connections)

            # Dont add connection to train if it overrides max time 
            if self.schedule.current_time + connection_with_least.travel_time > self.schedule.max_time:
                break 
            
            # Add best connection to train
            self.schedule.valid_connection(connection_with_least, current_possible_connections[connection_with_least])

            # Add ridden score to the connections score once it has been ridden
            self.connections_score[connection_with_least] += self.ridden_score

    def get_first_train_connection(self) -> Connection:
        """
        Function gets the first connection in the train by finding the connection with the best score that has not been ridden yet. 

        Returns: 
            Connection: The connection with the best score that has not yet been ridden.
        """
        # Take connection with least score as first station
        first_train_connection = self.find_best_score(self.connections_score)

        # Take next best connection if connection has already been ridden
        i = 0
        for trial in range(self.schedule.max_trains):
            if first_train_connection in self.schedule.ridden:
                ordered_dict = OrderedDict(sorted(self.connections_score.items(), key=lambda x: x[1]))
                first_train_connection, _ = list(ordered_dict.items())[i]
                i += 1

        return first_train_connection

    def create_greedy_schedule(self) -> Schedule:
        """
        Function creates a greedy schedule by filling schedule with trains built on connections through greedy choices.

        Returns:
            Schedule: The schedule object with the generated greedy schedule.
        """
        # Initialise greedy scores for all connections
        self.greedy_score()

        first_connections = []

        while len(self.schedule.ridden) < len(self.schedule.total_connections):
            first_train_connection = self.get_first_train_connection()
            
            # Add first station to train
            self.schedule.add_train(first_connection=first_train_connection)
            first_connections.append(first_train_connection)
            
            # Add ridden score for first station
            self.connections_score[first_train_connection] += self.ridden_score

            # Fill the train with connections by greedy choices
            self.fill_train()

            # Add current time to train time and add train to schedule
            self.schedule.train.total_time += self.schedule.current_time
            self.schedule.trains.append(self.schedule.train)

            # Break out of loop once the max number of trains has been met
            if len(self.schedule.trains) >= self.schedule.max_trains:
                break

        return self.schedule