from .information import Information
from .schedule import Schedule
from code.algorithms.random import Random_schedule
from code.algorithms.greedy import GreedySchedule
from code.algorithms.HillClimb import HillClimbingScheduler
from code.algorithms.HillClimber import HillClimber

import os

class Experiment:
    def __init__(self, data: classmethod, iterations: int, algorithm: str, max_trains: int, max_time: int) -> None:
        self.data = data
        self.iterations = iterations
        self.algorithm = algorithm
        self.max_trains = max_trains
        self.max_time = max_time
        
        # Keep track of scores and connections ridden per experiment
        self.all_scores = []
        self.all_ridden = []
        self.all_stations_trains = []

    def path_name(self, summary: bool = False) -> str:
        """
        Function creates a file name according to the algorithm and the nth experiment it is  
        """

        directory_path = f"experiment/{self.algorithm}"

        # Create folder if it doesn't exist
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        # Get a list of existing directories in the parent directory
        existing_directories = [d for d in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, d))]
        max_number = 0

        # Find the directory with the largest number
        for directory in existing_directories:
            number = int(directory.split('_')[-1])
            max_number = max(max_number, number)

        if summary == False:
            # New experiment number is one more than largest number in directory
            experiment_number = max_number + 1
        else: 
            experiment_number = max_number

        return f"experiment/{self.algorithm}/{self.algorithm}_{experiment_number}/"
    
    def get_best_trial(self) -> float:
        """
        Function finds trial that rode all connections with best score and returns its train schedule
        """

        # Add all indexes of schedules that rode all connections to list
        all_ridden = []
        for index, trial_ridden in enumerate(self.all_ridden):
            # TODO: currently hard coded 28 connections: update this when applying for all of NL
            if trial_ridden == 28:
                all_ridden.append(index)
        
        # If none of the schedules were able to ride all connections get the best score of all trials
        if len(all_ridden) == 0:
            index_best_score = self.all_scores.index(max(self.all_scores))
            return self.all_stations_trains[index_best_score]

        # Find the scores and indexes of the schedules that rode all connections
        all_ridden_scores = {}
        for index, score in enumerate(self.all_scores):
            if index in all_ridden:
                all_ridden_scores[score] = index

        # Take index with max score and return its train schedule 
        index_best_score = all_ridden_scores[max(all_ridden_scores)]
        return self.all_stations_trains[index_best_score]

    def run_experiment(self) -> tuple(float, list, list):
        """
        Function runs an experiment of N trials that each create a schedule using the algorithm specified
        """

        # Create objects
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
                arbitrary_solution = Random_schedule.create_random_schedule(schedule) 
                hillclimber = HillClimber(arbitrary_solution)
                best_trains, best_ridden = hillclimber.get_best_connection() 
                schedule.trains = best_trains
                schedule.ridden = best_ridden

            trial_stations_trains, trial_score, trial_ridden = schedule.display_schedule(file_name, save_each_output_as_csv=True)

            # Add score and number of ridden connections of trial to lists
            self.all_scores.append(trial_score)
            self.all_ridden.append(trial_ridden)
            self.all_stations_trains.append(trial_stations_trains)

        # Find which of the trials created the best schedule
        best_stations_trains = self.get_best_trial()

        return best_stations_trains, self.all_scores, self.all_ridden