from .schedule import Schedule
from .connection import Connection
from code.algorithms.random import RandomSchedule
from code.algorithms.greedy import GreedySchedule
from code.algorithms.HillClimb_Train import HillClimber_train
from code.algorithms.HillClimb_Connection import HillClimber_connections
from code.algorithms.HillClimb_ConnectionList import HillClimber_connectionslist
from code.algorithms.HillClimb_Combined import HillClimberCombined
from code.algorithms.hillclimb_combinedCopy import HillClimberCombinedCopy

import os
import pandas as pd
import csv

class Experiment:
    """
    Represents an experiment that runs multiple trials of a train schedule optimization algorithm.

    Attributes:
        iterations (int): The number of trials to run for the experiment.
        algorithm (str): The algorithm to be used in each trial.
        all_scores (list): The list of scores for each trial.
        all_ridden (list): The list of number of ridden connections for each trial.
        all_stations_trains (list): The list of stations ridden for each trial
    """

    def __init__(self, data: csv, iterations: int, algorithm: str) -> None:
        """
        Initializes a new Experiment object with the provided attributes.

        Parameters:
            data (csv): The data file containing all connection information.
            iterations (int): The number of trials to run for the experiment.
            algorithm (str): The optimization algorithm to be used in each trial.
        """
        self.data = pd.read_csv(data)
        self.iterations = iterations
        self.algorithm = algorithm

        # Keep track of scores and connections ridden per experiment
        self.all_scores = []
        self.all_ridden = []
        self.all_stations_trains = []

        # Create a directory to save the csv outputs in
        self.directory_path = f"experiment/{self.algorithm}"

    def create_connection_list(self) -> list[Connection]:
        """
        Function creates list of all connections available in the Netherlands.
        """
        connections_list = []
        for _, row in self.data.iterrows():
            connections_list.append(Connection(row['station1'], row['station2'], row['distance']))

        return connections_list

    def find_file_number(self, summary_boolean: bool) -> int:
        """
        Function finds most recent directory number in parent directory and returns correct experiment number for new file 
        depending on if the csv is an experiment summary or seperate experiment.
        
        Only want directory to change if it is a new experiment. Summaries should be in the same directory

        Parameters:
            summary_boolean (bool): A boolean indicating whether the CSV is an experiment summary.
        
        Returns:
            int: The correct experiment number.
        """
        max_number = 0

        # Find the directory with the largest number
        for directory in self.existing_directories:
            number = int(directory.split('_')[-1])
            max_number = max(max_number, number)

        if summary_boolean == False:
            # New experiment number is one more than largest number in directory
            return max_number + 1
        else: 
            return max_number

    def path_name(self, summary: bool = False) -> str:
        """
        Function creates a file name according to the algorithm and the nth experiment it is. 

        Parameters:
            summary (bool, optional): A flag indicating whether the CSV is an experiment summary. Defaults to False.

        Returns:
            str: The path name for saving the CSV results.
        """
        # Create folder if it doesn't exist
        if not os.path.exists(self.directory_path):
            os.makedirs(self.directory_path)

        # Get a list of existing directories in the parent directory
        self.existing_directories = [d for d in os.listdir(self.directory_path) if os.path.isdir(os.path.join(self.directory_path, d))]

        # Find experiment number depending on whether it is a summary file or not
        experiment_number = self.find_file_number(summary)

        return f"experiment/{self.algorithm}/{self.algorithm}_{experiment_number}/"
    
    def find_index_schedules_all_connections(self) -> list[int]:
        """
        Function finds indeces of the schedules that rode all the connections and adds them to a list.
        """
        self.all_ridden_list = []

        amount_total_connections = len(self.all_connections)

        # Check in each trial whether all connections were ridden
        for index, trial_ridden in enumerate(self.all_ridden):

            if trial_ridden == amount_total_connections:
                self.all_ridden_list.append(index)

    def find_scores_schedules_all_connections(self) -> dict:
        """
        Function finds scores and indexes of the schedules that rode all connections and returns them in a dictionary

        Returns:
            dict: A dictionary mapping scores to indices of schedules that rode all connections.
        """
        all_ridden_scores = {}

        for index, score in enumerate(self.all_scores):
            if index in self.all_ridden_list:
                all_ridden_scores[score] = index

        return all_ridden_scores
    
    def get_best_trial(self) -> list:
        """
        Function finds schedule that rode all connections with best score so that this schedule can be visualised later.

        Returns: 
            list: The list of station names from the best schedule.
        """
        # Add all indexes of schedules that rode all connections to list
        self.find_index_schedules_all_connections()
        
        # If none of the schedules were able to ride all connections get the best score of all trials
        if len(self.all_ridden_list) == 0:
            index_best_score = self.all_scores.index(max(self.all_scores))
            return self.all_stations_trains[index_best_score]

        # Find the scores of the schedules that rode all connections
        all_ridden_scores = self.find_scores_schedules_all_connections()

        # Take index with max score and return its train schedule 
        index_best_score = all_ridden_scores[max(all_ridden_scores)]
        return self.all_stations_trains[index_best_score]

    def run_experiment(self, max_trains: int, max_time: int) -> tuple[list, list, list]:
        """
        Function runs an experiment of N trials that each create a schedule using the algorithm specified

        Args:
            max_trains (int): The maximum number of trains in the schedule.
            max_time (int): The maximum time allowed for the schedule in minutes.

        Returns:
            tuple[list, list[list], list[list]]: 
                A tuple containing the stations of the best schedule, a list of all scores per schedule of the experiment
                and a list of all connections ridden per trial of the experiment .
        """
        # Create pathname to save trial csv outputs in
        self.pathname = self.path_name()

        self.all_connections = self.create_connection_list()
        
        for trial in range(self.iterations):
            file_name = f"{self.pathname}experiment_{trial + 1}"

            schedule = Schedule(max_trains, max_time, self.all_connections)

            # Create a schedule depending on which algorithm is called
            if self.algorithm == "random":
                random_schedule = RandomSchedule(schedule).create_random_schedule()
                schedule.trains = random_schedule.trains
                schedule.ridden = random_schedule.ridden

            elif self.algorithm == "greedy":
                greedy_schedule = GreedySchedule(schedule).create_greedy_schedule()
                schedule.trains = greedy_schedule.trains
                schedule.ridden = greedy_schedule.ridden

            elif self.algorithm == "hillclimb_train":
                hillclimber = HillClimber_train(schedule)
                best_trains, best_ridden = hillclimber.get_best_train()
                schedule.trains = best_trains
                schedule.ridden = best_ridden

            elif self.algorithm == "hillclimb_connection":
                hillclimber = HillClimber_connections(schedule)
                best_trains, best_ridden = hillclimber.get_best_connections()
                schedule.trains = best_trains
                schedule.ridden = best_ridden

            elif self.algorithm == "hillclimb_connectionlist":
                hillclimber = HillClimber_connectionslist(schedule)
                best_trains, best_ridden = hillclimber.get_best_connections()
                schedule.trains = best_trains
                schedule.ridden = best_ridden
            
            elif self.algorithm == "hillclimb_combined":
                hillclimber = HillClimberCombined(schedule)
                best_trains, best_ridden = hillclimber.get_best_combined_traject()
                schedule.trains = best_trains
                schedule.ridden = best_ridden

            else: 
                print("No valid algorithm was called. Please call one of the following algorithms in main.py:")
                print("'random', 'greedy', 'hillclimb_connection', 'hillclimb_train', or 'hillclimb_combined'")
                break

            trial_stations_trains, trial_score, trial_ridden = schedule.display_schedule(file_name, save_each_output_as_csv=True)

            # Add score and number of ridden connections of trial to lists
            self.all_scores.append(trial_score)
            self.all_ridden.append(trial_ridden)
            self.all_stations_trains.append(trial_stations_trains)

        # Find which of the trials created the best schedule
        best_stations_trains = self.get_best_trial()

        return best_stations_trains, self.all_scores, self.all_ridden
    
    def summary_experiment(self) -> None:
        """
        Function adds file inside experiment directory that shows summary of the experiment. 
        """
        file_name = f"{self.pathname}EXPERIMENT_SUMMARY"
        
        # Create folder if it doesn't exist
        os.makedirs(os.path.dirname(file_name), exist_ok=True)

        with open(file_name, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)

            csv_writer.writerow(["Algorithm type", self.algorithm])
            
            csv_writer.writerow(["Number of Trials", self.iterations])

            csv_writer.writerow(["Average Score", sum(self.all_scores)/self.iterations])

            csv_writer.writerow(["Average Connections Ridden", sum(self.all_ridden)/self.iterations])

            csv_writer.writerow(["Maximum Score", max(self.all_scores)])

            csv_writer.writerow(["Score", self.all_scores])

            csv_writer.writerow(["Connections ridden", self.all_ridden])