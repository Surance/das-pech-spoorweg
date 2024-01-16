class Quality: 
    def __init__(self, ridden, trains, all_connections):
        self.ridden = ridden
        self.trains = trains 
        self.all_connections = all_connections

    def calculate_quality(self):
        """
        Function calculates the quality of the created schedule using RailNL formula and returns value
        """
        # TODO: make into behaviour class? so you dont loop over same list 3484583838 times 
        p = len(self.ridden) / len(self.all_connections)
        T = len(self.trains)
        Min = sum([train.total_time for train in self.trains])
        K = p * 10000 - (T * 100 + Min)
        return K