"""
Network communication between robots.
"""
import os
import threading
import socket

from queue import Queue
from socketserver import BaseRequestHandler
from .utilities.server import Server


class Commutron:
    """
    Commutron uses Unix named sockets in order to provide communication between
    robots.

    Currently the inteface is a subject of limitation - only the last initialized
    Commutron is able to receive message in the whole process.
    """
    path = "/tmp/sst/"

    def __init__(self, name):
        self.name = name
        self.queue = Queue()
        self._message = self.data()

        handler = BaseRequestHandler
        handler.handle = lambda handler: self.handle(handler)

        self.server = Server(os.path.join(self.path, name), handler)
        server_thread = threading.Thread(target=self.server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()

    def handle(self, handler):
        data = handler.request.recv(1024).strip()
        self.queue.put(data)

    def data(self):
        """
        Message generator.
        """
        while True:
            if not self.queue.empty():
                yield self.queue.get(block=False).decode("utf-8")
            else:
                yield None

    @property
    def message(self):
        """
        Contains last received message, retrievable once.
        If all messages were read, returns None.
        """
        return next(self._message)

    def broadcast(self, message):
        """
        Send message to all listening robots.
        """
        robots = [f for f in os.listdir(self.path) if f != self.name]
        for robot in robots:
            self.send(robot, message)
            #wyslano("print do robota "+str(robot))

    def send(self, robot_name, message):
        """
        Send a message directly to a robot.
        Note: the message should be 1024 characters or less.
        """
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as conn:
            conn.connect(os.path.join(self.path, robot_name))
            conn.send(message.encode("utf-8"))
            conn.close()
