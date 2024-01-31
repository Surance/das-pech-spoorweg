import random
import math
from copy import deepcopy
from code.classes.quality import calculate_quality
from code.algorithms.HillClimb_ConnectionList import HillClimber_connectionsUPDATE
from code.algorithms.HillClimb_Train import HillClimber_train2
from code.algorithms.HillClimb_Connection import HillClimber_connections
from code.algorithms.greedy import GreedySchedule
from code.classes.schedule import Schedule

class HillClimber_combined3:
    def __init__(self, schedule: Schedule, initial_temperature: float = 100.0, cooling_rate: float = 0.95, convergence_threshold: float = 0.001) -> None:
        self.schedule = GreedySchedule(schedule).create_greedy_schedule()
        self.best_score = float('-inf')
        self.best_schedule = None
        self.temperature = initial_temperature
        self.cooling_rate = cooling_rate
        self.convergence_threshold = convergence_threshold
        self.iteration_count = 0
        self.scores_over_iterations = []
        self.iteration_count_train = 0
        self.iteration_count_conn = 0

    def delete_train(self, schedule: Schedule) -> Schedule:
        """
        Delete a random train from the schedule. 
        """
        rand_int = random.randint(0, 5)
        for _ in range(rand_int):
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
    
    def delete_connections(self, schedule: Schedule) -> Schedule:
        """
        Delete connections from a random index to the end of the list. 
        """
        train = random.choice(schedule.trains)
        if not train.connections_list:
            return schedule

        index = random.randint(0, len(train.connections_list) - 1)
        connections_to_remove = train.connections_list[index:]
        station = train.stations_names_list[-1]

        for connection in connections_to_remove:
            train.connections_list.remove(connection)
            if connection in schedule.ridden:
                schedule.ridden.remove(connection)

        train.stations_names_list.remove(station)

        schedule.current_time -= sum(connection.travel_time for connection in connections_to_remove)

        return schedule

    def add_connection(self, schedule) -> classmethod:
        """
        Add a random connection to the schedule. Update time and used connections
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
    
 
    def get_best_combined_traject(self) -> tuple[list, set]:
        """
        Randomly choose to delete or add a train. If the quality is higher after the change, keep the schedule
        """
        print("NEW TRIAL TRAINS ------------------------")
        
        for _ in range(10000):
            copy_schedule = deepcopy(self.schedule)

            rand_int = random.randint(0, 1)

            if rand_int == 0:
                altered_schedule = self.delete_train(copy_schedule)
                move = 'deletion'
            else:
                altered_schedule = self.add_new_train(copy_schedule)
                move = 'addition'

            altered_schedule = random.choice([self.delete_train(copy_schedule), self.add_new_train(copy_schedule)])
            current_score = self.calculate_schedule_score(altered_schedule)

            if current_score > self.best_score:
                self.best_score = current_score
                self.best_schedule = altered_schedule
                print(f"Iteration: {self.iteration_count_train} | Move: {move} | Current Score: {current_score} | Best Score: {self.best_score} |")

            self.iteration_count_train += 1

            # Because of removes and adds train names are no longer correct so we need to rename them in correct order 
            self.best_schedule.rename_trains()

            # After the loop, set the schedule to the best_schedule
            self.schedule = self.best_schedule

            print("NEW TRIAL CONNECTION ------------------------")
            while self.temperature > 1.0:
                copy_schedule = deepcopy(self.schedule)
                rand_int = random.randint(0, 1)
                if rand_int == 0:
                    altered_schedule = self.delete_connections(copy_schedule)
                    move = "Deletion"
                else:
                    altered_schedule = self.add_connection(copy_schedule)
                    move = "Addition"

                current_score = self.calculate_schedule_score(altered_schedule)
                self.scores_over_iterations.append(current_score)

                if current_score > self.best_score or random.uniform(0, 1) < math.exp((current_score - self.best_score) / self.temperature):
                    self.best_score = current_score
                    self.best_schedule = altered_schedule
                    print(f"Iteration: {self.iteration_count} | Move: {move} | Current Score: {current_score} | Best Score: {self.best_score} | Temperature: {self.temperature}")

                self.iteration_count += 1

                # Update temperature
                self.temperature *= self.cooling_rate

                # Check for convergence
                if self.iteration_count > 1 and abs(current_score - self.scores_over_iterations[-2]) < self.convergence_threshold:
                    print("Convergence achieved. Stopping the optimization.")
                    break

            # After the loop, set the schedule to the best_schedule
            self.schedule = self.best_schedule

            return self.schedule.trains, self.schedule.ridden


    def calculate_schedule_score(self, schedule: Schedule) -> float:
        """
        Calculate the quality score for the current schedule
        """
        return calculate_quality(schedule.ridden, schedule.trains, schedule.total_connections)
        

