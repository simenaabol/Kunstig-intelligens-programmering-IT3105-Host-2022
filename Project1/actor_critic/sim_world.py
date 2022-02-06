from sim_worlds.gambler import Gambler
from sim_worlds.cart import Cart
from sim_worlds.hanoi import Hanoi

class Sim_world():
    def __init__(self, config):

        """ Set initial game configs here """

        if config["problem"] == "cart":
            self.problem = Cart()
        elif config["problem"] == "gambler":
            self.problem = Gambler()
        elif config["problem"] == "hanoi":
            self.problem = Hanoi()
        else:
            raise Exception('Sim_world must be cart, gambler, or hanoi.')

        self.config = config

    def get_initial_game_state(self):

        """ Create game object from config and get states """
        return self.problem.get_state(), self.problem.game_over(), self.problem.get_legal_moves()

    def step(self, action):

        return self.problem.do_move(action)

