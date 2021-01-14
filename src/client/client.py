
import sys
import pygame
import random
from typing import Tuple
from multiprocessing import Process
from PodSixNet.Connection import connection, ConnectionListener

from src.commons.utils import Direction, Coordinates, RandomCoordinates
from src.commons import Snake, Food
from src.client import Renderer


class Client(ConnectionListener, Process):

    def __init__(self, screen_size_x: int = 480, screen_size_y: int = 480,
                 ip: str = "127.0.0.1", port: int = 5071):

        Process.__init__(self)
        ConnectionListener.__init__(self)

        # Set the screen size
        self.screen_size = Coordinates(screen_size_x, screen_size_y)

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
        self.loop()

    def loop(self):

        while True:
            connection.Pump()
            self.Pump()

            if self.is_connected:
                self.handle_keys()
                self.renderer.render(self.snakes.values(), self.foods.values())

        """
        while True:
            self.renderer.clock.tick(5)

            self.handle_keys()
            self.snakes[self.id].move()
            self.eat()

            self.random_spawn_food()
            self.renderer.render(self.snakes.values(), self.foods.values())
        """


    def eat(self):
        if pos := self.snakes[self.id].is_eating_food(self.foods):
            del self.foods[pos]

    def handle_keys(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    connection.Send({"action": "turn", "message": Direction.UP.value})

                elif event.key == pygame.K_DOWN:
                    connection.Send({"action": "turn", "message": Direction.DOWN.value})

                elif event.key == pygame.K_LEFT:
                    connection.Send({"action": "turn", "message": Direction.LEFT.value})

                elif event.key == pygame.K_RIGHT:
                    connection.Send({"action": "turn", "message": Direction.RIGHT.value})

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
        self.grid_size = Coordinates(
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
                Coordinates(player['location'][0], player['location'][1]),
                self.grid_size
            )

    def Network_update_positions(self, data: dict):
        """
        Function triggered when the server send the positions of all
        Snakes in the game.

        :param data: The data send by the server.
        """
        message: list = data['message']

        # Set the positions of each snake
        for player in message:
            self.snakes[player['id']].set_positions(player['positions'])
