class Connection:
    def __init__(self, departure_station: str, arrival_station: str, travel_time: int) -> None:
        self.departure_station = departure_station
        self.arrival_station = arrival_station
        self.travel_time = travel_time
    