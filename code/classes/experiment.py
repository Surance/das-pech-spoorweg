from .information import Information
from .schedule import Schedule
from code.algorithms.random import Random_schedule
from code.algorithms.greedy import GreedySchedule
from code.algorithms.HillClimb import HillClimbingScheduler

import os

class Experiment:
    def __init__(self, data, iterations, algorithm, max_trains, max_time):
        self.data = data
        self.iterations = iterations
        self.algorithm = algorithm
        self.max_trains = max_trains
        self.max_time = max_time
        
        # Count scores and connections ridden per experiment
        self.score_count = 0
        self.ridden_count = 0

    def path_name(self):
        """
        Function creates a file name according to the algorithm and the 
        """
        # Get a list of existing directories in the parent directory
        existing_directories = [d for d in os.listdir(f"experiment/{self.algorithm}") if os.path.isdir(os.path.join(f"experiment/{self.algorithm}", d))]
        max_number = 0

        # Find the directory with the largest number
        for directory in existing_directories:
            number = int(directory.split('_')[-1])
            max_number = max(max_number, number)

        # New experiment number is one more than largest number in directory
        experiment_number = max_number + 1

        return f"experiment/{self.algorithm}/{self.algorithm}_{experiment_number}/"

    def run_experiment(self):
        # Create objects
        all_stations = Information.create_station(self.data)
        all_connections = Information.create_connection(self.data)
        pathname = self.path_name()
        
        for trial in range(self.iterations):

            file_name = f"{pathname}experiment_{trial + 1}"

            schedule = Schedule(self.max_trains, self.max_time, all_connections)

            # Create a schedule depending on which algorithm is called
            if self.algorithm == "random":
                Random_schedule.create_random_schedule(schedule)

            elif self.algorithm == "greedy":
                GreedySchedule.create_greedy_schedule(schedule)

            elif self.algorithm == "hillclimb":
                HillClimbingScheduler.hill_climbing_schedule(schedule)

            stations_trains, trial_score, trial_ridden = schedule.display_schedule(file_name)

            # Add score and number of ridden connections of trial to count
            self.score_count += trial_score
            self.ridden_count += trial_ridden

        return stations_trains, self.score_count, self.ridden_count