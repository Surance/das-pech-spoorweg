import random
from code.classes.quality import Quality
from code.algorithms.random import Random_schedule

class HillClimb_connection:
    def __init__(self, schedule: classmethod) -> None:
        random_scheduler = Random_schedule(schedule)
        self.schedule = random_scheduler.create_random_schedule()
        self.best_score = float('-inf')
        self.best_schedule = None
        

    def delete_connection(self) -> None:
        """
        Delete a random connection from the schedule. Update time and used connections.
        """
        if len(self.schedule.trains) > 0:
            train_to_edit = random.choice(self.schedule.trains)

            if len(train_to_edit.connections_list) > 0:
                # Copy the train before making changes
                original_train = train_to_edit.copy_train()
                
                connection_to_remove = random.choice(train_to_edit.connections_list)
                station_to_remove = train_to_edit.stations_names_list[-1]

                # Remove the connection and station
                train_to_edit.connections_list.remove(connection_to_remove)
                train_to_edit.stations_names_list.remove(station_to_remove)
                self.schedule.current_time -= connection_to_remove.travel_time
                self.schedule.ridden.remove(connection_to_remove)


    def add_connection(self) -> classmethod:
        """
        Add a random connection to the schedule. Update time and used connections
        """
        possible_connections = self.schedule.check_possible_connections()
        if len(possible_connections.keys()) == 0:
            return self.schedule

        connection = random.choice(list(possible_connections.keys()))
        train_to_edit = random.choice(self.schedule.trains)

        # Create a copy of the train before making changes
        original_train = train_to_edit.copy_train()

        # Make changes to the train
        train_to_edit.connections_list.append(connection)
        train_to_edit.stations_names_list.append(possible_connections[connection])
        self.schedule.current_time += connection.travel_time
        self.schedule.ridden.add(connection)

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