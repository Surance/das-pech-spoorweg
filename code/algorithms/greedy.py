from code.classes.schedule import Schedule
from collections import OrderedDict
import random

class GreedySchedule:
    def __init__(self, schedule: Schedule) -> None:
        self.schedule = schedule

        self.possible_connections = {}

        self.connections_score = {}

        self.ridden_score = 100

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

        for current_connection in self.schedule.total_connections:
            self.connections_score[current_connection] = current_connection.travel_time + len(self.possible_connections[current_connection])

    def create_greedy_schedule(self):

        self.check_all_possible_connections()

        self.greedy_score()

        while len(self.schedule.ridden) < len(self.schedule.total_connections):
            # Take connection with least score as first station
            first_train_connection = min(self.connections_score.items(), key=lambda x: x[1])[0]
            
            # Add first station to train
            self.schedule.add_train(first_connection=first_train_connection)
            
            # Add ridden score for first station
            self.connections_score[first_train_connection] += self.ridden_score

            while self.schedule.current_time < self.schedule.max_time and len(self.schedule.ridden) < len(self.schedule.total_connections):
                # Check which connections are possible with the previous arrival station
                current_possible_connections = self.schedule.check_possible_connections()

                if len(current_possible_connections.keys()) == 0:
                    break
                    
                least_score = float('inf')
                # Check which of the possible connections has the least next possible connections
                for possible_connection in current_possible_connections.keys():
                    current_score = self.connections_score[possible_connection]
                    
                    if current_score < least_score:
                        least_score = current_score
                        connection_with_least = possible_connection
                
                self.schedule.valid_connection(connection_with_least, current_possible_connections[connection_with_least])

                self.connections_score[connection_with_least] += self.ridden_score

            self.schedule.train.total_time += self.schedule.current_time
            self.schedule.trains.append(self.schedule.train)

            # Break out of loop once the max number of trains has been met
            if len(self.schedule.trains) >= self.schedule.max_trains:
                break

        return self.schedule