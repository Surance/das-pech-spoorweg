import random
from copy import deepcopy
from code.functions.quality import calculate_quality
from code.classes.schedule import Schedule
from code.algorithms.greedy import GreedySchedule


class HillClimber_train:
    """
    Class for HillClimber algorithm that makes changes on the train level.

    Includes a delete and add function that randomly deletes and adds trains to the schedule, 
    as well as a function that calculates the quality score of the schedule.
    
    Algorithm continues to initialise new trains for set amount of iterations. 
    When trains are re-added, they are initialised randomly
    """
    def __init__(self, schedule: Schedule) -> None:
        self.schedule = GreedySchedule(schedule).create_greedy_schedule()
        self.best_score = float('-inf')
        self.best_schedule = None
        self.iteration_count = 0

    def delete_train(self, schedule: Schedule, trains_to_change) -> Schedule:
        """
        Delete a random amount of trains from the schedule. Amount of trains to delete is given by trains_to_change.
        Also removes connections ridden by the train from the ridden set, so that score is calculated accurately.
        """
        for _ in range(trains_to_change):
            train = random.choice(schedule.trains)
            
            # Remove connections ridden by the train from the ridden set
            for connection in train.connections_list:
                if connection in schedule.ridden:
                    schedule.ridden.remove(connection)
            
            schedule.trains.remove(train)

        return schedule
    
    def add_new_train(self, schedule: Schedule, trains_to_change) -> Schedule:
        """
        Add a random amount of trains back to the schedule. Update time and used connections.
        Amount of trains to add is given by parameter trains_to_change.
        """
        # Don't add a new train if there are already a maximum of trains present in schedule 
        if len(schedule.trains) == schedule.max_trains: 
            return schedule 
        
        for _ in range(trains_to_change):
            schedule.add_train()

        # Add new stations to train if it connects to previous station until all connections are passed or max time is met
        while schedule.current_time < schedule.max_time and len(schedule.ridden) < len(schedule.total_connections):
            
            # Check which connections are possible with the previous arrival station
            possible_connections = schedule.check_possible_connections()

            if len(possible_connections.keys()) == 0:
                break
            
            # Pick a random connection from those that are possible
            connection = random.choice(list(possible_connections.keys()))

            schedule.valid_connection(connection, possible_connections[connection])

        schedule.train.total_time += schedule.current_time
        schedule.trains.append(schedule.train)
        
        return schedule
    
    def get_best_train(self) -> tuple[list, set]:
        """
        Randomly choose amount of trains to delete between 1 and 10 and then re-add. If the quality (score, denoted by K) 
        is higher after the change, keep the schedule. Otherwise return to deepcopy of original schedule. Displays information
        about the current iteration and the best score so far, when best score is updated
        """
        print("NEW TRIAL TRAINS ------------------------")
        for _ in range(1000):
            copy_schedule = deepcopy(self.schedule)
            
            trains_to_change = random.randint(1, 10) 

            altered_schedule = self.delete_train(copy_schedule, trains_to_change)
            
            altered_schedule = self.add_new_train(altered_schedule, trains_to_change)

            current_score = self.calculate_schedule_score(altered_schedule)

            if current_score > self.best_score:
                self.best_score = current_score
                self.best_schedule = altered_schedule
                print(f"Iteration: {self.iteration_count} | Trains changed: {trains_to_change} | Current Score: {current_score} | Best Score: {self.best_score} |")

            self.iteration_count += 1

        # Because of removes and adds train names are no longer correct so we need to rename them in correct order 
        self.best_schedule.rename_trains()

        # After the loop, set the schedule to the best_schedule
        self.schedule = self.best_schedule

        return self.schedule.trains, self.schedule.ridden

    def calculate_schedule_score(self, schedule: Schedule) -> float:
        """
        Calculate the quality score for the current schedule
        """
        return calculate_quality(schedule.ridden, schedule.trains, schedule.total_connections)