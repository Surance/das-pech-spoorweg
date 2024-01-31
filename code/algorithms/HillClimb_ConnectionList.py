import random
import math
from copy import deepcopy
from code.functions.quality import calculate_quality
from code.algorithms.greedy import GreedySchedule
from code.classes.schedule import Schedule

class HillClimber_connectionslist:
    """
    Class for the HillClimber algorithm that focuses on modifying connections lists.

    Includes functions for deleting and adding connections, and a function that calculates
    the quality score of the schedule.

    The algorithm continues to initialize new schedules for a set number of iterations,
    considering changes in connection lists.
    """
    def __init__(self, schedule: Schedule, initial_temperature: float = 100.0, cooling_rate: float = 0.95, convergence_threshold: float = 0.001) -> None:
        """
        Initialize the HillClimberConnectionsList object.

        Parameters:
            schedule (Schedule): The initial schedule.
            initial_temperature (float): The initial temperature for simulated annealing.
            cooling_rate (float): The cooling rate for simulated annealing.
            convergence_threshold (float): The threshold for considering convergence.
        """
        self.schedule = GreedySchedule(schedule).create_greedy_schedule()
        self.best_score = float('-inf')
        self.best_schedule = None
        self.temperature = initial_temperature
        self.cooling_rate = cooling_rate
        self.convergence_threshold = convergence_threshold
        self.iteration_count = 0
        self.scores_over_iterations = []

    def delete_connections(self, schedule: Schedule) -> Schedule:
        """
        Delete connections from a random index to the end of the list. 
        
        Args:
            schedule (Schedule): The schedule to be modified.

        Returns:
            Schedule: The modified schedule after deleting a part of the connection list.
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

        return schedule

    def add_connection(self, schedule: Schedule) -> Schedule:
        """
        Add a random connection to the schedule. Update time and used connections.

        Args:
            schedule (Schedule): The schedule to be modified.

        Returns:
            Schedule: The modified schedule after adding back part of the connection list.
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

        return schedule

    def get_best_connections(self) -> tuple[list, set]:
        """
        Optimize the schedule by randomly deleting or adding connections.

        Returns:
            tuple[list, set]: Tuple containing the list of trains and the set of ridden connections.
        """
        print("NEW TRIAL CONNECTION ------------------------")
        while self.temperature > 1.0:
            copy_schedule = deepcopy(self.schedule)

            rand_int = random.randint(0, 1)

            if rand_int == 0:
                altered_schedule = self.delete_connections(copy_schedule)
                move = "Deletion"
            else:
                altered_schedule = self.add_connection(copy_schedule)
                move = "Addition"

            current_score = self.calculate_schedule_score(altered_schedule)
            self.scores_over_iterations.append(current_score)

            if current_score > self.best_score or random.uniform(0, 1) < math.exp((current_score - self.best_score) / self.temperature):
                self.best_score = current_score
                self.best_schedule = altered_schedule
                print(f"Iteration: {self.iteration_count} | Move: {move} | Current Score: {current_score} | Best Score: {self.best_score} | Temperature: {self.temperature}")

            self.iteration_count += 1

            # Update temperature
            self.temperature *= self.cooling_rate

            # Check for convergence
            if self.iteration_count > 1 and abs(current_score - self.scores_over_iterations[-2]) < self.convergence_threshold:
                print("Convergence achieved. Stopping the optimization.")
                break

        # After the loop, set the schedule to the best_schedule
        self.schedule = self.best_schedule

        return self.schedule.trains, self.schedule.ridden

    def calculate_schedule_score(self, schedule: Schedule) -> float:
        """
        Calculate the quality score for the current schedule.

        Args:
            schedule (Schedule): The schedule for which the quality score is calculated.

        Returns:
            float: The quality score.
        """
        return calculate_quality(schedule.ridden, schedule.trains, schedule.total_connections)