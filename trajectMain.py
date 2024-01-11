import station 
import connection

class Traject():
    def __init__(self, traject_name):
        self.stations_names_list = []
        self.connections_list = []
        self.traject_name = traject_name
        self.total_time = 0

    def traject_stations(self):
        """List of train stations the traject passes to use for output"""
        self.stations_names_list.append(station.Station.name)
    
    def connections_traject(self):
        self.connections_list.append(connection.Connection())

    def track_traject_time(self):
        for connection in self.connections_list:
            self.total_time += connection.time