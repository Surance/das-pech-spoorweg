class Train():
    def __init__(self, train_name: str) -> None:
        self.stations_names_list = []
        self.connections_list = []
        self.train_name = train_name
        self.total_time = 0

    def track_train_time(self) -> None:
        for connection in self.connections_list:
            self.total_time += connection.time