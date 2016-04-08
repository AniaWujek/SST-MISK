"""
Most generic motor type, base providing abilities to communicate with
remote and control effector.
"""

from .vrep import vrep


class Joint:
    """
    Generic motor representation, providing interface to control single joint.
    """
    def __init__(self, simulation, name):
        ret, handle = vrep.simxGetObjectHandle(simulation.client_id, name,
            vrep.simx_opmode_blocking)

        if ret != 0:
            raise Exception("Error code when accesing sensor: error {e}".format(e=ret))

        self.handle = handle
        self.sim = simulation
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


class Motor(Joint):
    """
    Joint extension used to set target velocity.
    """

    def __init__(self, simulation, name):
        super(Motor, self).__init__(simulation, name)
        self._velocity = 0
        self._position = None

    @property
    def position(self):
        return None

    @position.setter
    def position(self, value):
        pass

    @property
    def velocity(self):
        return _velocity

    @velocity.setter
    def velocity(self, value):
        ret = vrep.simxSetJointTargetVelocity(self.sim.client_id, self.handle, value,
            vrep.simx_opmode_oneshot)
        self._position = value
