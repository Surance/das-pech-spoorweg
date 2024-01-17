from code.classes.station import Station
from code.classes.connection import Connection
from code.classes.schedule import Schedule
import pandas as pd
import csv

def get_station_data(input_file):
    """
    Function that creates a pd dataframe from csv file with station info and coordinates
    """
    station_data_df = pd.read_csv(input_file)
    return station_data_df

def get_connection_data(input_file):
    """
    Function that creates a pd dataframe from csv file with connection info and time
    """
    connection_data_df = pd.read_csv(input_file)
    return connection_data_df

def create_connection(connection_data_df):
    """
    Function takes dataframe and creates list of connections
    """
    connections_list = []
    for _, row in connection_data_df.iterrows():
       connections_list.append(Connection(row['station1'], row['station2'], row['distance']))
    return connections_list

def create_station(station_data_df):
    """
    Function takes dataframe and creates list of stations 
    """
    stations_list = []
    for _, row in station_data_df.iterrows():
        stations_list.append(Station(row['station'], row['x'], row['y']))
    return stations_list

if __name__ == "__main__":
    # Input csv's
    station_data = get_station_data("data/StationsHolland.csv")
    connection_data = get_connection_data("data/ConnectionsHolland.csv")

    # Count scores and connections ridden per experiment
    score_count = 0
    ridden_count = 0

    iterations = 1000
    # TODO: find a way so it automatically calls it: algorithm_existing N + 1 
    algorithm = "random_2"
    max_trains = 7
    max_time = 120  # 2 hours

    # TODO: put the following in seperate file & function
    for trial in range(iterations):

        # Create objects
        all_stations = create_station(station_data)
        all_connections = create_connection(connection_data)

        schedule = Schedule(max_trains, max_time, all_connections)

        schedule.create_schedule()
        stations_trains, trial_score, trial_ridden = schedule.display_schedule(algorithm, trial)

        # Add score and number of ridden connections of trial to count
        score_count += trial_score
        ridden_count += trial_ridden
    
    # Save file with summary of the trials in the experiment 
    file_name = f"experiment/{algorithm}/EXPERIMENT_SUMMARY"

    with open(file_name, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        csv_writer.writerow(["Algorithm type", algorithm])
        
        csv_writer.writerow(["Number of Trials", iterations])

        csv_writer.writerow(["Average Score", score_count/iterations])

        csv_writer.writerow(["Average Connections Ridden", ridden_count/iterations])


    