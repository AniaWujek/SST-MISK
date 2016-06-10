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

    precision_p = 0.5
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
        if fun():
            return True
        sleep(0.5)
        return False

    def run(self):
        pos = self.sensors["position"].read()
        if pos is None:
            return None

        pos=pos.pos
        if math.sqrt( (pos[0] - self.destination[0])**2 + (pos[1] - self.destination[1])**2 ) < self.precision_p:
            #print("Robot: " + str(self.name) + "\n" + \
            #    "Pose: " + str(pos) + "\n" + \
            #    "Destination: " + str(self.destination) + "\n" + \
            #    "Lesser: " + str(abs(sum(x**2 for x in pos)-sum(x**2 for x in self.destination))) + "\n" + \
            #    "Bigger: " + str(self.precision_p))
            self.behavior = "rotate"
            return False

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

        velocity = self.obstacle_correction([v_left+v_p, v_right+v_p])

        self.motors["left"].velocity = velocity[0]
        self.motors["right"].velocity = velocity[1]        
        return False

    def rotate(self):
        #TODO
        #print("ON POSITION")
        #self.behavior = "idle"
        return True

    def goto(self, pos):
        self.destination=pos
        #print("Position for " + str(self.name) + " " + str(pos))
        self.behavior="run"


    def idle(self):
        self.motors["left"].velocity = 0
        self.motors["right"].velocity = 0
        sleep(0.2)
        return True

    def endofpath(self):
        print("Robot " + self.name + " ended.")
        self.behavior="ended"

    def wait(self):
        self.behavior="ended"

    def ended(self):
        self.motors["left"].velocity = 0
        self.motors["right"].velocity = 0
        sleep(0.2)
        return False


    def obstacle_correction(self, velocity):
        # [left, right]
        vel = velocity
        readings_good = False
        while not readings_good:
            readings = self.sensor_readings
            readings_good = True
            for r in readings:
                if readings[r] == None:
                    readings_good = False

        #print(readings)

        #interesuja nas czujniki od 1 do 8
        # frontowe to 4 i 5
        # prawy to 8
        # lewy to 1
        distances = [0,0,0,0,0,0,0,0]
        for i in range(8):
            s = "proximity-{nn}".format(nn=i+1)
            if readings[s].state == True:
                dist = math.sqrt(math.pow(readings[s].point[0],2)+math.pow(readings[s].point[1],2))
            else:
                dist = 100;
            distances[i]=dist
        min_dist = min(distances)

        # if self._name == 2:
        #     print(distances)
        
        scary_distance = 0.2

        if min_dist < scary_distance:
            min_dist_sensor = distances.index(min_dist)
            #print(self._name, min_dist_sensor)
            correction = 10*(scary_distance - min_dist)
            
            #przeszkoda z lewej, sensor 3 - straszna przeszkoda, sensor 0 - malo wazna
            if min_dist_sensor <= 3:
                correction = correction * min_dist_sensor
                print(correction)
                vel = [vel[0]+correction,vel[1]-correction]

            #przeszkoda z prawej, sensor 4 - straszna przeszkoda, sensor 7 - malo wazna
            else:
                correction = correction * (7 - min_dist_sensor)
                print(correction)
                vel = [vel[0]-correction,vel[1]+correction]


        return vel


        #print("sdfv")
    
    	
    	
    	
    	
    	
    	
    	
    	

