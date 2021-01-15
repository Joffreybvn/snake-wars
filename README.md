# Snake Wars

[![Generic badge](https://img.shields.io/badge/python-3.8%20%7C%203.9-blue)](https://www.python.org/downloads/release/python-380/)
[![Travis CI](https://travis-ci.com/Joffreybvn/snake-wars.svg?branch=master)](https://travis-ci.com/github/Joffreybvn/snake-wars)
[![Documentation Status](https://readthedocs.org/projects/snake-wars/badge/?version=latest)](https://snake-wars.readthedocs.io/en/latest/?badge=latest)

Snake game implementation for multiplayer and reinforcement learning.

### Installation
```
pip install snake-wars
```

### Get started - Solo player
Play alone, like a traditional snake

```Python
from snake_wars.server import Server
from snake_wars.client import Client

# Start a local server and connect the client to it
Server(slots=1).start()
Client(580, 580).start()
```

### Get started - Multiplayer
Play with your friends on a remote server

```Python
from snake_wars.client import Client

# Replace the ip with the ip of your server
# Same for the port
Client(580, 580, ip='127.0.0.1', port=5071).start()
```

### Launch a remote server
The easiest way to start a server on a VPS, Azure, AWS, ..., is to use the [Docker Image of the server](https://hub.docker.com/r/joffreybvn/snake-wars-server).
You can start it with a docker-compose.yml file:

```yaml
  snake:
    image: joffreybvn/snake-wars-server
    container_name: snake-wars-server
    restart: unless-stopped
    environment:
      PORT: 5071
      SLOTS: 2
      GRID_WIDTH: 20
      GRID_HEIGHT: 20
      FOOD_RATE: 0.15
    ports:
      - "5071:5071"
```

With this configuration, the game will start only when two players are connected.