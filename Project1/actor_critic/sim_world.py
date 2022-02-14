from ast import Continue
import sys 
sys.path.append("..") 

from sim_worlds.gambler import Gambler
from sim_worlds.cart import Cart
from sim_worlds.hanoi import Hanoi
from parameters import cartConfig, gamblerConfig, hanoiConfig


class Sim_world():
    def __init__(self, config):
        self.best_game = None

        if config["problem"] == "cart":
            self.problem = Cart(cartConfig['game_config']['L'], 
                                cartConfig['game_config']['Mp'], 
                                cartConfig['game_config']['g'], 
                                cartConfig['game_config']['t'], 
                                cartConfig['game_config']['Mc'], 
                                cartConfig['game_config']['x0'], 
                                cartConfig['game_config']['thM'], 
                                cartConfig['game_config']['nX'], 
                                cartConfig['game_config']['pX'], 
                                cartConfig['game_config']['T'], 
                                cartConfig['game_config']['step'], 
                                cartConfig['game_config']['nF'], 
                                cartConfig['game_config']['pF'])

        elif config["problem"] == "gambler":
            self.problem = Gambler(gamblerConfig['game_config']['win_prob'])

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

    def get_visualizing_data(self, actor, ep_step_count, least_steps_list):

        return self.problem.visualize(actor, ep_step_count, least_steps_list)

    def set_visualizing_data(self, list_of_states):
        if self.config["problem"] == "cart":
            Continue
        elif self.config["problem"] == "gambler":
            Continue
        elif self.config["problem"] == "hanoi":
            if self.best_game == None:
                self.best_game = list_of_states

            elif len(list_of_states) <  len(self.best_game):
                self.best_game = list_of_states

            
       
    # At the moment only used in Hanoi
    def render(self):
        if self.config["problem"] == "cart":
            Continue
        elif self.config["problem"] == "gambler":
            Continue
        elif self.config["problem"] == "hanoi":
            self.problem.get_graphic(self.best_game)

    

            

    
