"""
TCP communication with broadcasting abilities.
"""
from socketserver import UnixStreamServer, ThreadingMixIn


class Server(UnixStreamServer, ThreadingMixIn):
    """
    TCP server using linux sockets to communicate.
    """
    pass