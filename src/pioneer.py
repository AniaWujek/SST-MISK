"""
Robot extension to be used with vrep's Pioneer robot used in simulation.
"""
from wrep import Simulation, Robot


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

        self.start_communication()

    def __del__(self):
        # For sake of completeness, nothing guaranteed
        self.__class__.created = False

