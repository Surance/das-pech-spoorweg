import random
from code.classes.quality import Quality
from code.algorithms.random import Random_schedule
from code.classes.schedule import Schedule

class HillClimber_train:
    def __init__(self, schedule: Schedule) -> None:
        self.schedule = Random_schedule(schedule).create_random_schedule()
        self.best_score = float('-inf')
        self.best_schedule = None

    def delete_train(self) -> classmethod:
        """
        Delete a random train from the schedule. 
        """
        train = random.choice(self.schedule.trains)
        self.schedule.trains.remove(train)
      
        return self.schedule
    
    def add_new_train(self) -> classmethod:
        """
        Add a random train to the schedule. Update time and used connections
        """
        self.schedule.add_train()

        # Add new stations to train if it connects to previous station until all connections are passed or max time is met
        while self.schedule.current_time < self.schedule.max_time and len(self.schedule.ridden) < len(self.schedule.total_connections):
            
            # Check which connections are possible with the previous arrival station
            possible_connections = self.schedule.check_possible_connections()

            if len(possible_connections.keys()) == 0:
                break
            
            # Pick a random connection from those that are possible
            connection = random.choice(list(possible_connections.keys()))

            self.schedule.valid_connection(connection, possible_connections[connection])

        self.schedule.train.total_time += self.schedule.current_time
        self.schedule.trains.append(self.schedule.train)
        
        return self.schedule
    
    def get_best_train(self) -> tuple[list, set]:
        """
        Try deleting and replacing a deleted train if the quality is higher with the new trajectory.
        """
        # Set the initial schedule before starting iterations
        initial_schedule = self.schedule

        for i in range(1000):
            self.delete_train()
            self.add_new_train()
            current_score = self.calculate_schedule_score()

            if current_score > self.best_score:
                self.best_score = current_score
                self.best_schedule = self.schedule.copy_schedule()

        # After the loop, set the schedule to the best_schedule
        self.schedule = self.best_schedule

        return self.schedule.trains, self.schedule.ridden

    def calculate_schedule_score(self) -> float:
        """
        Calculate the quality score for the current schedule
        """
        return Quality(self.schedule.ridden, self.schedule.trains, self.schedule.total_connections).calculate_quality()