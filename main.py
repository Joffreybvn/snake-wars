
from snake_wars.server import Server
from snake_wars.client import Client


def start_solo():
    """Local solo starting script"""
    Server(slots=1).start()
    Client(580, 580).start()


def start_online():
    """
    Online starting script. Change the IP and port to connect
    to your desired server.
    """
    Client(580, 580, ip='116.203.85.179', port=5081).start()


if __name__ == '__main__':

    # start_solo()
    start_online()
