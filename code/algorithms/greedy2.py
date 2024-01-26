from code.classes.connection import Connection
from code.classes.schedule import Schedule
import random

class GreedySchedule:
    def __init__(self, schedule: Schedule) -> None:
        self.schedule = schedule

    def create_greedy_schedule(self) -> Schedule:
        """
        Function creates a schedule using greedy choice
        """