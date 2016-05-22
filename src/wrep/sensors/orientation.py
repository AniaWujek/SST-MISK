"""
Orientation sensor
"""

from collections import namedtuple
from ..vrep import vrep
from .sensor import Sensor, sensors


class Orientation(Sensor):
    """
    Ultrasonic sensor, used to detect obstacles and surfaces.
    """

    result = namedtuple("Orientation", ["ori"])

    def __init__(self, simulation, name, component):
        self.type="orientation"
        self._reader = self.reader()
        self.component = component
        self.sim = simulation

    def read(self):
        """
        Get sensor reading.
        """
        return next(self._reader)

    def reader(self):
        """
        Generator used to supply sensor data in coherent way.
        Will return None until first sensor read is available, then will simply
        repeat last value until updated one will be provided.
        """
        vrep.simxGetObjectOrientation(self.sim.client_id, self.component.handle, -1, vrep.simx_opmode_streaming)

        val = None
        while True:
            ret, *state = vrep.simxGetObjectOrientation(self.sim.client_id, self.component.handle, -1, vrep.simx_opmode_buffer)

            if ret == 0:
                val = self.result(*state)

            yield val


sensors["orientation"] = Orientation
