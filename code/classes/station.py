class Station:
    """
    Represents a station with a x and y coordinate.

    Attributes:
        name (int): The name of the train station.
        x (float): The x coordinate of the station.
        y (float): The y coordinate of the station.

    """
    def __init__(self, name: int, x: float, y: float) -> None:
        """
        Initializes a new Station object with the provided attributes.
        """
        self.name = name
        self.x = x
        self.y = y