class Train():
    def __init__(self, train_name: str) -> None:
        self.stations_names_list = []
        self.connections_list = []
        self.train_name = train_name
        self.total_time = 0

    def track_train_time(self) -> None:
        for connection in self.connections_list:
            self.total_time += connection.time

    def copy_train(self) -> 'Train':
        """
        Create a copy of the current train.
        """
        new_train = Train(self.train_name)
        new_train.stations_names_list = self.stations_names_list.copy()
        new_train.connections_list = self.connections_list.copy()
        new_train.total_time = self.total_time

        return new_train