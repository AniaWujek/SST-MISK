"""
Move planner for robots
"""
import math

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

  def run_forever(self):
    print("Running...")
    #while True:
    if not self.cloud:
      x=-self.length/2
      y=-self.width/2+self.distances*int(self.robot.name)
      self.robot.goto([x,y])
    else:
      print("OR ELSE")