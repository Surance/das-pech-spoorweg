from .information import Information
from .schedule import Schedule
from code.algorithms.random import Random_schedule
from code.algorithms.greedy import GreedySchedule
from code.algorithms.HillClimb_Train import HillClimber_train
from code.algorithms.HillClimb_Connection import HillClimber_connections
from code.algorithms.HillClimb_ConnectionList import HillClimber_connectionsUPDATE
from code.algorithms.HillClimb_Combined import HillClimber_combined

import os

class Experiment:
    def __init__(self, data: classmethod, iterations: int, algorithm: str, max_trains: int, max_time: int) -> None:
        self.data = data
        self.iterations = iterations
        self.algorithm = algorithm
        self.max_trains = max_trains
        self.max_time = max_time

        self.all_connections = Information.create_connection(self.data)
        
        # Keep track of scores and connections ridden per experiment
        self.all_scores = []
        self.all_ridden = []
        self.all_stations_trains = []

        self.directory_path = f"experiment/{self.algorithm}"

    def find_most_recent_directory(self) -> int:
        """
        Function finds most recent directory in parent directory by looking at largest number
        """
        max_number = 0

        # Find the directory with the largest number
        for directory in self.existing_directories:
            number = int(directory.split('_')[-1])
            max_number = max(max_number, number)

        return max_number
    
    def check_if_new_experiment(self, summary_boolean: bool) -> int:
        """
        Function returns the correct experment number depending on if the csv is an experiment summary or seperate experiment
        """
        if summary_boolean == False:
            # New experiment number is one more than largest number in directory
            return self.max_number + 1
        else: 
            return self.max_number

    def path_name(self, summary: bool = False) -> str:
        """
        Function creates a file name according to the algorithm and the nth experiment it is  
        """

        # Create folder if it doesn't exist
        if not os.path.exists(self.directory_path):
            os.makedirs(self.directory_path)

        # Get a list of existing directories in the parent directory
        self.existing_directories = [d for d in os.listdir(self.directory_path) if os.path.isdir(os.path.join(self.directory_path, d))]

        self.max_number = self.find_most_recent_directory()

        # Only want directory to change if it is a new experiment, summaries should be in the same directory
        experiment_number = self.check_if_new_experiment(summary)

        return f"experiment/{self.algorithm}/{self.algorithm}_{experiment_number}/"
    
    def find_index_schedules_all_connections(self) -> list:
        """
        Function finds indeces of the schedules that rode all the connections and adds them to a list
        """
        all_ridden_list = []

        amount_total_connections = len(self.all_connections)

        # Check in each trial whether all connections were ridden
        for index, trial_ridden in enumerate(self.all_ridden):

            if trial_ridden == amount_total_connections:
                all_ridden_list.append(index)

        return all_ridden_list
    
    def find_scores_schedules_all_connections(self, all_ridden) -> dict:
        """
        Function finds scores and indexes of the schedules that rode all connections and returns them in a dictionary
        """
        all_ridden_scores = {}
        for index, score in enumerate(self.all_scores):
            if index in all_ridden:
                all_ridden_scores[score] = index

        return all_ridden_scores
    
    def get_best_trial(self) -> float:
        """
        Function finds trial that rode all connections with best score and returns its train schedule
        """

        # Add all indexes of schedules that rode all connections to list
        all_ridden = self.find_index_schedules_all_connections()
        
        # If none of the schedules were able to ride all connections get the best score of all trials
        if len(all_ridden) == 0:
            index_best_score = self.all_scores.index(max(self.all_scores))
            return self.all_stations_trains[index_best_score]

        # Find the scores of the schedules that rode all connections
        all_ridden_scores = self.find_scores_schedules_all_connections(all_ridden)

        # Take index with max score and return its train schedule 
        index_best_score = all_ridden_scores[max(all_ridden_scores)]
        return self.all_stations_trains[index_best_score]

    def run_experiment(self) -> tuple[float, list, list]:
        """
        Function runs an experiment of N trials that each create a schedule using the algorithm specified
        """

        # Create pathname to save trial csv outputs in
        pathname = self.path_name()
        
        for trial in range(self.iterations):
            file_name = f"{pathname}experiment_{trial + 1}"

            schedule = Schedule(self.max_trains, self.max_time, self.all_connections)

            # Create a schedule depending on which algorithm is called
            if self.algorithm == "random":
                random_schedule = Random_schedule(schedule).create_random_schedule()
                schedule.trains = random_schedule.trains
                schedule.ridden = random_schedule.ridden

            elif self.algorithm == "greedy":
                greedy_schedule = GreedySchedule(schedule).create_greedy_schedule()
                schedule.trains = greedy_schedule.trains
                schedule.ridden = greedy_schedule.ridden

            elif self.algorithm == "hillclimb":
                hillclimber = HillClimber_connections(schedule)
                best_trains, best_ridden = hillclimber.get_best_connections()
                schedule.trains = best_trains
                schedule.ridden = best_ridden

            elif self.algorithm == "hillclimb2":
                hillclimber = HillClimber_connectionsUPDATE(schedule)
                best_trains, best_ridden = hillclimber.get_best_connections()
                schedule.trains = best_trains
                schedule.ridden = best_ridden

            elif self.algorithm == "hillclimb_train":
                train_climber = HillClimber_train(schedule)
                best_trains, best_ridden = train_climber.get_best_train() 
                schedule.trains = best_trains
                schedule.ridden = best_ridden
            
            elif self.algorithm == "hillclimbCombined":
                hillclimber = HillClimber_combined(schedule)
                best_trains, best_ridden = hillclimber.run()
                schedule.trains = best_trains
                schedule.ridden = best_ridden

            elif self.algorithm == "greedy2":
                greedy_schedule = GreedySchedule(schedule).create_greedy_schedule()
                schedule.trains = greedy_schedule.trains
                schedule.ridden = greedy_schedule.ridden

            else: 
                print("No valid algorithm was called. Please call one of the following algorithms in main.py:")
                print("'random', 'greedy', 'hillclimb', 'hillclimb_train'")
                break

            trial_stations_trains, trial_score, trial_ridden = schedule.display_schedule(file_name, save_each_output_as_csv=True)

            # Add score and number of ridden connections of trial to lists
            self.all_scores.append(trial_score)
            self.all_ridden.append(trial_ridden)
            self.all_stations_trains.append(trial_stations_trains)

        # Find which of the trials created the best schedule
        best_stations_trains = self.get_best_trial()

        return best_stations_trains, self.all_scores, self.all_ridden