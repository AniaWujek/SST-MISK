"""
Most generic motor type, base providing abilities to communicate with
remote and control effector.
"""

from .vrep import vrep
from .component import Component

class Joint(Component):
    """
    Generic motor representation, providing interface to control single joint.
    """
    def __init__(self, simulation, name):
        super(Joint, self).__init__(simulation, name)
        self.name = name
        self._position = 0

    @property
    def position(self):
        return self._position  # TODO: check if introspection (encoders) are available

    @position.setter
    def position(self, value):
        vrep.simxSetJointTargetPosition(self.sim.client_id, self.handle, value,
            vrep.simx_opmode_oneshot)
        self._position = value


class Motor(Component):
    """
    Joint extension used to set target velocity.
    """

    def __init__(self, simulation, name):
        super(Motor, self).__init__(simulation, name)
        self._velocity = 0
        self._position = None

    @property
    def velocity(self):
        return _velocity

    @velocity.setter
    def velocity(self, value):
        ret = vrep.simxSetJointTargetVelocity(self.sim.client_id, self.handle, value,
            vrep.simx_opmode_oneshot)
        #print(ret)
        self._position = value
