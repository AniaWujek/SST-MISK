#!/usr/bin/env python3
""" Test for wrep API """
from wrep import Simulation, Robot

sim = Simulation(port_number=19999)

robot = Robot(sim)

for i in range(1, 17):
    robot.add_sensor(
        name="Pioneer_p3dx_ultrasonicSensor{n}".format(n=i),
        sensor_type="proximity",
        key="proximity-{n}".format(n=i))

robot.add_motor(
    name="Pioneer_p3dx_leftMotor",
    key="left")

robot.add_motor(
    name="Pioneer_p3dx_rightMotor",
    key="right")
    
robot0 = Robot(sim)

for i in range(1, 17):
    robot0.add_sensor(
        name="Pioneer_p3dx_ultrasonicSensor{n}#0".format(n=i),
        sensor_type="proximity",
        key="proximity-{n}".format(n=i))

robot0.add_motor(
    name="Pioneer_p3dx_leftMotor#0",
    key="left")

robot0.add_motor(
    name="Pioneer_p3dx_rightMotor#0",
    key="right")
    
import time
robot.motors["left"].velocity = 100
time.sleep(5)
robot0.motors["left"].velocity = -100
time.sleep(5)
robot.motors["right"].velocity = 100
time.sleep(5)
robot0.motors["right"].velocity = -100

robot0.motors["left"].velocity = 100
time.sleep(5)
robot.motors["left"].velocity = -100
time.sleep(5)
robot0.motors["right"].velocity = 100
time.sleep(5)
robot.motors["right"].velocity = -100

print(robot.sensor_readings)

time.sleep(2)
print(robot.sensor_readings)

sim.close()
