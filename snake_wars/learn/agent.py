
import time
from typing import Union
from multiprocessing import Process
from snake_wars.commons import Direction, GameState, Location
from snake_wars.client import SynchronizedClient


class Agent(Process):

    def __init__(self):
        super().__init__()

        self.client: Union[SynchronizedClient, None] = None

    def new_game(self):
        """Start a new game session."""

        self.client = SynchronizedClient(580, 580)
        time.sleep(0.05)

    def play_step(self, direction: Direction):
        """Trigger a game loop."""

        self.client.play_step(direction)

    def get_state(self) -> GameState:
        """Return the raw game state."""

        return self.client.get_state()

    def is_collision(self, location: tuple):
        """
        Wrapper for the client function. Return True if there's a collision
        between the given locatin and any snake on the game.
        """
        return self.client.is_collision(location)

    def run(self):
        self.train()

    def train(self):
        pass
