from code.classes.information import Information
from code.classes.experiment import Experiment

from code.visualisation.visualise import process_input
from code.visualisation.visualise import plot_trains
from code.visualisation.visualise import get_coordinates
from code.visualisation.visualise import coords_data
from code.visualisation.visualise2 import create_map_plot
from code.visualisation.visualise2 import format_coordinates

if __name__ == "__main__":
    # Input csv's
    data = Information("data/StationsNationaal.csv", "data/ConnectiesNationaal.csv")

    iterations = 10
    algorithm = "hillclimb_train"
    max_trains = 20
    max_time = 180  # 3 hours

    # Run an experiment with specified algorithm and specified number of iterations
    current_experiment = Experiment(data, iterations, algorithm, max_trains, max_time)
    stations_trains, score_list, ridden_count = current_experiment.run_experiment()

    #Calling both forms of visualise
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