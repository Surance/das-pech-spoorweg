import random
from code.classes.quality import Quality
from code.algorithms.random import Random_schedule

class HillClimber:
    def __init__(self, schedule: classmethod) -> None:
        self.schedule = Random_schedule.create_random_schedule(schedule) 
        self.best_score = float('-inf')
        self.best_schedule = None

    def delete_connection(self) -> None:
        """
        Delete a random connection from the schedule. Update time and used connections.
        """
        connection = random.choice(self.schedule.ridden)
        self.schedule.ridden.remove(connection)
        self.schedule.trains[connection.train].connections.remove(connection)
        self.schedule.current_time -= connection.travel_time
      
        return self.schedule
    
    def add_connection(self) -> classmethod:
        """
        Add a random connection to the schedule. Update time and used connections
        """
        possible_connections = self.schedule.check_possible_connections()
        if len(possible_connections.keys()) == 0:
            return self.schedule
        connection = random.choice(list(possible_connections.keys()))
        self.schedule.ridden.append(connection)
        self.schedule.trains[connection.train].connections.append(connection)
        self.schedule.current_time += connection.travel_time

        return self.schedule
    
    def get_best_train(self) -> tuple[list, set]:
        """
        Try deleting and replacing a deleted connection if the quality is higher with the new trajectory.
        """
        for i in range(1000):
            self.delete_connection()
            self.add_connection()
            current_score = self.calculate_schedule_score()

            if current_score > self.best_score:
                self.best_score = current_score
                self.best_schedule = self.schedule.copy_schedule()

        # After the loop, set the schedule to the best_schedule
        self.schedule = self.best_schedule

        return self.schedule.trains, self.schedule.ridden

    def calculate_schedule_score(self) -> float:
        """
        Calculate the quality score for the current schedule.
        """
        return Quality(self.schedule.ridden, self.schedule.trains, self.schedule.total_connections).calculate_quality()