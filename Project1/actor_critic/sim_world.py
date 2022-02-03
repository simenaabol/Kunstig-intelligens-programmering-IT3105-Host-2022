from sim_worlds.gambler import Gambler
from sim_worlds.cart import Cart
from sim_worlds.hanoi import Hanoi

class Sim_world():
    def __init__(self, config):

        """ Set initial game configs here """

        if config["problem"] == "cart":
            self = Cart()
        elif config["problem"] == "gambler":
            self = Gambler()
        elif config["problem"] == "hanoi":
            self = Hanoi()
        else:
            raise Exception('Sim_world must be cart, gambler, or hanoi.')

        self.config = config

    def reset_game_state(self):

        return self  # simworld, state, done?, legal moves
