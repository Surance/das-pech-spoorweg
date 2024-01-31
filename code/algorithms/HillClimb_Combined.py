import random
import math
from copy import deepcopy
from code.functions.quality import calculate_quality
from code.algorithms.greedy import GreedySchedule
from code.classes.schedule import Schedule

class HillClimberCombined:
    def __init__(self, schedule: Schedule, initial_temperature: float = 100.0, cooling_rate: float = 0.95, convergence_threshold: float = 0.001) -> None:
        self.schedule = GreedySchedule(schedule).create_greedy_schedule()
        self.best_score = float('-inf')
        self.best_schedule = None
        self.temperature = initial_temperature
        self.cooling_rate = cooling_rate
        self.convergence_threshold = convergence_threshold
        self.iteration_count = 0
        self.scores_over_iterations = []
        self.iteration_count_train = 0
        self.iteration_count_conn = 0

    def delete_train(self, schedule: Schedule, trains_to_change) -> Schedule:
        """
        Delete a random amount of trains from the schedule. Amount of trains to delete is given by trains_to_change.
        Also removes connections ridden by the train from the ridden set, so that score is calculated accurately.
        """
        for _ in range(trains_to_change):
            train = random.choice(schedule.trains)
            
            # Remove connections ridden by the train from the ridden set
            for connection in train.connections_list:
                if connection in schedule.ridden:
                    schedule.ridden.remove(connection)
            
            schedule.trains.remove(train)

        return schedule
    
    def add_new_train(self, schedule: Schedule, trains_to_change) -> Schedule:
        """
        Add a random amount of trains back to the schedule. Update time and used connections.
        Amount of trains to add is given by parameter trains_to_change.
        """
        # Don't add a new train if there are already a maximum of trains present in schedule 
        if len(schedule.trains) == schedule.max_trains: 
            return schedule 
        
        for _ in range(trains_to_change):
            schedule.add_train()

        # Add new stations to train if it connects to previous station until all connections are passed or max time is met
        while schedule.current_time < schedule.max_time and len(schedule.ridden) < len(schedule.total_connections):
            
            # Check which connections are possible with the previous arrival station
            possible_connections = schedule.check_possible_connections()

            if len(possible_connections.keys()) == 0:
                break
            
            # Pick a random connection from those that are possible
            connection = random.choice(list(possible_connections.keys()))

            schedule.valid_connection(connection, possible_connections[connection])

        schedule.train.total_time += schedule.current_time
        schedule.trains.append(schedule.train)
        
        return schedule
    
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

        return schedule
    
 
    def get_best_combined_traject(self) -> tuple[list, set]:
        """
        Randomly choose to delete or add a train. If the quality is higher after the change, keep the schedule
        """
        print("NEW TRIAL TRAINS ------------------------")
        for _ in range(10):
            copy_schedule = deepcopy(self.schedule)
            
            trains_to_change = random.randint(1, 10) 

            altered_schedule = self.delete_train(copy_schedule, trains_to_change)
            
            altered_schedule = self.add_new_train(altered_schedule, trains_to_change)

            current_score = self.calculate_schedule_score(altered_schedule)

            if current_score > self.best_score:
                self.best_score = current_score
                self.best_schedule = altered_schedule
                print(f"Iteration: {self.iteration_count} | Trains changed: {trains_to_change} | Current Score: {current_score} | Best Score: {self.best_score} |")

            self.iteration_count += 1

        # Because of removes and adds train names are no longer correct so we need to rename them in correct order 
        self.best_schedule.rename_trains()

        # After the loop, set the schedule to the best_schedule
        self.schedule = self.best_schedule

        print("NEW TRIAL CONNECTION ------------------------")
        while self.temperature > 1.0:
            copy_schedule = deepcopy(self.schedule)
            rand_int = random.randint(0, 1)
            if rand_int == 0:
                altered_schedule = self.delete_connections(copy_schedule)
                move = "deletion"
            else:
                altered_schedule = self.add_connection(copy_schedule)
                move = "addition"

            current_score = self.calculate_schedule_score(altered_schedule)
            self.scores_over_iterations.append(current_score)

            if current_score > self.best_score or random.uniform(0, 1) < math.exp((current_score - self.best_score) / self.temperature):
                self.best_score = current_score
                self.best_schedule = altered_schedule
                print(f"Iteration: {self.iteration_count} | Move: {move} | Current Score: {current_score} | Best Score: {self.best_score} | Temperature: {self.temperature}")

            self.iteration_count += 1

            # Update temperature
            self.temperature *= self.cooling_rate

        # After the loop, set the schedule to the best_schedule
        self.schedule = self.best_schedule

        return self.schedule.trains, self.schedule.ridden


    def calculate_schedule_score(self, schedule: Schedule) -> float:
        """
        Calculate the quality score for the current schedule
        """
        return calculate_quality(schedule.ridden, schedule.trains, schedule.total_connections)
        

