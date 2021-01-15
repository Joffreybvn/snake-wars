
from typing import Iterable
from snake_wars.commons import Location


class Snake:

    def __init__(self, start_location: Location = None):

        self.positions = [start_location]
        self.color = (17, 24, 47)

    def set_positions(self, positions: list):
        """
        Update the positions of the Snake from a given raw list of positions.
        :param positions: A list of raw positions.
        """

        # TODO: Create a lambda function
        def generate_positions() -> Iterable:
            for position in positions:
                yield Location(position[0], position[1])

        self.positions = list(generate_positions())

