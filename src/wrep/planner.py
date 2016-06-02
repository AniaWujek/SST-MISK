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
    self.cloud = False
    no_robots = config["robots"]["count"]
    max_spaces = config["robots"]["sensor_range"] * config["robots"]["precision_range"]
    no_paths = math.ceil(config["board"]["width"] / (max_spaces * no_robots))
    self.spaces = config["board"]["width"] / no_paths
    self.no_paths = self.spaces/no_robots

  def run_forever(self):
    while True:
      if not self.cloud:
        robot.goto