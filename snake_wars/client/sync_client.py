
from snake_wars.client import Client
from snake_wars.commons import Direction


class SynchronizedClient(Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        while not self.lobby_loop():
            pass

    def game_loop(self, direction: Direction):
        """Client loop. Refresh the game from the server."""

        self.pump()

        if self.is_connected:
            self.send_state(direction)
            self.renderer.render(self.snakes.values(), self.foods)
