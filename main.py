
import numpy as np
from scipy.spatial import distance

import random
from snake_wars.server import Server, SynchronisedServer
from snake_wars.client import Client
from snake_wars.commons import Direction, GameState
from snake_wars.learn import Agent


def start_solo():
    """Local solo starting script"""
    Server(slots=2).start()

    for i in range(2):
        Client(580, 580).start()


def start_online():
    """
    Online starting script. Change the IP and port to connect
    to your desired server.
    """
    Client(580, 580, ip='116.203.85.179', port=5081).start()


class Reinforcement(Agent):

    def __init__(self):
        super().__init__()

    def train(self):
        self.new_game()

        while True:
            self.play_step(random.choice(list(Direction)))
            state = self.get_state()
    
    def get_state(self):
        """Return the current state of the game as Numpy array of 0 and 1."""

        # Get the raw game state from the Agent
        state: GameState = super().get_state()

        # Find nearest food
        food = None
        if state.foods.any():

            # Math the city-block distance between head and all foods
            head = np.array([state.head], dtype=int)
            distances = distance.cdist(state.foods, head, metric='cityblock')

            # Save the nearest food
            nearest_indexes = np.where(distances == np.amin(distances))[0]
            food = state.foods[nearest_indexes[0]]

        # Check if there's possible collisions with the surroundings
        is_collision = {
            'left': self.is_collision(state.surroundings['left']),  # left cell
            'right': self.is_collision(state.surroundings['right']),  # right cell
            'up': self.is_collision(state.surroundings['up']),  # top cell
            'down': self.is_collision(state.surroundings['down'])  # bottom cell
        }

        # Return a binary array of the game state
        return np.array([

            # Danger straight
            (state.direction['left'] and is_collision['left']) or  # Goes left and danger left
            (state.direction['right'] and is_collision['right']) or  # Goes right and danger right
            (state.direction['up'] and is_collision['up']) or  # Goes up and danger up
            (state.direction['down'] and is_collision['down']),  # Goes down and danger down

            # Danger left
            (state.direction['left'] and is_collision['down']) or  # Goes left and danger down
            (state.direction['right'] and is_collision['up']) or  # Goes right and danger up
            (state.direction['up'] and is_collision['left']) or  # Goes up and danger left
            (state.direction['down'] and is_collision['right']),  # Goes down and danger right

            # Danger right
            (state.direction['left'] and is_collision['up']) or  # Goes left and danger up
            (state.direction['right'] and is_collision['down']) or  # Goes right and danger down
            (state.direction['up'] and is_collision['right']) or  # Goes up and danger right
            (state.direction['down'] and is_collision['left']),  # Goes down and danger left

            # Move direction
            *state.direction.values(),

            # Food location
            food is not None and food[0] < state.head[0],  # Food is on the left
            food is not None and food[0] > state.head[0],  # Food is on the right
            food is not None and food[1] < state.head[1],  # Food is up
            food is not None and food[1] > state.head[1],  # Food is down
        ], dtype=int)


def start_train():
    SynchronisedServer(slots=1).start()
    Reinforcement().start()


if __name__ == '__main__':

    # start_solo()
    # start_online()
    start_train()
