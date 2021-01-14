
from enum import Flag


class Direction(Flag):
    """Enumerate the movement's direction of a snake."""

    # Direction = (x, y)
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    @staticmethod
    def list():
        """Return a list of all values."""

        return [d.value for d in Direction]
