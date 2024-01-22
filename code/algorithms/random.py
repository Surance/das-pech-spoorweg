import random 
from classes.schedule import Schedule

class Random_schedule:
    def __init__(self):
    
    def create_random_schedule(self):
        """
        Function  creates a schedule of trains, taking in account the connections and the max time
        """

        # Create a new train every iteration until all connections are passed 
        while len(Schedule.ridden) < len(Schedule.total_connections):
            # Start train somewhere randomly
            Schedule.add_train()

            # Add new stations to train if it connects to previous station until all connections are passed or max time is met
            while Schedule.current_time < Schedule.max_time and len(Schedule.ridden) < len(Schedule.total_connections):
                
                # Check which connections are possible with the previous arrival station
                possible_connections = Schedule.check_possible_connections()

                if len(possible_connections.keys()) == 0:
                    break
                
                # Pick a random connection from those that are possible
                connection = random.choice(list(possible_connections.keys()))

                Schedule.valid_connection(connection, possible_connections[connection])

            Schedule.train.total_time += Schedule.current_time
            Schedule.trains.append(Schedule.train)
            
            # Break out of loop once the max number of trains has been met
            if len(Schedule.trains) >= Schedule.max_trains:
                break

        return Schedule.trains, Schedule.ridden