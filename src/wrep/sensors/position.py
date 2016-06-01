"""
Proximity sensor, used for obstacle detection.
"""

from collections import namedtuple
from ..vrep import vrep
from .sensor import Sensor, sensors


class Position(Sensor):
    """
    Ultrasonic sensor, used to detect obstacles and surfaces.
    """

    result = namedtuple("Position", ["pos"])

    def __init__(self, simulation, name, component):
        self.type="position"
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
        vrep.simxGetObjectPosition(self.sim.client_id, self.component.handle, -1, vrep.simx_opmode_streaming)

        val = None
        while True:
            ret, *state = vrep.simxGetObjectPosition(self.sim.client_id, self.component.handle, -1, vrep.simx_opmode_buffer)

            if ret == 0:
                val = self.result(*state)
            else:
                val = None
            yield val


sensors["position"] = Position
