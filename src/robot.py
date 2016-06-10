#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
Script responsible for managing single robot.
"""
try:
    import simplejson as json
except Exception:
    import json

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
    planner.get_ready()
    while True:
        pos = robot.sensors["position"].read().pos
        d = dict()
        d["robot"] = int(robot.name)
        pos = robot.sensors["position"].read().pos
        d["position"] = pos[0:2]
        robot.commutron.send("BigScaryCloud_Bill", json.dumps(d))
        planner.check_mail()
        time.sleep(0.2)
        decide = robot.step()
        if robot.obstacle:
            #mamy przeszkode
            print("obstacle")
            planner.bug2()
        else:
            robot.destination = planner.old_goto
        if planner.cloud:
            #mamy chmure
            print("cloud")
            robot.behavior = "idle"

        #print("DECISION " + str(robot.name) + " " + str(decide))
        if decide:
            planner.next_step()
        planner.broadcast_info()


if __name__ == "__main__":
    parser = ArgumentParser(description="Robot control module")
    parser.add_argument("config", help="Path to environment configuration")
    parser.add_argument("name", help="Robot name", type = int)
    args = parser.parse_args()

    config = ConfigParser()
    config.read(args.config)

    main(args.name, config)
