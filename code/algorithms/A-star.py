from code.classes.train import Train
from code.classes.schedule import Schedule
from code.classes.connection import Connection
import csv



class AStarScheduler:
    def __init__(self, max_trains, max_time, total_connections):
        self.max_trains = max_trains
        self.max_time = max_time
        self.total_connections = total_connections

        self.initial_state = ([], set())  # (stations, ridden_connections)
        self.goal_state = None  # Will be set during initialization

    def heuristic(self, state):
        # Estimate the cost to reach the goal from a given state
        remaining_connections = set(self.total_connections) - state[1]
        return len(remaining_connections)

    def cost(self, state, connection):
        # Evaluate the quality of a state (considering the total time spent)
        return state[0][-1].total_time + connection.travel_time

    def get_actions(self, state):
        # Get possible actions from a given state
        possible_connections = set()

        for connection_to_check in self.total_connections:
            if state[0] and state[0][-1].stations_names_list[-1] == connection_to_check.departure_station:
                possible_connections.add(connection_to_check)

        return possible_connections

    def a_star(self):
        self.goal_state = (None, set(self.total_connections))

        open_set = [(0, self.initial_state)]

        while open_set:
            open_set.sort(key=lambda x: x[0] + self.heuristic(x[1]))
            current_cost, current_state = open_set.pop(0)

            if current_state == self.goal_state:
                return current_state

            for action in self.get_actions(current_state):
                new_state = self.apply_action(current_state, action)
                new_cost = self.cost(current_state, action) + self.heuristic(new_state)

                if new_state not in open_set:
                    open_set.append((new_cost, new_state))

        return None

    def apply_action(self, state, connection):
        new_stations = state[0] + [connection.departure_station, connection.arrival_station]
        new_ridden = state[1] | {connection}
        new_train = Train(f"train_{len(new_stations) // 2}")
        new_train.stations_names_list = new_stations
        new_train.connections_list = state[0][-1].connections_list + [connection]
        new_train.total_time = sum(conn.travel_time for conn in new_train.connections_list)

        return new_stations, new_ridden

    def create_optimal_schedule(self):
        result = self.a_star()

        if result:
            stations, ridden_connections = result
            optimal_schedule = Schedule(self.max_trains, self.max_time, self.total_connections)
            optimal_schedule.trains.append(Train("Initial Train"))  # Add initial dummy train

            for i in range(1, len(stations), 2):
                connection = Connection(stations[i - 1], stations[i], 0)  # Assuming time is not important for the result
                optimal_schedule.valid_connection(connection, stations[i])

            return optimal_schedule

        return None


max_trains = 7
max_time = 120
file_path = 'data/ConnectionsHolland.csv'
connections = []

with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            connection = Connection(
                row['station1'],
                row['station2'],
                int(row['distance'])  # Assuming 'distance' is the travel time
            )
            connections.append(connection)


# Example usage:
file_path = 'data/ConnectionsHolland.csv'
connections_list = connections

total_connections = connections_list
astar_scheduler = AStarScheduler(max_trains, max_time, total_connections)
optimal_schedule = astar_scheduler.create_optimal_schedule()

if optimal_schedule:
    optimal_schedule.display_schedule("A*", 1, save_each_output_as_csv=True)
else:
    print("Optimal schedule not found.")
