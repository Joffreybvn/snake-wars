
class Location:
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
