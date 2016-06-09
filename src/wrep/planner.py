"""
Move planner for robots
"""
try:
        import simplejson as json
except Exception:
        import json

import math
from time import sleep

class Planner:
    """
    Planner is responsible for planning paths for each of the robots and coordinating their movement.
    """
    def __init__(self, robot, config):
        self.robot = robot
        self.config = config
        self.number = robot.name
        self.width = int(config["board"]["width"])
        self.length = int(config["board"]["length"])
        self.cloud = False
        self.no_robots = int(config["robots"]["count"])
        max_spaces = int(config["robots"]["sensor_range"]) * float(config["robots"]["precision_range"])
        self.no_stages = math.ceil(self.width / (max_spaces * self.no_robots))
        self.spaces_width = self.width / self.no_stages
        self.distances = self.spaces_width/self.no_robots
        #self.no_stages = self.width / self.spaces_width

        #TODO: zmienic podzial, dziala tylko dla kwadratow
        self.no_substages = self.length // 5
        print(self.no_substages)
        self.substage_length= self.length / self.no_substages
        print(self.substage_length)
        self.stage = 0
        self.substage = 0
        self.cloud_sensor = None
        self.others_status = {str(i): (0,0) for i in range(self.no_robots)}
        del self.others_status[str(self.number)]


    def check_mail(self):
        message = self.robot.commutron.message
        while message is not None:
            data = json.loads(message)
            if data["type"] == "cloudread":
                self.cloud_sensor = data["concentration"]
            if data["type"] == "progress":
                self.others_status[data["robot"]] = (data["stage"], data["substage"])
            message = self.robot.commutron.message

    def get_ready(self):
        #print("Running...")
        #while True:
        if not self.cloud:
            x=-self.length/2
            y=-self.width/2+self.distances*int(self.robot.name) + self.distances/2
            self.robot.goto([x,y])
        #else:
            #print("OR ELSE")

    def change_stage(self):
        if self.substage >= self.no_substages:
            #print("NEXT STAGE" + str(self.stage)) 
            self.substage = 0
            self.stage = self.stage + 1
            if self.stage >= self.no_stages:
                print("Max stages: " + str(self.no_stages))
                print("Current stage: " + str(self.stage))
                self.robot.endofpath()
            return
        #print(str(self.robot.name) + " NEXT SUBSTAGE " + str(self.substage))    
        self.substage = self.substage + 1
    def next_substage(self, direction, x, y):
        #print(self.number)
        #print(self.others_status)
        #print(self.stage, self.substage)
        if not all((self.stage, self.substage) <= self.others_status[i] for i in self.others_status):
            #print(self.robot.name + " ommiting!")
            return
        self.robot.goto([direction * x + direction * self.substage_length * self.substage , y + self.distances/2])
        #print(str(self.robot.name) + " NO PHASE2 " + str(self.length / self.distances))
        self.change_stage()
        
    def next_step(self):
        if not self.cloud:
            x=-self.length/2
            y=-self.width / 2 + self.distances * int(self.robot.name) + self.stage * self.spaces_width
            if self.stage % 2 == 0:
                self.next_substage(1, x, y)
            elif self.stage % 2 == 1:
                self.next_substage(-1, x, y)
        #else:
            #print("OR ELSE 2")
                        
    def broadcast_info(self):
        #print("Sending info!" + str(self.number))
        message = str(self.robot._name)+str(self.substage)
        message = dict()
        message["robot"] = self.robot.name
        message["stage"] = self.stage
        message["substage"] = self.substage
        message["type"] = "progress"
        self.robot.commutron.broadcast(json.dumps(message))
                
    def neighbors_sync(self):
            sync_left = False
            sync_right = False
            while not (sync_left and sync_right):
                    message = self.robot.commutron.message
                    if message is not None:
                            if (self.robot._name > 0 and message == str(self.robot._name-1)+str(self.substage)) or self.robot._name is 0: #jesli od sasiada z lewej
                                    sync_left = True 
                    sleep(0.2)          
            
    
    
    
    
    
    
