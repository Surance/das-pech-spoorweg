from code.classes.connection import Connection
import random

class GreedySchedule:
    def __init__(self, schedule):
        self.schedule = schedule


    def create_greedy_schedule(self) -> tuple(list, set):
        """
        Function creates a schedule using greedy choice
        Returns a list of the trains in the greedy schedule and a set of the connections the schedule rides 
        """
        first_stations = set()
        # Create set of max train number of stops to be the randomly chosen first stop for each train
        while len(first_stations) < self.max_trains:
            first_stations.add(random.choice(self.total_connections))
        
        i = 0

        first_stations = list(first_stations)

        while len(self.ridden) < len(self.total_connections):
            
            first_station = first_stations[i]
            
            # Add first stations from the set of randomly chosen stations
            self.add_train(first_connection=first_station)

            while self.current_time < self.max_time and len(self.ridden) < len(self.total_connections):
                # Check which connections are possible with the previous arrival station
                possible_connections = self.check_possible_connections()

                if len(possible_connections.keys()) == 0:
                    break

                # Sort connections by distance in ascending order (greedy choice)
                sorted_connections = sorted(possible_connections.keys(), key=lambda x: x.travel_time)

                # Select the first (shortest) connection
                connection = sorted_connections[0]

                self.valid_connection(connection, possible_connections[connection])
            
            self.train.total_time += self.current_time
            self.trains.append(self.train)

            # For the next train, take the next one out of the list of first stations 
            i+=1

            # Break out of loop once the max number of trains has been met
            if len(self.trains) >= self.max_trains:
                
                break

        return self.trains, self.ridden
