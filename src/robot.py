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
            planner.next_step()


if __name__ == "__main__":
    parser = ArgumentParser(description="Robot control module")
    parser.add_argument("config", help="Path to environment configuration")
    parser.add_argument("name", help="Robot name", type = int)
    args = parser.parse_args()

    config = ConfigParser()
    config.read(args.config)

    main(args.name, config)
