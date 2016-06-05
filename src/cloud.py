import math
from wrep.communication import Commutron

class Cloud():
    """
    Cloud simulator.
    Only one can exist in the universe.
    """
    
    def __init__(self, center, radius):
        self.name = "BigScaryCloud_Bill"
        self.center = center
        self.radius = radius
        self.max_concentration = 100;
        self.commutron = Commutron(self.name)
          
    def concentration(self, pos):
        d = math.sqrt(math.pow(pos[0] - self.center[0], 2) + math.pow(pos[1] - self.center[1], 2))
        if d > self.radius:
            return 0
        return (self.radius - d)/self.radius * self.max_concentration
        
    def check_mailbox(self):
        #print("cloud checking mailbox")
        message = self.commutron.message
        while message is not None:
            info = message.split("_")
            if len(info) is 3:
                robot = int(info[0])
                pos = [float(info[1]), float(info[2])]
                #self.commutron.send(robot, str(self.concentration(pos)))
                print("robot: ", robot, "sensor: ", self.concentration(pos))
            message = self.commutron.message
