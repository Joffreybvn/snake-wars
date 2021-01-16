
import time
import random
from typing import Union
from multiprocessing import Process
from snake_wars.commons import Direction
from snake_wars.client import SynchronizedClient


class Reinforcement(Process):

    def __init__(self):
        super().__init__()

        self.client: Union[SynchronizedClient, None] = None

    def new_game(self):
        """Start a new game session."""

        self.client = SynchronizedClient(580, 580)

    def loop(self, direction: Direction):
        """Run a game loop."""

        self.client.game_loop(direction)

    def run(self):
        self.train()

    def train(self):
        pass
