from code.classes.train import Train
from code.classes.schedule import Schedule
from code.classes.connection import Connection

class Greedyschedule:
    def __init__(self, schedule):
        self.schedule = schedule

    def create_greedy_schedule(self):
        self.schedule.add_train()  # Add the first train

        while len(self.schedule.trains) < self.schedule.max_trains:
            train = self.schedule.trains[-1]  # Get the last added train
            possible_connections = self.schedule.check_possible_connections()

            if not possible_connections:
                # No more possible connections for the current train, add a new train
                self.schedule.add_train()
                continue

            # Sort connections by distance in ascending order (greedy choice)
            sorted_connections = sorted(possible_connections.keys(), key=lambda x: x.distance)

            # Select the first (shortest) connection
            selected_connection = sorted_connections[0]
            next_station = possible_connections[selected_connection]

            # Check if adding the connection violates the time constraint
            if train.total_time + selected_connection.travel_time <= self.schedule.max_time:
                # Add the connection and station to the train's schedule
                self.schedule.valid_connection(selected_connection, next_station)
            else:
                # Adding the connection would exceed the time constraint, add a new train
                self.schedule.add_train()

        return self.schedule