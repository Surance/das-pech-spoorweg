import random 

class Random_schedule:
    def __init__(self, schedule):
        self.schedule = schedule

    def create_random_schedule(self):
        """
        Function  creates a schedule of trains, taking in account the connections and the max time
        """

        # Create a new train every iteration until all connections are passed 
        while len(self.ridden) < len(self.total_connections):
            # Start train somewhere randomly
            self.add_train()

            # Add new stations to train if it connects to previous station until all connections are passed or max time is met
            while self.current_time < self.max_time and len(self.ridden) < len(self.total_connections):
                
                # Check which connections are possible with the previous arrival station
                possible_connections = self.check_possible_connections()

                if len(possible_connections.keys()) == 0:
                    break
                
                # Pick a random connection from those that are possible
                connection = random.choice(list(possible_connections.keys()))

                self.valid_connection(connection, possible_connections[connection])

            self.train.total_time += self.current_time
            self.trains.append(self.train)
            
            # Break out of loop once the max number of trains has been met
            if len(self.trains) >= self.max_trains:
                break

        return self.trains, self.ridden