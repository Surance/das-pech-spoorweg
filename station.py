class Station:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y 
    
    def StationInfo(self):
        print(f'{self.name} at {self.x}/{self.y}')
        