"""
Move planner for robots
"""
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
    no_robots = int(config["robots"]["count"])
    max_spaces = int(config["robots"]["sensor_range"]) * float(config["robots"]["precision_range"])
    no_paths = math.ceil(self.width / (max_spaces * no_robots))
    self.spaces_width = self.width / no_paths
    self.distances = self.spaces_width/no_robots
    self.stage = 0
    self.substage = 0

  def run_forever(self):
    print("Running...")
    #while True:
    if not self.cloud:
      x=-self.length/2
      y=-self.width/2+self.distances*int(self.robot.name)
      self.robot.goto([x,y])
    else:
      print("OR ELSE")

  def change_stage(self):
    print("NEXT STAGE" + str(self.stage)) 
    self.substage = 0
    self.stage = self.stage + 1
    if self.stage > self.width / self.spaces_width:
      return
    self.next_step()
  def next_step(self):
    print(str(self.robot.name) + " NEXT PHASE " + str(self.substage))
    if not self.cloud:
      x=-self.length/2
      y=-self.width / 2 + self.distances * int(self.robot.name) + self.stage * self.spaces_width
      if self.stage % 2 == 0:
        self.robot.goto([x + self.distances * self.substage , y])
        print(str(self.robot.name) + " NO PHASE1 " + str(self.length / self.distances))
        if self.substage > self.length / self.distances:
          self.change_stage()
          return 
        self.substage = self.substage + 1
      elif self.stage % 2 == 1:
        self.robot.goto([- x - self.distances * self.substage , y])
        print(str(self.robot.name) + " NO PHASE2 " + str(self.length / self.distances))
        if self.substage > self.length / self.distances:
          self.change_stage()
          return 
        self.substage = self.substage + 1
    else:
      print("OR ELSE 2")
