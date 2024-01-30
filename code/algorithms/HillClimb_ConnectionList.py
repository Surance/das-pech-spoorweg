import random
from copy import deepcopy
from math import exp
from code.classes.quality import Quality
from code.algorithms.random import Random_schedule
from code.classes.schedule import Schedule

class HillClimber_connectionsUPDATE:
    def __init__(self, schedule: Schedule, initial_temperature=1000, cooling_rate=0.99, min_temperature=0.1, iterations_per_temperature=50, exploration_penalty_factor=0.1) -> None:
        self.schedule = Random_schedule(schedule).create_random_schedule()
        self.best_score = float('-inf')
        self.best_schedule = None
        self.initial_temperature = initial_temperature
        self.cooling_rate = cooling_rate
        self.min_temperature = min_temperature
        self.iterations_per_temperature = iterations_per_temperature
        self.exploration_penalty_factor = exploration_penalty_factor
        self.explored_connections = set()

    def delete_connections(self, schedule: Schedule) -> Schedule:
        """
        Delete connections from a random index to the end of the list.
        """
        train = random.choice(schedule.trains)
        if not train.connections_list:
            return schedule

        index = random.randint(0, len(train.connections_list) - 1)
        connections_to_remove = train.connections_list[index:]
        station = train.stations_names_list[-1]

        for connection in connections_to_remove:
            train.connections_list.remove(connection)
            if connection in schedule.ridden:
                schedule.ridden.remove(connection)

        train.stations_names_list.remove(station)

        schedule.current_time -= sum(connection.travel_time for connection in connections_to_remove)
        self.explored_connections.update(connections_to_remove)

        return schedule

    def add_connection(self, schedule) -> classmethod:
        """
        Add a random connection to the schedule. Update time and used connections
        """
        possible_connections = schedule.check_possible_connections()
        if len(possible_connections.keys()) == 0:
            return schedule

        train = random.choice(schedule.trains)
        connection = random.choice(list(possible_connections.keys()))
        schedule.valid_connection(connection, possible_connections[connection])

        train.connections_list.append(connection)
        train.stations_names_list.append(possible_connections[connection])
        schedule.current_time += connection.travel_time
        schedule.ridden.add(connection)

        self.explored_connections.add(connection)

        return schedule

    def get_best_connections(self) -> tuple[list, set]:
        """
        Randomly choose to delete or add connections. If the quality is higher after the change, keep the schedule
        """
        print("NEW TRIAL ------------------------")
        temperature = self.initial_temperature

        for iteration in range(self.iterations_per_temperature):
            copy_schedule = deepcopy(self.schedule)
            rand_int = random.randint(0, 1)
            if rand_int == 0:
                altered_schedule = self.delete_connections(copy_schedule)
                print(f"Iteration: {iteration + 1} | Move: Deletion")
            else:
                altered_schedule = self.add_connection(copy_schedule)
                print(f"Iteration: {iteration + 1} | Move: Addition")

            current_score = self.calculate_schedule_score(altered_schedule)

            # Add exploration penalty
            exploration_penalty = self.exploration_penalty_factor * len(set(altered_schedule.trains[0].connections_list) - self.explored_connections)
            current_score -= exploration_penalty

            if current_score > self.best_score or random.uniform(0, 1) < exp((current_score - self.best_score) / temperature):
                self.best_score = current_score
                self.best_schedule = altered_schedule

            temperature *= self.cooling_rate
            temperature = max(temperature, self.min_temperature)

        # After the loop, set the schedule to the best_schedule
        self.schedule = self.best_schedule

        return self.schedule.trains, self.schedule.ridden

    def calculate_schedule_score(self, schedule: Schedule) -> float:
        """
        Calculate the quality score for the current schedule
        """
        return Quality(schedule.ridden, schedule.trains, schedule.total_connections).calculate_quality()
