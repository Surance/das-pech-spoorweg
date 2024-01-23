from .information import Information
from .schedule import Schedule
from code.algorithms.random import Random_schedule
from code.algorithms.Astar import AStarScheduler

class Experiment:
    def __init__(self, data, iterations, algorithm, max_trains, max_time):
        self.data = data
        self.iterations = iterations
        self.algorithm = algorithm
        self.max_trains = max_trains
        self.max_time = max_time
        
        # Count scores and connections ridden per experiment
        self.score_count = 0
        self.ridden_count = 0

    def run_experiment(self):
        # Create objects
        all_stations = Information.create_station(self.data)
        all_connections = Information.create_connection(self.data)
        pathname = Schedule.path_name(self.algorithm, self.algorithm)
        
        for trial in range(self.iterations):

            file_name = f"{pathname}experiment_{trial + 1}"

            schedule = Schedule(self.max_trains, self.max_time, all_connections)

            # Create a schedule depending on which algorithm is called
            if self.algorithm == "random":
                Random_schedule.create_random_schedule(schedule)
            
            elif self.algorithm == "Astar":
                astar_scheduler = AStarScheduler(schedule)
                optimal_schedule = astar_scheduler.create_optimal_schedule()

                # TODO: put outside of elif once A Star works
                if optimal_schedule:
                    optimal_schedule.display_schedule("A*", 1, save_each_output_as_csv=True)
                else:
                    print("Optimal schedule not found.")
            
            stations_trains, trial_score, trial_ridden = schedule.display_schedule(file_name, save_each_output_as_csv=True)

            # Add score and number of ridden connections of trial to count
            self.score_count += trial_score
            self.ridden_count += trial_ridden

        return stations_trains, self.score_count, self.ridden_count