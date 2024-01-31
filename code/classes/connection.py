class Connection:
    """
    Represents a connection between two train stations with associated travel time.

    Attributes:
        departure_station (str): The name of the departure train station.
        arrival_station (str): The name of the arrival train station.
        travel_time (int): The travel time between the departure and arrival stations in minutes.
    """
    
    def __init__(self, departure_station: str, arrival_station: str, travel_time: int) -> None:
        """
        Initializes a new Connection object with the provided attributes.
        """
        self.departure_station = departure_station
        self.arrival_station = arrival_station
        self.travel_time = travel_time