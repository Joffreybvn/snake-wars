
from itertools import chain
from typing import Dict
import numpy as np
from snake_wars.client import Client
from snake_wars.client.entities import Snake
from snake_wars.commons import Direction, Location, GameState


class SynchronizedClient(Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        while not self.lobby_loop():
            pass

    def play_step(self, direction: Direction):
        """Perform a game loop. Refresh the game from the server."""

        # Send the direction
        self.send_state(direction)
        self.pump()

        # Display the game
        self.renderer.render(self.snakes.values(), self.foods)

    def get_state(self) -> GameState:
        """
        Create and return a dictionary with the game state,
        from the point of view of this client's snake.
        """

        # Get client's own snake
        snake: Snake = self.snakes[self.id]
        head: Location = snake.get_head_position()

        # Get cells (x, y) location surrounding the head
        surroundings: Dict[str, tuple] = {
            'left': ((head.x - 1) % self.grid_size.width, head.y),  # left
            'right': ((head.x + 1) % self.grid_size.width, head.y),  # right
            'up': (head.x, (head.y - 1) % self.grid_size.height),  # up
            'down': (head.x, (head.y + 1) % self.grid_size.height)  # down
        }

        # Create a boolean list with the direction of the snake
        direction: Dict[str, bool] = {
            'left': snake.direction == Direction.LEFT.value,  # left
            'right': snake.direction == Direction.RIGHT.value,  # right
            'up': snake.direction == Direction.UP.value,  # up
            'down': snake.direction == Direction.DOWN.value  # down
        }

        # Get vectors of all foods coordinates and head coordinate
        foods = np.array(list(self.foods.keys()), dtype=int)

        # Return the data
        return GameState(head.tuple(), surroundings, direction, foods)

    def is_collision(self, location: tuple) -> bool:
        """
        Return True if there's a collision between the given location
        and any snake on the grid.
        """

        # Iterate over all positions of all snakes
        for pos in chain(snake.get_all_raw_positions() for snake in self.snakes.values()):

            # If there's a collision, return True
            if pos == location:
                return True

        return False
