from code.classes.connection import Connection
from code.classes.schedule import Schedule
from collections import OrderedDict
import random

class Greedy2Schedule:
    def __init__(self, schedule: Schedule) -> None:
        self.schedule = schedule

        self.possible_connections = {}

        self.connections_score = {}

    def check_all_possible_connections(self):
        # TODO: check if there is a nicer way to do this cause this is hideous
        
        for connection_1 in self.schedule.total_connections:
            
            connections_list = []
    
            for connection_2 in self.schedule.total_connections:
                if connection_1.arrival_station == connection_2.arrival_station:
                    connections_list.append(connection_2)
                
                elif connection_1.departure_station == connection_2.departure_station:
                    connections_list.append(connection_2)
                
                elif connection_1.arrival_station == connection_2.departure_station:
                    connections_list.append(connection_2)
                
                elif connection_1.departure_station == connection_2.arrival_station:
                    connections_list.append(connection_2)
            
            self.possible_connections[connection_1] = connections_list

        return OrderedDict(sorted(self.possible_connections.items(), key=lambda x: len(x[1])))

    def greedy_score(self):
        """
        Take into account:
        - distance
        - amount of times already ridden
        - number of possible next connections
        """

        for connection in self.schedule.total_connections:
            self.connections_score[connection] = connection.travel_time + len(self.possible_connections[connection])

    def create_greedy_schedule(self):
        sorted_possible_connections = self.check_all_possible_connections()

        self.greedy_score()

        # Take the stations with the least connections as starting stations
        first_connections = list(sorted_possible_connections.keys())[:7]
        i = 0

        while len(self.schedule.ridden) < len(self.schedule.total_connections):
            first_train_connection = first_connections[i]
            
            # Add first stations from the set of randomly chosen stations
            self.schedule.add_train(first_connection=first_train_connection)

            while self.schedule.current_time < self.schedule.max_time and len(self.schedule.ridden) < len(self.schedule.total_connections):
                # Check which connections are possible with the previous arrival station
                current_possible_connections = self.schedule.check_possible_connections()

                if len(current_possible_connections.keys()) == 0:
                    break
                    
                least_score = 100
                # Check which of the possible connections has the least next possible connections
                for possible_connection in current_possible_connections.keys():
                    current_score = self.connections_score[possible_connection]
                    
                    if current_score < least_score:
                        least_score = current_score
                        connection_with_least = possible_connection
                
                print("current_possible_connections:", current_possible_connections)
                print("connection_with_least:", connection_with_least)

                self.schedule.valid_connection(connection_with_least, current_possible_connections[connection_with_least])
                
                # Set double current score when already ridden
                score = self.connections_score[connection_with_least]
                print("connection score:", score)
                print("")

                # TODO: check with jacob/luka cause this part is weird
                self.connections_score[connection_with_least] = score + 40

            self.schedule.train.total_time += self.schedule.current_time
            self.schedule.trains.append(self.schedule.train)

            # For the next train, take the next one out of the list of first stations 
            i+=1

            # Break out of loop once the max number of trains has been met
            if len(self.schedule.trains) >= self.schedule.max_trains:
                break

        return self.schedule