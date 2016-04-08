"""
Module containing generic sensor definition.
"""

from ..vrep import vrep


sensors = dict()


class Sensor:
    """
    Generic sensor definition, without any information what data are
    measured.
    """
    def __init__(self, simulation, name, type=None):
        ret, handle = vrep.simxGetObjectHandle(simulation.client_id, name,
            vrep.simx_opmode_blocking)

        if ret != 0:
            raise Exception("Error code when accesing sensor: error {e}".format(e=ret))

        self.handle = handle
        self.type = type
        self.sim = simulation
        self.name = name

    @staticmethod
    def create(simulation, name, type=None):
        cls = sensors.get(type, Sensor)
        return cls(simulation, name)
