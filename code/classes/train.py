class Train():
    """
    Represents a train in the schedule.

    Attributes:
        stations_names_list (List[str]): The list of station names visited by the train.
        connections_list (List[Connection]): The list of connections taken by the train.
        train_name (str): The name of the train.
        total_time (int): The time the train spends riding the connections.
    """
    def __init__(self, train_name: str) -> None:
        """
        Initializes a new Train object.

        Args:
            train_name (str): The name of the train.
        """
        self.stations_names_list = []
        self.connections_list = []
        self.train_name = train_name
        self.total_time = 0

    def track_train_time(self) -> None:
        """
        Function tracks the total time spent by the train based on the connections taken.
        """
        for connection in self.connections_list:
            self.total_time += connection.time

    def copy_train(self) -> 'Train':
        """
        Function creates a copy of the current train and its attributes.

        Returns:
            Train: A copy of the current train.
        """
        # Create a copy of the current train and its attributes
        new_train = Train(self.train_name)
        new_train.stations_names_list = self.stations_names_list.copy()
        new_train.connections_list = self.connections_list.copy()
        new_train.total_time = self.total_time

        return new_train