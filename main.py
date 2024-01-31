import argparse

from code.classes.information import Information
from code.classes.experiment import Experiment
from code.visualisation.visualise import process_input
from code.visualisation.visualise import plot_trains
from code.visualisation.visualise import get_coordinates
from code.visualisation.visualise import coords_data
from code.visualisation.visualise2 import create_map_plot
from code.visualisation.visualise2 import format_coordinates

def parse_arguments():
    parser = argparse.ArgumentParser(description="Run an experiment with specified parameters.")
    parser.add_argument("--iterations", type=int, default=10, help="Number of iterations for the experiment.")
    parser.add_argument("--algorithm", type=str, default="hillclimb_train", help="Algorithm to use for the experiment.")
    parser.add_argument("--max_trains", type=int, default=20, help="Maximum number of trains for the experiment.")
    parser.add_argument("--max_time", type=int, default=180, help="Maximum time for the experiment in minutes.")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()

    # Input csv's
    data = Information("data/StationsNationaal.csv", "data/ConnectiesNationaal.csv")

    # Use command line arguments
    iterations = args.iterations
    algorithm = args.algorithm
    max_trains = args.max_trains
    max_time = args.max_time

    # Run an experiment with specified algorithm and specified number of iterations
    current_experiment = Experiment(data, iterations, algorithm, max_trains, max_time)
    stations_trains, score_list, ridden_count = current_experiment.run_experiment()


    # Calling both forms of visualise
    def visualize_data(stations_trains: str, coords_data: list, visualise_plot: bool=True, visualise_map: bool=True):
        """
        Function to visualise the train stations and trajects using specified options.
        """
        train_data = process_input(stations_trains)

        if visualise_plot:
            plot_trains(coords_data, train_data)

        if visualise_map:
            coords_dict = format_coordinates(train_data, coords_data)
            map_plot = create_map_plot(coords_dict, coords_data)

    # Example usage running experiment
    visualize_data(stations_trains, coords_data, visualise_plot=False, visualise_map=True)

    pathname = current_experiment.path_name(summary=True)

    data.summary_experiment(algorithm, pathname, iterations, score_list, ridden_count)