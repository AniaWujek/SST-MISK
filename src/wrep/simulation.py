"""
This module is responsible for estabilishing and maintaing communication with
remote VREP server.
"""

from wrep.vrep import vrep


class Simulation:
    """
    Class represents single simulation.

    It is expected to be instantiated exactly once. All API calls should be
    executed with the of this singletonic instance, as it provides valid
    and vital informations about connection to the main VREP server.

    Warning: When it is instanciated, all previous instances of it are
    invalidated.

    This class cannot be unit tested because of side effects from close
    integration with remote server.
    """

    def __init__(self, ip_addr='127.0.0.1', port_number=19999):
        """
        Instance initialization.

        When it is invoked, all previous connections to remote are closed and a
        new connection is established.
        """
        vrep.simxFinish(-1)

        client_id = vrep.simxStart(ip_addr, port_number, True, True, 5000, 5)
        if client_id == -1:
            raise IOError("Could not connect to remote")

        self.client_id = client_id

    @property
    def active(self):
        """
        Check if connection to remote is active.
        """
        return vrep.simxGetConnectionId(self.client_id)

    def close(self):
        """
        Close active connection to remote.
        """
        vrep.simxFinish(self.client_id)
