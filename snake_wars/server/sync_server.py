
from snake_wars.server import Server


class SynchronisedServer(Server):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def game_loop(self):
        """
        Synchronized game loop: Wait for the clients, the refresh and update
        the game state. Send the result to all clients.
        """

        while True:
            self.Pump()

            # If all players has updated their state
            if self.check_player_synchronisation():

                # Refresh player states
                self._move_all()
                self._eat_all()
                self._are_death()
                self._random_spawn_food()
                self.step += 1

                # Send updates to players
                self.update_positions()
                self.Pump()

                # Close this game loop if all players disconnected
                if len(self.players) == 0:
                    self.step = 0
                    break

    def check_player_synchronisation(self):
        """
        Check if all player has updated their state, and
        if their step is synchronized with the server.
        """

        # Get all player steps
        players_step = [player.step for player in self.players.values()]

        # Check if all players has the same step,
        # and if this step match the server step
        if len(set(players_step)) <= 1 and players_step[0] == self.step:
            return True

        return False
