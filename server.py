
# SERVER start script - Remote use only

from os import environ
from src.server import Server


# Port and server slots
PORT = int(environ.get('PORT', 5071))
SLOTS = int(environ.get('SLOTS', 2))

# Grid size
GRID_WIDTH = int(environ.get('GRID_WIDTH', 20))
GRID_HEIGHT = int(environ.get('GRID_HEIGHT', 20))

# Food spawn rate
FOOD_RATE = float(environ.get('FOOD_RATE', 0.15))


server = Server(ip="0.0.0.0", port=PORT, slots=SLOTS,
                grid_width=GRID_WIDTH, grid_height=GRID_HEIGHT,
                food_spawn_rate=FOOD_RATE)


if __name__ == '__main__':

    # Start the server
    server.start()
