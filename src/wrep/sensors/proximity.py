"""
Proximity sensor, used for obstacle detection.
"""

from collections import namedtuple
from ..vrep import vrep
from .sensor import Sensor, sensors


class ProximitySensor(Sensor):
    """
    Ultrasonic sensor, used to detect obstacles and surfaces.
    """

    result = namedtuple("ProximityData", ["state", "point", "handle", "normal"])

    def __init__(self, name, simulation):
        super(ProximitySensor, self).__init__(name, simulation,
            type="proximity")
        self._reader = self.reader()

    @property
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
        vrep.simxReadProximitySensor(self.sim.client_id, self.handle,
            vrep.simx_opmode_streaming)

        val = None
        while True:
            ret, *state = vrep.simxReadProximitySensor(self.sim.client_id, self.handle,
                vrep.simx_opmode_streaming)

            if ret == 0:
                val = self.result(*state)

            yield val


sensors["proximity"] = ProximitySensor
