import random
from code.classes.quality import Quality
from code.algorithms.random import Random_schedule

class HillClimber:
    def __init__(self, schedule):
        self.schedule = schedule
        self.best_score = float('-inf')
        self.best_schedule = None

    def set_initial_schedule(self, initial_schedule):
        """
        Set the initial schedule for the HillClimber.
        """
        self.schedule = initial_schedule

    def generate_random_schedule(self):
        """
        Use the Random_schedule algorithm to generate a random initial schedule.
        """
        random_schedule_generator = Random_schedule(self.schedule.max_trains, self.schedule.max_time, self.schedule.total_connections)
        self.schedule.trains, self.schedule.ridden = random_schedule_generator.create_random_schedule()

    def delete_connection(self):
        """
        Delete a random connection from the schedule. Update time and used connections.
        """
        connection = random.choice(self.schedule.ridden)
        self.schedule.ridden.remove(connection)
        self.schedule.trains[connection.train].connections.remove(connection)
        self.schedule.current_time -= connection.travel_time
      
        return self.schedule
    
    def add_connection(self):
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
    
    def get_best_connection(self):
        """
        Try deleting and replacing a deleted connection if the quality is higher with the new trajectory.
        """
        # Set the initial schedule before starting iterations
        initial_schedule = self.schedule.copy_schedule()

        for i in range(1000):
            self.set_initial_schedule(initial_schedule)  # Reset the schedule to the initial one
            self.delete_connection()
            self.add_connection()
            current_score = self.calculate_schedule_score()

            if current_score > self.best_score:
                self.best_score = current_score
                self.best_schedule = self.schedule.copy_schedule()

        # After the loop, set the schedule to the best_schedule
        self.schedule = self.best_schedule

        return self.schedule.trains, self.schedule.ridden

    def calculate_schedule_score(self):
        """
        Calculate the quality score for the current schedule.
        """
        return Quality(self.schedule.ridden, self.schedule.trains, self.schedule.total_connections).calculate_quality()