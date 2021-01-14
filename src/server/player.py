
import random
from typing import Union
from PodSixNet.Channel import Channel

from src.server.entities import Snake
from src.commons import RandomLocation, Size


class Player(Channel):
    """Player socket representation on the server."""

    def __init__(self, *args, **kwargs):

        # Create a random id
        self.id = random.randint(0, 10000)
        self.snake: Union[Snake, None] = None

        super().__init__(*args, **kwargs)

    def create_snake(self):
        """Create a Snake at a random location in the game grid."""

        # Create a random spawn location for the Snake
        grid_size: Size = self._server.grid_size
        location = RandomLocation(grid_size.width, grid_size.height)

        # Instantiate a new Snake
        self.snake = Snake(location, grid_size)

    # NETWORK related functions
    # -------------------------------------------------------------------------

    def Network(self, data):
        pass

    def Network_turn(self, data):
        """Handle client's input (turn left, right, top, bottom)."""

        self.snake.turn(data["message"])