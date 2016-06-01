"""
Robot extension to be used with vrep's Pioneer robot used in simulation.
"""
from wrep import Simulation, Robot, vrep
from time import sleep
import sys
import math

class Pioneer(Robot):
    """
    Pioneer robot to be used in simulation.
    Only one robot can be created per process.
    """
    def __new__(cls, *args, **kwarg):
        if getattr(cls, 'created', False):
            raise Exception("Only one robot may be controlled by process.")
        cls.created = True
        return super(Pioneer, cls).__new__(cls)

    def __init__(self, simulation, name, robot_number=None):
        super(Pioneer, self).__init__(simulation, "Pioneer_p3dx#{nn}".format(nn=robot_number))
        self._name = name

        if robot_number is None:
            robot_number = name
        print("Nazwa "+str(name) +" numer "+ str(robot_number))
        self.behavior = "idle"
        self.destination = None
        
        for i in range(1, 17):
            self.add_sensor(
                name="Pioneer_p3dx_ultrasonicSensor{n}#{nn}".format(n=i, nn=robot_number),
                sensor_type="proximity",
                key="proximity-{n}".format(n=i))

        self.add_motor(
            name="Pioneer_p3dx_leftMotor#{nn}".format(nn=robot_number),
            key="left")

        self.add_motor(
            name="Pioneer_p3dx_rightMotor#{nn}".format(nn=robot_number),
            key="right")

        self.add_sensor(
            name=None,
            sensor_type="position",
            key="position",
            component=self)

        self.add_sensor(
            name=None,
            sensor_type="orientation",
            key="orientation",
            component=self)

        self.sensors["orientation"].read()
        self.sensors["position"].read()
        sleep(0.5)
        print("Orientacja POCZATKOWA: " + str(self.sensors["orientation"].read()))
        print("Polozenie POCZATKOWE: " + str(self.sensors["position"].read()))
        sleep(0.5)
        print("Orientacja POCZATKOWA 2: " + str(self.sensors["orientation"].read().ori[2]))
        print("Polozenie POCZATKOWE 2: " + str(self.sensors["position"].read().pos[0])+ str( self.sensors["position"].read().pos[1]))
        print("Starting communication for " + str(self.name) + ".\n")
        self.start_communication()
        print("Communication for " + str(self.name) + " started!\n")

    def __del__(self):
        # For sake of completeness, nothing guaranteed
        self.__class__.created = False
    def step(self):
        print("Begginning step")
        fun=getattr(self, self.behavior)
        fun()
        print("Ending step")
        sleep(0.5)
    def run(self):
        pos = self.sensors["position"].read()
        sleep(0.5)
        pos = self.sensors["position"].read()
        if pos is None:
            return
        pos=pos.pos
        status = self.sensors["orientation"].read()
        sleep(0.5)
        status = self.sensors["orientation"].read()
        if status is None:
            return
        current_o = status.ori[2]
        precision_p = 0.1
        precision_o = 0.05
        v_max_o = 5
        v_max_p = 2
        if current_o < 0:
            current_o = math.pi + (math.pi + current_o)

        d_p = (self.destination[0] - pos[0],self.destination[1] - pos[1])
        print("Dokad: " + str(d_p))
        desired_o = math.atan2(-d_p[1], -d_p[0])+math.pi
        d_o = desired_o - current_o
        k_p = math.sqrt(math.pow(d_p[0], 2) + math.pow(d_p[1], 2))
        v_p = min(v_max_p, k_p*v_max_p)
        k_o = min([abs(d_o), 2*math.pi-abs(d_o)])/(2*math.pi)
        v_o = k_o*v_max_o
        if d_o < -math.pi:
            v_right = -v_o 
            v_left = v_o
        elif d_o < 0:
            v_right = v_o 
            v_left = -v_o
        elif d_o < math.pi:
            v_right = -v_o 
            v_left = v_o
        else:
            v_right = v_o 
            v_left = -v_o
        print("Predkosc stala: " + str(v_o))
        print("Orientacja: " + str(current_o))
        print("Orientacja: " + str(self.sensors["orientation"].read()))
        print("Polozenie: " + str(self.sensors["position"].read()))
        self.motors["left"].velocity = v_left+v_p
        self.motors["right"].velocity = v_right+v_p
        sleep(0.5)
    def goto(self, pos):
        self.destination=pos
        self.behavior="run"
    def set_row(self):
        self.name
    def idle(self):
        self.motors["left"].velocity = 0
        self.motors["right"].velocity = 0

