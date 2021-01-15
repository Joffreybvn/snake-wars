
from snake_wars.commons import Location


class Size(Location):

    def __init__(self, width: int = 0, height: int = 0):
        super().__init__(width, height)

    @property
    def width(self):
        return self.x

    @property
    def height(self):
        return self.y
