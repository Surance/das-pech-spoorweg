from .traject import Traject
from .quality import Quality
import random

class Schedule:
    def __init__(self, max_trajects, max_time, total_connections):
        self.max_trajects = max_trajects 
        self.max_time = max_time
        self.total_connections = total_connections
        
        # Store traject classes in list
        self.trajects = []

        # Keep track of ridden connections for all trajects
        self.ridden = set()

    def create_schedule(self):
        """
        Function  creates a schedule of trains, taking in account the connections and the max time
        """

        # Create a new traject every iteration until all connections are passed 
        while len(self.ridden) < len(self.total_connections):
            # Start traject somewhere randomly 
            first_connection = random.choice(self.total_connections)
            traject_name = f"train_{len(self.trajects) + 1}"
            traject = Traject(traject_name)
            traject.stations_names_list.append(first_connection.departure_station)
            traject.stations_names_list.append(first_connection.arrival_station)
            current_time = 0

            # Add stations to traject if it connects to previous station until all connections are passed and max time is met
            while current_time < self.max_time and len(self.ridden) < len(self.total_connections):
                connection = random.choice(self.total_connections)
                departure_station = connection.departure_station
                arrival_station = connection.arrival_station

                # BUG: sorry ff heel lelijk maar anders blijft ie hangen
                if traject.stations_names_list[-1] == "Den Helder":
                    break

                # Only add new connection to traject if connection is possible with previous station
                if traject.stations_names_list[-1] == arrival_station and traject.stations_names_list[-2] != departure_station: 
                    traject.connections_list.append(connection)
                    traject.stations_names_list.append(departure_station)
                    current_time += connection.travel_time
                    
                    self.ridden.add(connection)
                
                # Only add new connection to traject if connection is possible with previous station
                elif traject.stations_names_list[-1] == departure_station: 
                    traject.connections_list.append(connection)
                    traject.stations_names_list.append(arrival_station)
                    current_time += connection.travel_time
                    
                    self.ridden.add(connection)
                
                
            traject.total_time += current_time
            self.trajects.append(traject)
            
            # Break out of loop once the max number of trajects has been met
            if len(self.trajects) >= self.max_trajects:
                break

            # BUG: doesnt have a objective to visit all connections, only focuses on limiting factors now

        return self.trajects, self.ridden

    def display_schedule(self):
        """
        Displays the schedule and score in the format as provided on ah.proglab.nl
        """
        stations_per_traject = []
        for traject_connections in self.trajects:
            stations = traject_connections.stations_names_list
            stations_per_traject.append(stations)
            print(f"{traject_connections.traject_name},\"{stations}\"")
        score = Quality(self.ridden, self.trajects, self.total_connections).calculate_quality()
        print(f"score,{score}")

        # To see if all connections have been passed:
        print(f"rode {len(self.ridden)} out of {len(self.total_connections)} connections")

        return stations_per_traject