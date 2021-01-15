
import time
import random
from typing import Dict, Iterable
from multiprocessing import Process
from iteration_utilities import duplicates
from PodSixNet.Server import Server as PodSixServer

from snake_wars.commons import RandomLocation, Size
from snake_wars.server.entities import Food
from snake_wars.server import Player


class Server(PodSixServer, Process):

    channelClass = Player

    def __init__(self, ip: str = "127.0.0.1", port: int = 5071, slots: int = 1,
                 grid_width: int = 20, grid_height: int = 20,
                 food_spawn_rate: float = 0.15):

        Process.__init__(self)
        PodSixServer.__init__(self, localaddr=(ip, port))

        # Server address
        self.ip: str = ip
        self.port: int = port

        # Server state
        self.max_slots: int = slots

        # Players (snakes) and food
        self.players: Dict[int, Player] = {}
        self.foods = {}
        self.occupied_positions = []

        # Game constants
        self.grid_size = Size(grid_width, grid_height)
        self.food_spawn_rate: float = food_spawn_rate

        print(f"[Server] Starting complete > Listening to: {self.ip}:{self.port}")

    def run(self):

        while True:
            self.lobby_loop()
            self.game_loop()

    def lobby_loop(self):
        """Lobby loop: Run while waiting for all players to connect."""

        while True:
            self.Pump()

            if len(self.players) == self.max_slots:
                break

    def game_loop(self):
        """
        Game loop: Refresh and update the game state. Send the
        result to all clients.
        """

        while True:
            time.sleep(0.5)
            self.Pump()

            # Refresh player states
            self.__move_all()
            self.__eat_all()
            self.__are_death()
            self.__random_spawn_food()

            # Send updates to players
            self.update_positions()
            self.Pump()

            # Close game if all players disconnected
            if len(self.players) == 0:
                break

    def __move_all(self):
        self.occupied_positions = []

        # Move all players, get their positions
        for player in self.players.values():
            self.occupied_positions += player.move()

        # Remove the Snake that overlap another
        for pos in duplicates(self.occupied_positions):
            for player in self.players.values():

                if pos == player.snake.get_head_position().tuple():
                    player.snake.death = True

    def __eat_all(self):
        for player in self.players.values():

            if not player.snake.death:
                if pos := player.snake.is_eating_food(self.foods):

                    del self.foods[pos]

    def __are_death(self):

        players = {**self.players}  # Create a shallow copy
        for player_id, player in players.items():

            if player.snake.death:
                self.disconnect(player)
                del self.players[player_id]

    def __random_spawn_food(self):
        """
        Randomly spawn a food (or not), at a random position.
        """

        # Boolean random based on probability:
        if random.random() < self.food_spawn_rate:

            # Spawn a food at a random location
            location = RandomLocation(self.grid_size.width, self.grid_size.height)
            self.foods[location.tuple()] = Food(location)

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
        """Send all positions of all Snakes and foods to all players."""

        # Get all player's snake positions
        all_players_positions = list(self.get_all_players_positions())

        # Send these positions to all players
        for player in self.players.values():
            player.Send({"action": "update_positions", "message": {
                'players': all_players_positions,
                'foods': list(self.foods.keys())
            }})

    def get_all_players_positions(self) -> Iterable:
        """Return an Iterable of all player's positions."""

        for player_id, player in self.players.items():

            yield {
                'id': player_id,
                'positions': list(player.snake.get_all_raw_positions())
            }

    @staticmethod
    def disconnect(player: Player):
        """
        Send a Game Over to a death player. The player should
        disconnect once he receive this message.
        """

        player.Send({"action": "game_over"})
