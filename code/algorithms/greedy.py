from code.classes.connection import Connection
from code.classes.schedule import Schedule
import random

class GreedySchedule:
    def __init__(self, schedule: Schedule) -> None:
        self.schedule = schedule

    def create_greedy_schedule(self) -> Schedule:
        """
        Function creates a schedule using greedy choice
        Returns a list of the trains in the greedy schedule and a set of the connections the schedule rides 
        """
        first_stations = set()
        
        # Create set of max train number of stops to be the randomly chosen first stop for each train
        while len(first_stations) < self.schedule.max_trains:
            first_stations.add(random.choice(self.schedule.total_connections))
        
        i = 0

        first_stations = list(first_stations)

        while len(self.schedule.ridden) < len(self.schedule.total_connections):
            
            first_station = first_stations[i]
            
            # Add first stations from the set of randomly chosen stations
            self.schedule.add_train(first_connection=first_station)

            while self.schedule.current_time < self.schedule.max_time and len(self.schedule.ridden) < len(self.schedule.total_connections):
                # Check which connections are possible with the previous arrival station
                possible_connections = self.schedule.check_possible_connections()

                if len(possible_connections.keys()) == 0:
                    break

                # Sort connections by distance in ascending order (greedy choice)
                sorted_connections = sorted(possible_connections.keys(), key=lambda x: x.travel_time)

                # Select the first (shortest) connection
                connection = sorted_connections[0]

                self.schedule.valid_connection(connection, possible_connections[connection])
            
            self.schedule.train.total_time += self.schedule.current_time
            self.schedule.trains.append(self.schedule.train)

            # For the next train, take the next one out of the list of first stations 
            i+=1

            # Break out of loop once the max number of trains has been met
            if len(self.schedule.trains) >= self.schedule.max_trains:
                break

        return self.schedule
