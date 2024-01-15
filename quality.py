class Quality: 
    def __init__(self, ridden, trajects, all_connections):
        self.ridden = ridden
        self.trajects = trajects 
        self.all_connections = all_connections

    def calculate_quality(self):
        """
        Function calculates the quality of the created schedule using RailNL formula and returns value
        """
        # TODO: make into behaviour class? so you dont loop over same list 3484583838 times 
        p = len(self.ridden) / len(self.all_connections)
        T = len(self.trajects)
        Min = sum([traject.total_time for traject in self.trajects])
        K = p * 10000 - (T * 100 + Min)
        return K