"""
Network communication between robots.
"""
import os
import threading

from queue import Queue
from socketserver import BaseRequestHandler
from .utilities.server import Server


class Commutron:
    """
    Commutron uses Unix named sockets in order to provide communication between
    robots.
    """

    def __init__(self, name):
        self.name = name
        self.queue = Queue()
        self._message = self.data()

        handler = BaseRequestHandler
        handler.handle = lambda handler: self.handle(handler)

        self.server = Server(os.path.join("/tmp/sst/", name), handler)
        server_thread = threading.Thread(target=self.server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()


    def handle(self, handler):
        data = handler.request.recv(1024).strip()
        self.queue.put(data)

    def data(self):
        while True:
            if not self.queue.empty():
                yield self.queue.get(block=False)
            else:
                yield None

    @property
    def message(self):
        return next(self._message)