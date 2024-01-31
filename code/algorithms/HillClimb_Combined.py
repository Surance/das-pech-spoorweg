import random
import math
from copy import deepcopy
from code.classes.quality import calculate_quality
from code.algorithms.HillClimb_ConnectionList import HillClimber_connectionsUPDATE
from code.algorithms.HillClimb_Train import HillClimber_train
from code.algorithms.HillClimb_Connection import HillClimber_connections
from code.algorithms.greedy import GreedySchedule
from code.classes.schedule import Schedule

class HillClimber_combined:
    def __init__(self, schedule: Schedule) -> None:
        self.schedule = GreedySchedule(schedule).create_greedy_schedule()

    def run(self) -> Schedule:
        """
        Initialize a greedy schedule and run hillclimber_trains on it, after it converges, run hillclimber_connections on it,
        until it converges again. Return the best schedule.
        """

        train_climber = HillClimber_train(self.schedule)
        best_trains, best_ridden = train_climber.get_best_train() 
        self.schedule.trains = best_trains
        self.schedule.ridden = best_ridden

        print(len(self.schedule.trains))

        connection_climber = HillClimber_connectionsUPDATE(self.schedule)
        best_trains, best_ridden = connection_climber.get_best_connections()

        print(len(self.schedule.trains))

        return best_trains, best_ridden