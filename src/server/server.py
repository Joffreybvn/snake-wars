
import time
import random
from typing import Union, Dict, Iterable
from multiprocessing import Process
from PodSixNet.Server import Server as PodSixServer
from PodSixNet.Channel import Channel

from src.commons.utils import Coordinates, RandomCoordinates
from src.commons import Snake, Food


class Player(Channel):
    """Player socket representation on the server."""

    def __init__(self, *args, **kwargs):

        # Create a random id
        self.id = random.randint(0, 10000)
        self.snake: Union[Snake, None] = None

        super().__init__(*args, **kwargs)

    def create_snake(self):
        """Create a Snake at a random location in the game grid."""

        # Create a random spawn location for the Snake
        grid_size = self._server.grid_size
        location = RandomCoordinates(grid_size.x, grid_size.y)

        # Instantiate a new Snake
        self.snake = Snake(location, grid_size)

    # NETWORK related functions
    # -------------------------------------------------------------------------

    def Network(self, data):
        pass

    def Network_turn(self, data):
        """Handle client's input (turn left, right, top, bottom)."""

        self.snake.turn(data["message"])


class Server(PodSixServer, Process):

    channelClass = Player

    def __init__(self, ip: str = "127.0.0.1", port: int = 5071, slots: int = 1,
                 grid_size_x: int = 20, grid_size_y: int = 20,
                 food_spawn_rate: float = 0.15):

        Process.__init__(self)
        PodSixServer.__init__(self, localaddr=(ip, port))

        # Server address
        self.ip = ip
        self.port = port

        # Players (snakes) and food
        self.max_slots = slots
        self.players: Dict[int, Player] = {}
        self.foods = {}

        # Game constants
        self.grid_size = Coordinates(grid_size_x, grid_size_y)
        self.food_spawn_rate = food_spawn_rate

        print(f"[Server] Starting complete > Listening to: {self.ip}:{self.port}")

    def run(self):
        self.loop()

    def loop(self):

        while True:
            time.sleep(0.5)
            self.Pump()

            if len(self.players) == self.max_slots:
                self.__move_all()
                # self.__random_spawn_food()

                # Send updates to players
                self.update_positions()
                self.Pump()

    def __move_all(self):
        for player in self.players.values():
            player.snake.move()

    def __random_spawn_food(self):
        """
        Randomly spawn a food (or not), at a random position.
        """

        # Boolean random based on probability:
        if random.random() < self.food_spawn_rate:

            # Spawn a food at a random position
            position = RandomCoordinates(self.grid_size.x, self.grid_size.y)
            self.foods[position.tuple()] = Food(position)

    # NETWORK related functions
    # -------------------------------------------------------------------------

    def Connected(self, new_player: Player, address):
        """
        Function triggered when a new player connect to the server:
        Create a new player in the server; Send a message to all players
        about this new player; And send back a response to the newly
        connected player.

        :param new_player: A player channel Object.
        :param address: A tuple containing the (ip, port) the client connected to.
        :type new_player: ClientChannel
        :type address: tuple
        """

        print(f'[Server] ++ New client connected ++ Socket: {address[1]} - Id: {new_player.id}')

        # Create a Snake for this player
        new_player.create_snake()

        # Send the new player to all connected players
        for player in self.players.values():

            player.Send({"action": "add_players", "message": [{
                'id': new_player.id,
                'location': new_player.snake.get_head_position().tuple(),
            }]})

        # Save this new player
        self.players[new_player.id] = new_player

        # Send its id and the game size to the new player
        new_player.Send({"action": "authentication", "message": {
            'id': new_player.id,
            'grid_size': self.grid_size.tuple(),
        }})

        # Send all the players to the new player
        new_player.Send({"action": "add_players", "message": list(self.__get_all_players_data())})

    def __get_all_players_data(self) -> Iterable:
        """Return an iterator of all player's id and spawning location."""

        for player_id, player in self.players.items():

            yield {
                'id': player_id,
                'location': player.snake.get_head_position().tuple()
            }

    def update_positions(self):
        """Send all positions of all Snakes to all players."""

        # Get all player's snake positions
        all_positions = list(self.get_all_players_positions())

        # Send these positions to all players
        for player in self.players.values():
            player.Send({"action": "update_positions", "message": all_positions})

    def get_all_players_positions(self) -> Iterable:
        """Return an Iterable of all player's positions."""

        for player_id, player in self.players.items():

            yield {
                'id': player_id,
                'positions': list(player.snake.get_all_raw_positions())
            }
