
import random
import time
from snake_wars.server import Server, SynchronisedServer
from snake_wars.client import Client
from snake_wars.commons import Direction
from snake_wars.learn import Reinforcement


def start_solo():
    """Local solo starting script"""
    Server(slots=2).start()

    for i in range(2):
        Client(580, 580).start()


def start_online():
    """
    Online starting script. Change the IP and port to connect
    to your desired server.
    """
    Client(580, 580, ip='116.203.85.179', port=5081).start()


class Example(Reinforcement):

    def __init__(self):
        super().__init__()

    def train(self):
        self.new_game()

        while True:
            time.sleep(0.25)
            self.loop(random.choice(list(Direction)))


def start_train():
    SynchronisedServer(slots=1).start()
    Example().start()


if __name__ == '__main__':

    # start_solo()
    # start_online()
    start_train()
