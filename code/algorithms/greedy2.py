from code.classes.schedule import Schedule
import random

class GreedySchedule:
    def __init__(self, schedule: Schedule) -> None:
        self.schedule = schedule

    def create_greedy_schedule(self) -> Schedule:
        """
        Function creates a schedule using improved greedy choice with dynamic exploration
        """

        initial_exploration_prob = 0.5  # Initial exploration probability
        min_exploration_prob = 0.1  # Minimum exploration probability
        exploration_decay = 0.95  # Decay factor for exploration probability

        exploration_prob = initial_exploration_prob

        # Create a new train every iteration until all connections are passed 
        while len(self.schedule.ridden) < len(self.schedule.total_connections):
            # Start train somewhere randomly
            self.schedule.add_train()
            
            # Add new stations to train if it connects to the previous station until all connections are passed or max time is met
            while self.schedule.current_time < self.schedule.max_time and len(self.schedule.ridden) < len(self.schedule.total_connections):
                
                # Check which connections are possible with the previous arrival station
                possible_connections = self.schedule.check_possible_connections()

                if len(possible_connections.keys()) == 0:
                    break

                # Sort connections by distance in ascending order
                sorted_connections = sorted(possible_connections.keys(), key=lambda x: x.travel_time)

                # Introduce exploration vs. exploitation
                if random.random() < exploration_prob:
                    # Randomly choose a connection among the top ones
                    selected_connection = random.choice(sorted_connections[:min(2, len(sorted_connections))])
                else:
                    # Select the first (shortest) connection
                    selected_connection = sorted_connections[0]

                self.schedule.valid_connection(selected_connection, possible_connections[selected_connection])

            self.schedule.train.total_time += self.schedule.current_time
            self.schedule.trains.append(self.schedule.train)

            if len(self.schedule.trains) >= self.schedule.max_trains:
                break

            # Decay exploration probability
            exploration_prob = max(min_exploration_prob, exploration_prob * exploration_decay)

        return self.schedule
