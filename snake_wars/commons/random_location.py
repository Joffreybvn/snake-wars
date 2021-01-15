
import random
from snake_wars.commons import Location


class RandomLocation(Location):
    """
    A custom Coordinates class to instantiate automatically random
    coordinates from a given range.
    """

    def __init__(self, max_x: int = None, max_y: int = None):

        # Generate random coordinates given maximum coordinates
        x = random.randint(0, max_x)
        y = random.randint(0, max_y)

        super().__init__(x, y)
