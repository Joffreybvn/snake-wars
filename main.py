
import time
from src.server import Server
from src.client import Client

server = Server(slots=2, food_spawn_rate=0.5)
# client = Client(580, 580)

if __name__ == '__main__':

    server.start()

    for i in range(2):

        Client(580, 580).start()
        time.sleep(2)
