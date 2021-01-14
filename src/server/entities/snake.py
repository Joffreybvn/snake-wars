
import random
from typing import Iterable, List
from src.commons import Direction, Location, Size


class Snake:

    def __init__(self, start_location: Location, grid_size: Size):

        self.grid_size = grid_size

        # Set position, direction and color of the snake
        self.positions: List[Location] = [start_location]
        self.direction = random.choice(Direction.list())
        self.color = (17, 24, 47)

        # Init the length and score values
        self.length = 1
        self.score = 0

    def get_head_position(self) -> Location:
        """Return the location of the Snake's head."""

        return self.positions[0]

    def get_all_raw_positions(self) -> Iterable[tuple]:
        """Return an Iterable of all positions as tuples."""

        for position in self.positions:
            yield position.tuple()

    def turn(self, direction: tuple):

        # Avoid the snake to turn on 180 degrees
        if self.length > 1 and (direction[0] * -1, direction[1] * -1) == self.direction:
            return

        # Else, set the new direction
        self.direction = direction

    def move(self):
        current_loc = self.get_head_position()
        x, y = self.direction

        # Math new head position
        # Modulo: When the snake reach a border, it appear on the other side.
        new_loc = Location(
            (current_loc.x + x) % self.grid_size.width,
            (current_loc.y + y) % self.grid_size.height
        )

        # If the snake eat itself, reset
        #if len(self.positions) > 2 and new_pos in self.positions[2:]:
        #    self.reset()

        #else:
        self.positions.insert(0, new_loc)

        if len(self.positions) > self.length:
            self.positions.pop()

    def is_eating_food(self, foods: dict):
        current_pos = self.get_head_position().tuple()

        for pos in foods.keys():
            if current_pos == pos:

                self.length += 1
                self.score += 1

                return pos

    # def reset(self):
    #    self.length = 1
    #    self.positions = [((screen_width/2), (screen_height/2))]
    #    self.direction = random.choice(Direction.list())
    #    self.score = 0
