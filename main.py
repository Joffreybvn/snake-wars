
from src.server import Server
from src.client import Client


def start_solo():
    """Local solo starting script"""
    Server(slots=1).start()
    Client(580, 580).start()


def start_online():
    """
    Online starting script. Change the IP and port to connect
    to your desired server.
    """
    Client(580, 580, ip='127.0.0.1', port=5071)


if __name__ == '__main__':

    start_solo()
    # start_online()
