
import sys
import pygame
from multiprocessing import Process
from PodSixNet.Connection import connection, ConnectionListener

from snake_wars.commons import Direction, Size, Location
from snake_wars.client.entities import Snake, Food
from snake_wars.client import Renderer


class Client(ConnectionListener, Process):

    def __init__(self, screen_width: int = 480, screen_height: int = 480,
                 ip: str = "127.0.0.1", port: int = 5071):

        Process.__init__(self)
        ConnectionListener.__init__(self)

        # Set the screen size
        self.screen_size = Size(screen_width, screen_height)

        # Synchronization parameter
        self.step = 0

        # Init the id and grid_size, defined later by the server
        self.id = None
        self.grid_size = None
        self.renderer = None
        self.is_connected = False

        # Init a dict to store all snake.
        self.snakes = {}
        self.foods = {}

        # Connect to the server
        self.Connect(address=(ip, port))
        print(f"[Client] Starting complete > Connected to: {ip}:{port}")

    def run(self):

        while not self.lobby_loop():
            pass

        while True:
            self.game_loop()

    def lobby_loop(self):
        self.pump()

        if self.is_connected:
            return True

        return False

    def game_loop(self, *args, **kwargs):
        """Client loop. Refresh the game from the server."""

        self.pump()

        if self.is_connected:
            self.handle_keys()
            self.renderer.render(self.snakes.values(), self.foods)

    def handle_keys(self):
        """Handle the client key press."""

        for event in pygame.event.get():

            # If the player close the game, request a smooth disconnection
            if event.type == pygame.QUIT:
                connection.Send({"action": "disconnect"})

            # If the player press a direction button, send the direction to the server
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.send_state(Direction.UP)

                elif event.key == pygame.K_DOWN:
                    self.send_state(Direction.DOWN)

                elif event.key == pygame.K_LEFT:
                    self.send_state(Direction.LEFT)

                elif event.key == pygame.K_RIGHT:
                    self.send_state(Direction.RIGHT)

    def pump(self):
        """Refresh the connection with the server."""

        connection.Pump()
        self.Pump()

    @staticmethod
    def quit():
        """Close the Client."""

        pygame.quit()
        sys.exit()

    # NETWORK related functions
    # -------------------------------------------------------------------------

    def Network_authentication(self, data: dict):
        """
        Function triggered when the server respond to this client connection.
        The server return a randomly generated id and the size of the game's
        grid.

        :param data: The data send by the server.
        """
        message = data['message']

        # Save its own id and the game grid size
        self.id = message['id']
        self.grid_size = Size(
            message['grid_size'][0],
            message['grid_size'][1]
        )

        # Instantiate the renderer and set is_connected to True
        self.renderer = Renderer(self.screen_size, self.grid_size)
        self.is_connected = True

    def Network_add_players(self, data: dict):
        """
        Function triggered when the server send the information that
        a new player joined the game.

        :param data: The data send by the server.
        """
        message = data['message']

        # Create a local copy of the given snakes
        for player in message:

            self.snakes[player['id']] = Snake(
                Location(player['location'][0], player['location'][1])
            )

    def Network_game_state(self, data: dict):
        """
        Function triggered when the server send the positions of all
        Snakes in the game.

        :param data: The data send by the server.
        """
        message: dict = data['message']

        # Set the game step
        self.step = message['step']

        # Reset and create a local copy of each snake
        self.snakes = {}
        for player in message['players']:

            snake = Snake()
            snake.set_positions(player['positions'])

            self.snakes[player['id']] = snake

        # Reset and create a local copy of the given foods
        self.foods = {}
        for food in message['foods']:
            self.foods[food] = Food()

    def Network_disconnect(self, data: dict):
        """
        Function triggered when the server send a game over, or
        after the client requested to disconnect. Close the game client.
        """

        self.quit()

    def send_state(self, direction: Direction):
        """Send the direction of the client for this step."""

        connection.Send({"action": "state", "message": {
            'direction': direction.value,
            'step': self.step
        }})
