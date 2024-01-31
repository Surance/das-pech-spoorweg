import random
import math
from copy import deepcopy
from code.functions.quality import calculate_quality
from code.algorithms.greedy import GreedySchedule
from code.classes.schedule import Schedule

from .HillClimb_Train import HillClimber_train
from .HillClimb_Connection import HillClimber_connections

class HillClimberCombinedCopy:
    """
    Class for the HillClimber algorithm that combines hillclimber train and connection changes.
    
    Includes a function that 
    Includes functions for deleting and adding trains, deleting and adding connections, and a function that calculates
    the quality score of the schedule.

    The algorithm continues to initialize new schedules for a set number of iterations, considering changes at both
    train and connection levels.
    """
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
    
    def alter_trains(self):
        """
        
        """
        copy_schedule = deepcopy(self.schedule)
        
        trains_to_change = random.randint(1, 10) 

        altered_schedule = HillClimber_train(copy_schedule).delete_train(copy_schedule, trains_to_change)
        
        altered_schedule = HillClimber_train(altered_schedule).add_new_train(altered_schedule, trains_to_change)

        current_score = self.calculate_schedule_score(altered_schedule)

        if current_score > self.best_score:
            self.best_score = current_score
            self.best_schedule = altered_schedule
            print(f"Iteration: {self.iteration_count} | Trains changed: {trains_to_change} | Current Score: {current_score} | Best Score: {self.best_score} |")

        self.iteration_count += 1

    def alter_connections(self):
        """
        
        """
        copy_schedule = deepcopy(self.schedule)
        rand_int = random.randint(0, 1)
        if rand_int == 0:
            altered_schedule = HillClimber_connections(copy_schedule).delete_connection(copy_schedule)
            move = "deletion"
        else:
            altered_schedule = HillClimber_connections(copy_schedule).add_connection(copy_schedule)
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

    def get_best_combined_traject(self) -> tuple[list, set]:
        """

        """
        print("NEW TRIAL TRAINS ------------------------")
        for _ in range(10):
            self.alter_trains()

        # Because of removes and adds train names are no longer correct so we need to rename them in correct order 
        self.best_schedule.rename_trains()

        # After the loop, set the schedule to the best_schedule
        self.schedule = self.best_schedule

        print("NEW TRIAL CONNECTION ------------------------")
        while self.temperature > 1.0:
            self.alter_connections()

        # After the loop, set the schedule to the best_schedule
        self.schedule = self.best_schedule

        return self.schedule.trains, self.schedule.ridden

    def calculate_schedule_score(self, schedule: Schedule) -> float:
        """
        Calculate the quality score for the current schedule
        """
        return calculate_quality(schedule.ridden, schedule.trains, schedule.total_connections)