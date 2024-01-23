from code.classes.connection import Connection
from code.classes.quality import Quality 

class HillClimbingScheduler:
    def __init__(self, schedule):
        self.schedule = schedule

    def hill_climbing_schedule(self, max_iterations=1000):
        i = 1
        best_score = float('-inf')  # Initialize the best score with negative infinity

        while i <= max_iterations:
            # Add random first train
            self.schedule.add_train()

            while self.schedule.current_time < self.schedule.max_time and len(self.schedule.ridden) < len(self.schedule.total_connections):
                # Check which connections are possible with the previous arrival station
                possible_connections = self.schedule.check_possible_connections()

                if len(possible_connections.keys()) == 0:
                    break

                # Sort connections by distance in ascending order (greedy choice)
                sorted_connections = sorted(possible_connections.keys(), key=lambda x: x.travel_time)

                # Select the first (shortest) connection
                connection = sorted_connections[0]

                self.schedule.valid_connection(connection, possible_connections[connection])

            # Calculate score for the current schedule
            current_score = self.calculate_schedule_score()

            # If the current schedule is better than the best known schedule, update the best schedule
            if current_score > best_score:
                best_score = current_score
                best_schedule = self.schedule.copy_schedule()

            i += 1

        return best_schedule.trains, best_schedule.ridden

    def calculate_schedule_score(self):
        # Calculate the score for the current schedule
        return Quality(self.schedule.ridden, self.schedule.trains, self.schedule.total_connections).calculate_quality()
