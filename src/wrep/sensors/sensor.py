"""
Module containing generic sensor definition.
"""

from ..vrep import vrep
from ..component import Component

sensors = dict()


class Sensor(Component):
    """
    Generic sensor factory.
    This class is created without any information what data are
    measured, and thus should be used only as a base class
    for other sensors.
    """
    def __init__(self, name, simulation, type):
        super(Sensor, self).__init__(name, simulation)
        self.type = type

    @staticmethod
    def create(simulation, name, typ, *args, **kwarg):
        """
        Create sensor subtype.

        Currently available sensor types:
            - proximity - binary proximity sensor
        """
        cls = sensors[typ]
        return cls(simulation, name, *args, **kwarg)
