import random
from copy import deepcopy
from code.functions.quality import calculate_quality
from code.algorithms.greedy import GreedySchedule
from code.classes.schedule import Schedule

class HillClimber_connections:
    """
    Class for the HillClimber algorithm that makes changes on the connection level.

    Includes functions for deleting and adding connections to a train in the schedule, as well as a function that calculates
    the quality score of the schedule.
    The algorithm continues to initialize new schedules for a set number of iterations.
    """
    def __init__(self, schedule: Schedule) -> None:
        """
        Initializes the HillClimberConnections object.

        Args:
            schedule (Schedule): The schedule object to be modified using the HillClimber algorithm.
        """
        self.schedule = GreedySchedule(schedule).create_greedy_schedule()
        self.best_score = float('-inf')
        self.best_schedule = None
        self.iteration_count = 0

    def delete_connection(self, schedule: Schedule) -> Schedule:
        """
        Deletes a random connection from the schedule.

        Args:
            schedule (Schedule): The schedule from which a connection will be deleted.

        Returns:
            Schedule: The modified schedule after deleting a connection.
        """
        train = random.choice(schedule.trains)
        if not train.connections_list:
            return schedule

        connection = random.choice(train.connections_list)
        station = train.stations_names_list[-1]

        train.connections_list.remove(connection)
        train.stations_names_list.remove(station)

        schedule.current_time -= connection.travel_time
        schedule.ridden.remove(connection)
      
        return schedule
    
    def add_connection(self, schedule) -> classmethod:
        """
        Adds a random connection to the schedule. Updates time and used connections.

        Args:
            schedule (Schedule): The schedule to which a connection will be added.

        Returns:
            Schedule: The modified schedule after adding a connection.
        """
        possible_connections = schedule.check_possible_connections()
        if len(possible_connections.keys()) == 0:
            return schedule
        
        train = random.choice(schedule.trains)
        connection = random.choice(list(possible_connections.keys()))
        schedule.valid_connection(connection, possible_connections[connection])

        train.connections_list.append(connection)
        train.stations_names_list.append(possible_connections[connection])
        schedule.current_time += connection.travel_time
        schedule.ridden.add(connection)

        return schedule
    
    def get_best_connections(self) -> tuple[list, set]:
        """
        Randomly chooses to delete or add a connection. If the quality is higher after the change, keep the schedule.

        Returns:
            tuple[list, set]: A tuple containing the list of trains and the set of ridden connections in the best schedule.
        """
        print("NEW TRIAL CONNECTION------------------------")
        for _ in range(10000):
            copy_schedule = deepcopy(self.schedule)

            rand_int = random.randint(0, 1)

            if rand_int == 0:
                altered_schedule = self.delete_connection(copy_schedule)
                move = 'deletion'
            else:
                altered_schedule = self.add_connection(copy_schedule)
                move = 'addition'
            
            current_score = self.calculate_schedule_score(altered_schedule)

            if current_score > self.best_score:
                self.best_score = current_score
                self.best_schedule = altered_schedule
                print(f"Iteration: {self.iteration_count} | Move: {move} | Current Score: {current_score} | Best Score: {self.best_score} |")

            self.iteration_count += 1

        # After the loop, set the schedule to the best_schedule
        self.schedule = self.best_schedule

        return self.schedule.trains, self.schedule.ridden

    def calculate_schedule_score(self, schedule: Schedule) -> float:
        """
        Calculates the quality score for the current schedule.

        Args:
            schedule (Schedule): The schedule for which the quality score will be calculated.

        Returns:
            float: The quality score of the schedule.
        """
        return calculate_quality(schedule.ridden, schedule.trains, schedule.total_connections)