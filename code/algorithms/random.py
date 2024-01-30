from code.classes.schedule import Schedule
import random 

class Random_schedule:
    def __init__(self, schedule: Schedule) -> None:
        self.schedule = schedule

    def create_random_schedule(self) -> Schedule:
        """
        Function  creates a schedule of trains, taking in account the connections and the max time
        """

        # Create a new train every iteration until all connections are passed 
        while len(self.schedule.ridden) < len(self.schedule.total_connections):
            # Start train somewhere randomly
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
            
            # Break out of loop once the max number of trains has been met
            if len(self.schedule.trains) >= self.schedule.max_trains:
                break
        
        # TODO: RETURN (self.schedule.)SCHEDULE INSTEAD OF TUPLE 
        return self.schedule