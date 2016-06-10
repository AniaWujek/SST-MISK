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
        self.old_goto = None
        self.bug2_iter = 0
        #self.no_stages = self.width / self.spaces_width

        #TODO: zmienic podzial, dziala tylko dla kwadratow
        self.no_substages = self.length // 5
        #print(self.no_substages)
        self.substage_length= self.length / self.no_substages
        #print(self.substage_length)
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
            self.old_goto = [x,y]
        #else:
            #print("OR ELSE")

    def change_stage(self):
        if self.stage >= self.no_stages:
            print("Max stages: " + str(self.no_stages))
            print("Current stage: " + str(self.stage))
            self.robot.endofpath()
            return
        if self.substage >= self.no_substages:
            self.substage = 0
            self.stage = self.stage + 1
            print(str(self.robot.name) + " NEXT STAGE " + str(self.stage) + "/" + str(self.no_stages)) 
            return
        self.substage = self.substage + 1
        print(str(self.robot.name) + " NEXT SUBSTAGE " + str(self.substage)+ "/" + str(self.no_substages))   
    def next_substage(self, direction, x, y):
        #print(self.number)
        #print(self.others_status)
        #print(self.stage, self.substage)
        if not all((self.stage, self.substage) <= self.others_status[i] for i in self.others_status):
            #print(self.robot.name + " ommiting!")
            return
        self.robot.goto([direction * x + direction * self.substage_length * self.substage , y + self.distances/2])
        self.old_goto = [direction * x + direction * self.substage_length * self.substage , y + self.distances/2]
        self.change_stage()
        #print(str(self.robot.name) + " NO PHASE2 " + str(self.length / self.distances))
        
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

    def bug2(self):



        readings_good = False
        while not readings_good:
            readings = self.robot.sensor_readings
            readings_good = True
            for r in readings:
                if readings[r] == None:
                    readings_good = False

        distances = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        for i in range(16):
            s = "proximity-{nn}".format(nn=i+1)
            if readings[s].state == True:
                dist = math.sqrt(math.pow(readings[s].point[0],2)+math.pow(readings[s].point[1],2))
            else:
                dist = 100;
            distances[i]=dist

        distances = distances[4:]+distances[:4]

        obstacles = [i for i, v in enumerate(distances) if v < 1]

        min_dist = min(distances)
        min_sensor = distances.index(min_dist)

        

        if 3 < min_sensor < 12:
            #self.robot.destination = self.old_goto
            self.robot.goto(self.old_goto)
            return

        self.bug2_iter += 1

        pos = self.robot.sensors["position"].read()
        if pos is None:
            return None
        pos=pos.pos

        if self.bug2_iter > 20 and abs(pos[1] - self.old_goto[1]) < 0.001:
            #self.robot.destination = self.old_goto
            self.robot.goto(self.old_goto)
            self.bug2_iter = 0
            return

        angles = [10,30,50,90,90,130,150,170,190,210,230,270,270,310,330,350]
        #angles = [10,30,50,90,90,130,150,170,-170,-150,-130,-90,-90,-50,-30,-10]

        angle = (90 - angles[min_sensor]) * math.pi / 180.0

        if angles[min_sensor] < 180:
            angle = (360 - (90 - angles[min_sensor])) * math.pi / 180.0
        else:
            angle = (90 - (360 - angles[min_sensor])) * math.pi / 180.0

        status = self.robot.sensors["orientation"].read()
        if status is None:
            return None
        ori = status.ori[2]
        if ori < 0:
            ori = math.pi + (math.pi + ori)

        

        

        pos = self.robot.sensors["position"].read()
        if pos is None:
            return None
        pos=pos.pos

        

        z = 5.0
        print("first angle:",angle)
        angle = (angle + ori) % 2*math.pi
        dy = math.sin(angle+ori) * z
        dx = math.cos(angle+ori) * z
        if angle > math.pi:
            angle = 2*math.pi - angle
            dy = -math.sin(angle+ori) * z
            dx = math.cos(angle+ori) * z

        pos = [pos[0]+dx,pos[1]+dy]
        print("planner:",pos,angle)
        self.robot.goto(pos)

        #self.robot.delta_orientation = angle
        #self.robot.behavior = "rotate"

