from code.classes.connection import Connection
from code.classes.quality import Quality
from code.classes.schedule import Schedule  # Assuming you have a Schedule class

class HillClimbingScheduler:
    def __init__(self, schedule):
        self.schedule = schedule

    def hill_climbing_schedule(self, max_iterations=1000):
        i = 1
        best_score = float('-inf')

        while i <= max_iterations:
            self.schedule.add_train()

            while self.schedule.current_time < self.schedule.max_time and len(self.schedule.ridden) < len(self.schedule.total_connections):
                possible_connections = self.schedule.check_possible_connections()

                if len(possible_connections.keys()) == 0:
                    break

                sorted_connections = sorted(possible_connections.keys(), key=lambda x: x.travel_time)
                connection = sorted_connections[0]

                self.schedule.valid_connection(connection, possible_connections[connection])

            current_score = self.calculate_schedule_score()

            if current_score > best_score:
                best_score = current_score
                best_schedule = self.schedule.copy_schedule()

            i += 1

        return best_schedule.trains, best_schedule.ridden

    def calculate_schedule_score(self):
        return Quality(self.schedule.ridden, self.schedule.trains, self.schedule.total_connections).calculate_quality()
