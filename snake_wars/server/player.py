
import random
from typing import Union
from PodSixNet.Channel import Channel

from snake_wars.server.entities import Snake
from snake_wars.commons import RandomLocation, Size


class Player(Channel):
    """Player socket representation on the server."""

    def __init__(self, *args, **kwargs):

        # Create a random id
        self.id = random.randint(0, 10000)
        self.snake: Union[Snake, None] = None

        # The client step - Used to check synchronization
        self.step = 0

        super().__init__(*args, **kwargs)

    def create_snake(self):
        """Create a Snake at a random location in the game grid."""

        # Create a random spawn location for the Snake
        grid_size: Size = self._server.grid_size
        location = RandomLocation(grid_size.width, grid_size.height)

        # Instantiate a new Snake
        self.snake = Snake(location, grid_size)

    def move(self):
        """Move its Snake and return its positions."""

        # Move the snake
        self.snake.move()

        # If the snake is still alive, return its positions
        if not self.snake.death:
            return list(self.snake.get_all_raw_positions())

        # If not, return an empty list
        return []

    # NETWORK related functions
    # -------------------------------------------------------------------------

    def Network(self, data):
        pass

    def Network_state(self, data):
        """
        Triggered when the client send its direction inputs.
        (turn left, right, top, bottom).
        """
        message = data['message']

        self.snake.turn(message["direction"])
        self.step = message['step']

    def Network_step(self, data):
        """
        Triggered when the client send its step.
        """
        self.step = data['message']

    def Network_disconnect(self, data):
        """
        Triggered when the client disconnect.
        """

        # Remove the client from the server
        self._server.disconnect_player(self, self.id)

