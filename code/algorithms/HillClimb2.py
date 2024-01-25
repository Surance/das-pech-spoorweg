from code.classes.quality import Quality
import random

class HillClimb2:
    def __init__(self, initial_solution):
        self.current_solution = initial_solution

    def random_change(self):
        """
        Perform a random change to the current solution by either adding or deleting a connection.
        """
        # Randomly decide whether to add or delete a connection
        action = random.choice(["add", "delete"])

        if action == "add":
            self.add_random_connection()
        elif action == "delete":
            self.delete_random_connection()

    def add_random_connection(self):
        """
        Add a random connection to the current solution.
        """
        # Implement logic to add a random valid connection
        possible_connections = self.current_solution.check_possible_connections()

        if len(possible_connections) > 0:
            connection = random.choice(list(possible_connections.keys()))
            station_to_add = possible_connections[connection]
            self.current_solution.valid_connection(connection, station_to_add)

    def delete_random_connection(self):
        """
        Delete a random connection from the current solution.
        """
        # Implement logic to delete a random connection while ensuring the solution remains valid
        if len(self.current_solution.trains) > 0:
            train_to_edit = random.choice(self.current_solution.trains)
            if len(train_to_edit.connections_list) > 1:
                connection_to_remove = random.choice(train_to_edit.connections_list)
                station_to_remove = train_to_edit.stations_names_list[-1]

                # Remove the connection and station
                train_to_edit.connections_list.remove(connection_to_remove)
                train_to_edit.stations_names_list.remove(station_to_remove)
                self.current_solution.current_time -= connection_to_remove.travel_time
                self.current_solution.ridden.remove(connection_to_remove)

    def hill_climb(self, iterations):
        """
        Perform hill climb algorithm.

        Parameters:
            - iterations (int): Number of iterations for the hill climb.
        """
        for _ in range(iterations):
            # Save the current solution before making changes
            current_solution_copy = self.current_solution.copy_schedule()

            # Perform a random change by either adding or deleting a connection
            self.random_change()

            # Calculate the new score for the modified solution
            new_score = Quality(self.current_solution.ridden, self.current_solution.trains, self.current_solution.total_connections).calculate_quality()

            # Calculate the score for the previous solution
            current_score = Quality(current_solution_copy.ridden, current_solution_copy.trains, current_solution_copy.total_connections).calculate_quality()

            # Decide whether to keep the modified solution or revert to the previous one
            if new_score > current_score:
                # Keep the modified solution
                pass
            else:
                # Revert to the previous solution
                self.current_solution = current_solution_copy
            
        return self.current_solution.trains, self.current_solution.ridden
    
    def get_final_solution(self):
        """
        Get the final solution after running the hill climb algorithm.

        Returns:
            - Schedule: The final schedule after hill climb.
        """
        return self.current_solution
