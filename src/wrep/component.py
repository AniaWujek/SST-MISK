"""
Module contains component class - responsible for managing API initialization
and handling object identity.
"""

from .vrep import vrep


class Component:
    """
    This class is a base for all effectors and actuators available.
    It handles common API connected elements, like component
    initialization.
    """
    def __init__(self, simulation, name):
        ret, handle = vrep.simxGetObjectHandle(simulation.client_id, name,
            vrep.simx_opmode_blocking)

        if ret != 0:
            raise Exception("Error code when accesing sensor: error {e}".format(e=ret))

        self.handle = handle
        self.sim = simulation
        self.name = name
