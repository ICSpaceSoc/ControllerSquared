class TestSystem:
    def __init__(self, initial_x=0, gamma=0.1) -> None:
        self.x = initial_x
        self.gamma = gamma
        self.timestep = 0
    
    def following_function(self):
        if(self.timestep>100):
            return 1
        else:
            return 0
    
    def adjust(self, u):
        self.x += self.gamma*u
        self.timestep+=1

    