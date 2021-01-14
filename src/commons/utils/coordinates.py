
import random


class Coordinates:
    """
    A simple 2D-coordinates class. Useful to store a position,
    or the size of a 2D grid.
    """

    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def tuple(self) -> tuple:
        """Return a tuple of coordinates."""

        return self.x, self.y


class RandomCoordinates(Coordinates):
    """
    A custom Coordinates class to instantiate automatically random
    coordinates from a given range.
    """

    def __init__(self, max_x: int = None, max_y: int = None):

        # Generate random coordinates given maximum coordinates
        x = random.randint(0, max_x)
        y = random.randint(0, max_y)

        super().__init__(x, y)
