import argparse

from code.classes.experiment import Experiment

from code.visualisation.visualise_plot import process_input
from code.visualisation.visualise_plot import plot_trains
from code.visualisation.visualise_plot import coords_data
from code.visualisation.visualise_map import create_map_plot
from code.visualisation.visualise_map import format_coordinates

def parse_arguments():
    """
    Adds an argument parser to the main.py file, so that the user can specify the number of iterations, algorithm, 
    maximum number of trains, maximum time, and visualization options.
    """
    parser = argparse.ArgumentParser(description="Run an experiment with specified parameters.")
    parser.add_argument("--standard_experiment", action="store_true", help="Run a standard experiment with default parameters.")
    parser.add_argument("--algorithm", type=str, help="Algorithm to use for the experiment.")
    parser.add_argument("--iterations", type=int, help="Number of iterations for the experiment.")
    parser.add_argument("--max_trains", type=int, help="Maximum number of trains for the experiment.")
    parser.add_argument("--max_time", type=int, help="Maximum time for the experiment in minutes.")
    parser.add_argument("--visualise_plot", action="store_true", help="Whether to visualize the plot.")
    parser.add_argument("--visualise_map", action="store_true", help="Whether to visualize the map.")

    return parser.parse_args()

def get_user_input():
    """
    If the user does not specify the arguments in the command line, this function prompts the user to enter the
    arguments manually one by one.
    """
    standard_experiment = input("Do you want to run a standard experiment? (y/n): ").lower() == 'y'
    if standard_experiment:
        algorithm = input("Enter the algorithm (random, greedy, hillclimb_train, hillclimb_connection or hillclimb_combined): ")
        return True, algorithm, 10, 20, 180, False, True
    else:
        iterations = int(input("Enter the number of iterations: "))
        algorithm = input("Enter the algorithm (random, greedy, hillclimb_train, hillclimb_connection or hillclimb_combined): ")
        max_trains = int(input("Enter the maximum number of trains (max is 20): "))
        if max_trains > 20:
            print("Warning: Setting max_trains greater than 20 will not work.")
        max_time = int(input("Enter the maximum time for the experiment in minutes: "))
        visualise_plot = input("Do you want to visualize the plot? (y/n): ").lower() == 'y'
        visualise_map = input("Do you want to visualize the map? (y/n): ").lower() == 'y'

        return False, algorithm, iterations, max_trains, max_time, visualise_plot, visualise_map

def visualize_data(stations_trains: str, coords_data: list, visualise_plot: bool=True, visualise_map: bool=True):
    """
    Function to visualize the train stations and trajects using specified options.
    """
    train_data = process_input(stations_trains)

    if visualise_plot:
        plot_trains(coords_data, train_data)

    if visualise_map:
        coords_dict = format_coordinates(train_data, coords_data)
        create_map_plot(coords_dict, coords_data)

if __name__ == "__main__":
    args = parse_arguments()

    # Prompt user for input if arguments are not provided
    if not all(vars(args).values()):
        print("Please specify the iterations, algorithm, max trains, max time, and visualization options you want to run.")
        standard_experiment, algorithm, iterations, max_trains, max_time, visualise_plot, visualise_map = get_user_input()

    else:
        iterations = args.iterations
        algorithm = args.algorithm
        max_trains = args.max_trains
        max_time = args.max_time
        visualise_plot = args.visualise_plot
        visualise_map = args.visualise_map

    # Run an experiment with specified algorithm and specified number of iterations
    current_experiment = Experiment("data/ConnectiesNationaal.csv", iterations, algorithm)
    stations_trains, score_list, ridden_count = current_experiment.run_experiment(max_trains, max_time)

    # Visualize the data of the experiment
    visualize_data(stations_trains, coords_data, visualise_plot, visualise_map)

    pathname = current_experiment.path_name(summary=True)

    current_experiment.summary_experiment()
