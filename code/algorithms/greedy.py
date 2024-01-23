from code.classes.connection import Connection

class GreedySchedule:
    def __init__(self, schedule):
        self.schedule = schedule

    def create_greedy_schedule(self, max_iterations=1000):
        i = 1
        all_stations = set(connection.departure_station for connection in self.schedule.total_connections) | set(connection.arrival_station for connection in self.schedule.total_connections)

        while len(self.schedule.ridden) < len(self.schedule.total_connections) and i <= max_iterations:
            # Add random first train
            self.schedule.add_train()

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

            i += 1

        return self.schedule.trains, self.schedule.ridden
