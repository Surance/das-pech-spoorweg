import random
from copy import deepcopy
from code.classes.quality import Quality
from code.algorithms.random import Random_schedule
from code.classes.schedule import Schedule

class HillClimber_train:
    def __init__(self, schedule: Schedule) -> None:
        self.schedule = Random_schedule(schedule).create_random_schedule()
        self.best_score = float('-inf')
        self.best_schedule = None

    def delete_train(self, schedule: Schedule) -> Schedule:
        """
        Delete a random train from the schedule. 
        """
        train = random.choice(schedule.trains)
        schedule.trains.remove(train)
      
        return schedule
    
    def add_new_train(self, schedule: Schedule) -> Schedule:
        """
        Add a random train to the schedule. Update time and used connections
        """
        # Don't add a new train if there are already a maximum of trains present in schedule 
        if len(schedule.trains) == schedule.max_trains: 
            return schedule 
        
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
        Randomly choose to delete or add a train. If the quality is higher after the change, keep the schedule
        """

        for i in range(1000):
            copy_schedule = deepcopy(self.schedule)
            altered_schedule = random.choice([self.delete_train(copy_schedule), self.add_new_train(copy_schedule)])
            current_score = self.calculate_schedule_score(altered_schedule)

            if current_score > self.best_score:
                self.best_score = current_score
                self.best_schedule = altered_schedule

        # After the loop, set the schedule to the best_schedule
        self.schedule = self.best_schedule

        return self.schedule.trains, self.schedule.ridden

    def calculate_schedule_score(self, schedule: Schedule) -> float:
        """
        Calculate the quality score for the current schedule
        """
        return Quality(schedule.ridden, schedule.trains, schedule.total_connections).calculate_quality()