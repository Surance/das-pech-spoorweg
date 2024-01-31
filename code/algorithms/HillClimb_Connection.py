import random
from copy import deepcopy
from code.classes.quality import calculate_quality
from code.algorithms.greedy import GreedySchedule
from code.classes.schedule import Schedule

class HillClimber_connections:
    """

    NOTES
    
    """
    def __init__(self, schedule: Schedule) -> None:
        self.schedule = GreedySchedule(schedule).create_greedy_schedule()
        self.best_score = float('-inf')
        self.best_schedule = None

    def delete_connection(self, schedule: Schedule) -> Schedule:
        """
        Delete a random connection from the schedule. 
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
        Add a random connection to the schedule. Update time and used connections
        """
             
        possible_connections = schedule.check_possible_connections()
        if len(possible_connections.keys()) == 0:
            return schedule
        
        train = random.choice(schedule.trains)
        print('add_function')
        print(train.connections_list)
        connection = random.choice(list(possible_connections.keys()))
        schedule.valid_connection(connection, possible_connections[connection])

        
        train.connections_list.append(connection)
        train.stations_names_list.append(possible_connections[connection])
        schedule.current_time += connection.travel_time
        schedule.ridden.add(connection)

        return schedule
    
    def get_best_connections(self) -> tuple[list, set]:
        """
        Randomly choose to delete or add a connection. If the quality is higher after the change, keep the schedule
        """
        print("NEW TRIAL ------------------------")
        for _ in range(10):
            copy_schedule = deepcopy(self.schedule)
            rand_int = random.randint(0, 1)
            if rand_int == 0:
                altered_schedule = self.delete_connection(copy_schedule)
                print(rand_int)
            else:
                altered_schedule = self.add_connection(copy_schedule)
                print(rand_int)
            # altered_schedule = random.choice([self.delete_connection(copy_schedule), self.add_connection(copy_schedule)])
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
        return calculate_quality(schedule.ridden, schedule.trains, schedule.total_connections)