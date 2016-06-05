#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
Script responsible for managing single robot.
"""

from argparse import ArgumentParser
from configparser import ConfigParser
from wrep import Simulation, Planner
from pioneer import Pioneer
from time import sleep
from wrep.communication import Commutron
import time

def main(name, environment):
    sim = Simulation(port_number=19870+name)
    robot = Pioneer(sim, name, environment["robots"])
    planner = Planner(robot, environment)
    robot.add_sensor(
        name=None,
        sensor_type="position",
        key="position",
        component=robot)
        
    robot.add_sensor(
        name=None,
        sensor_type="orientation",
        key="orientation",
        component=robot)
        
    #robot.goto([0,0])
    print("Begginning run forever")
    planner.run_forever()
    while True:        
        if robot.step():
            robot.commutron.broadcast(str(name)+str(planner.substage))
            sync_left = False
            sync_right = False
            while not (sync_left and sync_right):
                message = robot.commutron.message
                if message is not None:
                    if (name > 0 and message == str(name-1)+str(planner.substage)) or name is 0: #jesli od sasiada z lewej
                        sync_left = True 
                    if (name < 2 and message == str(name+1)+str(planner.substage)) or name is 2: #jesli od sasiada z prawej
                        sync_right = True
                time.sleep(0.2)                        
            planner.next_step()



if __name__ == "__main__":
    parser = ArgumentParser(description="Robot control module")
    parser.add_argument("config", help="Path to environment configuration")
    parser.add_argument("name", help="Robot name", type = int)
    args = parser.parse_args()

    config = ConfigParser()
    config.read(args.config)

    main(args.name, config)
