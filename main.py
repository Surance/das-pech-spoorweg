from code.classes.information import Information
from code.classes.schedule import Schedule
from code.classes.experiment import Experiment
from code.algorithms.random import Random_schedule
from code.algorithms.Astar import AStarScheduler
from code.algorithms.greedy import GreedySchedule

from code.visualisation.visualise import process_input
from code.visualisation.visualise import plot_trains
from code.visualisation.visualise import get_coordinates
from code.visualisation.visualise import coords_data

import pandas as pd
import csv

if __name__ == "__main__":
    # Input csv's
    data = Information("data/StationsHolland.csv", "data/ConnectionsHolland.csv")

    iterations = 1000
    algorithm = "random"
    max_trains = 7
    max_time = 120  # 2 hours

    # Run an experiment with specified algorithm and specified number of iterations
    stations_trains, score_count, ridden_count = Experiment(data, iterations, algorithm, max_trains, max_time).run_experiment()

    # Calling and running visualiser
    train_data = process_input(stations_trains)
    plot_trains(coords_data, train_data)

    # Save file with summary of the trials in the experiment
    pathname = Schedule.path_name(algorithm) 
    Information.summary_experiment(algorithm, pathname, iterations, score_count, ridden_count)