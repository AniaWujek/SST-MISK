"""
Robot extension to be used with vrep's Pioneer robot used in simulation.
"""
from wrep import Simulation, Robot
from time import sleep
import sys
import math
from wrep.vrep import vrep


class Pioneer(Robot):
    """
    Pioneer robot to be used in simulation.
    Only one robot can be created per process.
    """

    precision_p = 0.1
    precision_o = 0.05

    def __new__(cls, *args, **kwarg):
        if getattr(cls, 'created', False):
            raise Exception("Only one robot may be controlled by process.")
        cls.created = True
        return super(Pioneer, cls).__new__(cls)

    def __init__(self, simulation, name, config, robot_number=None):
        super(Pioneer, self).__init__(simulation, "Pioneer_p3dx#{nn}".format(nn=name))
        self.sim = simulation
        self.sensors = dict()
        self.motors = dict()
        self._name = name
        self.config = config

        if robot_number is None:
            robot_number = name
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
        self.start_communication()

    def __del__(self):
        # For sake of completeness, nothing guaranteed
        self.__class__.created = False

    def step(self):
        fun=getattr(self, self.behavior)
        fun()
        sleep(0.5)

    def run(self):
        pos = self.sensors["position"].read()
        if pos is None:
            return None

        pos=pos.pos
        if sum(x**2 for x in pos)-sum(x**2 for x in self.destination) < self.precision_p:
            self.behavior = "idle"
            return True

        status = self.sensors["orientation"].read()
        if status is None:
            return None


        current_o = status.ori[2]
        if current_o < 0:
            current_o = math.pi + (math.pi + current_o)
        d_p = (self.destination[0] - pos[0],self.destination[1] - pos[1])
        desired_o = math.atan2(-d_p[1], -d_p[0])+math.pi
        d_o = desired_o - current_o

        v_max_o = 5
        v_max_p = 2

        k_p = math.sqrt(math.pow(d_p[0], 2) + math.pow(d_p[1], 2))
        v_p = min(v_max_p, k_p*v_max_p)
        k_o = min([abs(d_o), 2*math.pi-abs(d_o)])/(2*math.pi)
        v_o = k_o*v_max_o
        if d_o < -math.pi:
            v_right = v_o 
            v_left = -v_o
        elif d_o < 0:
            v_right = -v_o 
            v_left = v_o
        elif d_o < math.pi:
            v_right = v_o 
            v_left = -v_o
        else:
            v_right = -v_o 
            v_left = v_o
        self.motors["right"].velocity = v_right+v_p
        self.motors["left"].velocity = v_left+v_p
        return False

    def goto(self, pos):
        self.destination=pos
        self.behavior="run"

    def set_row(self):
        goto
        self.name

    def idle(self):
        self.motors["left"].velocity = 0
        self.motors["right"].velocity = 0

