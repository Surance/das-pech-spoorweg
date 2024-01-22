from code.classes.information import Information
from code.classes.schedule import Schedule
from code.algorithms.random import Random_schedule

from code.visualisation.visualise import process_input
from code.visualisation.visualise import plot_trains
from code.visualisation.visualise import get_coordinates
from code.visualisation.visualise import coords_data

import pandas as pd
import csv

if __name__ == "__main__":
    # Input csv's
    data = Information("data/StationsHolland.csv", "data/ConnectionsHolland.csv")

    # Count scores and connections ridden per experiment
    score_count = 0
    ridden_count = 0

    iterations = 1000
    # TODO: find a way so it automatically calls it: algorithm_existing N + 1 
    algorithm = "random_3"
    algorithm_type = "random"
    max_trains = 7
    max_time = 120  # 2 hours

    # TODO: put the following in seperate file & function
    for trial in range(iterations):

        # Create objects
        all_stations = Information.create_station(data)
        all_connections = Information.create_connection(data)

        schedule = Schedule(max_trains, max_time, all_connections)

        if algorithm_type == "random":
            Random_schedule.create_random_schedule(schedule)
        
        # TODO: add if statement for dijkstra
        # elif algorithm_type == "dijkstra":
        

        stations_trains, trial_score, trial_ridden = schedule.display_schedule(algorithm, trial)

        # Add score and number of ridden connections of trial to count
        score_count += trial_score
        ridden_count += trial_ridden

    # Calling and running visualise
    train_data = process_input(stations_trains)
    plot_trains(coords_data, train_data)

    # Save file with summary of the trials in the experiment 
    file_name = f"experiment/{algorithm}/EXPERIMENT_SUMMARY"

    with open(file_name, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        csv_writer.writerow(["Algorithm type", algorithm])
        
        csv_writer.writerow(["Number of Trials", iterations])

        csv_writer.writerow(["Average Score", score_count/iterations])

        csv_writer.writerow(["Average Connections Ridden", ridden_count/iterations])





    