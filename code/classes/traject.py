class Traject():
    def __init__(self, traject_name):
        self.stations_names_list = []
        self.connections_list = []
        self.traject_name = traject_name
        self.total_time = 0

    def track_traject_time(self):
        for connection in self.connections_list:
            self.total_time += connection.time