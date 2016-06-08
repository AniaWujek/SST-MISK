try:
    import simplejson as json
except Exception:
    import json

import math
import os
import socket

from wrep.communication import Commutron
from socketserver import UnixStreamServer, BaseRequestHandler


class Cloud(BaseRequestHandler):
    """
    Cloud simulator.
    Only one can exist in the universe.
    """
    maxsize = 1024
    name = "BigScaryCloud_Bill"

    def __init__(self, center, radius, *args, **kwarg):
        self.center = center
        self.radius = radius
        self.max_concentration = 100;
        super(Cloud, self).__init__(*args, **kwarg)

    def handler(center, position):
        def actual_factory(*args, **kwargs):
            return Cloud(center, radius, *args, **kwargs)
        return actual_factory

    def concentration(self, pos):
        d = math.sqrt(math.pow(pos[0] - self.center[0], 2) + math.pow(pos[1] - self.center[1], 2))
        if d > self.radius:
            return 0
        return (self.radius - d)/self.radius * self.max_concentration


    def handle(self):
        raw = self.request.recv(self.maxsize).strip()
        data = json.loads(raw.decode("utf-8"))

        res = dict()
        res['concentration'] = self.concentration(data["position"])
        res['robot'] = data['robot']
        res['position'] = data['position']
        res['type'] = "cloudread"

        # Send response using single communication channel.
        # Generally it's bad pattern, but don't want to make async nor block
        # inside robot.
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as conn:
            conn.connect(os.path.join("/tmp/sst/", str(data["robot"])))
            conn.send(json.dumps(res).encode("utf-8"))
            conn.close()


if __name__ == "__main__":
    center = [-10, -17]
    radius = 5
    path = os.path.join("/tmp/sst/", Cloud.name)
    server = UnixStreamServer(path, Cloud.handler(center, radius))
    server.serve_forever()
