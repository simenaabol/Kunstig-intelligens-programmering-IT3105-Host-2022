import sys # added!
sys.path.append("..") # added!


from sim_worlds.gambler import Gambler
from sim_worlds.cart import Cart
from sim_worlds.hanoi import Hanoi
from parameters import cartConfig, gamblerConfig, hanoiConfig


class Sim_world():
    def __init__(self, config):

        """ Set initial game configs here """

        if config["problem"] == "cart":
            self.problem = Cart()
        elif config["problem"] == "gambler":
            self.problem = Gambler()
        elif config["problem"] == "hanoi":
            self.problem = Hanoi(hanoiConfig["game_config"]['pegs'], hanoiConfig["game_config"]['discs'])
        else:
            raise Exception('Sim_world must be cart, gambler, or hanoi.')

        self.config = config

    def get_initial_game_state(self):

        self.problem.reset_game()
        return self.problem.get_state_key(), self.problem.game_done()[1], self.problem.get_legal_moves()

    def step(self, action):

        self.problem.take_action(action)
        
        return self.problem.get_state_key(), self.problem.game_done()[0], self.problem.game_done()[1], self.problem.get_legal_moves()

    def get_parameters(self):
        if self.config["problem"] == "cart":
            return cartConfig
        elif self.config["problem"] == "gambler":
            return gamblerConfig
        elif self.config["problem"] == "hanoi":
            return hanoiConfig