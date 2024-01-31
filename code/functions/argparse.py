import argparse

def parse_arguments():
    """
    Adds an argument parser to the main.py file, so that the user can specify the number of iterations, algorithm, 
    maximum number of trains, maximum time, and visualization options.
    """
    parser = argparse.ArgumentParser(description="Run an experiment with specified parameters.")
    parser.add_argument("--iterations", type=int, help="Number of iterations for the experiment.")
    parser.add_argument("--algorithm", type=str, help="Algorithm to use for the experiment.")
    parser.add_argument("--max_trains", type=int, help="Maximum number of trains for the experiment (maximum is 20).")
    parser.add_argument("--max_time", type=int, help="Maximum time for the experiment in minutes.")
    parser.add_argument("--visualise_plot", action="store_true", help="Whether to visualize the plot.")
    parser.add_argument("--visualise_map", action="store_true", help="Whether to visualize the map.")

    return parser.parse_args()

def get_user_input():
    """
    If the user does not specify the arguments in the command line, this function prompts the user to enter the
    arguments manually one by one.
    """
    iterations = int(input("Enter the number of iterations: "))
    algorithm = input("Enter the algorithm (random, greedy, hillclimb_train, hillclimb_connection or hillclimb_combined): ")
    max_trains = int(input("Enter the maximum number of trains (maximum is 20): "))
    max_time = int(input("Enter the maximum time for the experiment in minutes: "))
    visualise_plot = input("Do you want to visualize the plot? (y/n): ").lower() == 'y'
    visualise_map = input("Do you want to visualize the map? (y/n): ").lower() == 'y'

    return iterations, algorithm, max_trains, max_time, visualise_plot, visualise_map
