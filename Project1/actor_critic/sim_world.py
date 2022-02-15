import sys 
sys.path.append("..") 

from sim_worlds.gambler import Gambler
from sim_worlds.cart import Cart
from sim_worlds.hanoi import Hanoi
from parameters import cartConfig, gamblerConfig, hanoiConfig

class Sim_world():
    def __init__(self, config):
        """ 

        This class acts like a hub for the games in the assignment. It feeds the learner
        all it needs to learn. Like states, legal actions, if the game is finished and so 
        on.

        PARAMS: config for the system

        """

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
                                cartConfig['game_config']['F'])

        elif config["problem"] == "gambler":
            self.problem = Gambler(gamblerConfig['game_config']['win_prob'])

        elif config["problem"] == "hanoi":
            self.problem = Hanoi(hanoiConfig["game_config"]['pegs'], 
                                hanoiConfig["game_config"]['discs'])
            
        else:
            raise Exception('Sim_world must be cart, gambler, or hanoi.')

        self.config = config

        # Used for visualization
        self.best_game = None


    def get_initial_game_state(self):
        """ 

        Resets the games and feeds the learner the initial state, if the game is finished, and
        the legal moves for this state.

        RETURNS: Initial state, is_finished, legal moves

        """

        self.problem.reset_game()

        return self.problem.get_state_key(), self.problem.game_done()[1], self.problem.get_legal_moves()


    def step(self, action, actor, parameters, episode):
        """

        Makes the learner do an action, and retrieves relevant values from this action.

        PARAMS: action, retrieved from the learner through the actor
        RETURNS: State, reward, is_finished, legal moves

        """

        self.problem.take_action(action)

        if self.config["problem"] == "cart":
            # print('Episode', episode)
            if episode == parameters['num_episodes']-10:
                actor.update_epsilon(0)
        elif self.config["problem"] == "hanoi":
            if episode == parameters['num_episodes']-10:
                actor.update_epsilon(0)

        
        # game_done[0] is reward, and game_done[1] is a boolean.
        return self.problem.get_state_key(), self.problem.game_done()[0], self.problem.game_done()[1], self.problem.get_legal_moves()


    def get_parameters(self):
        """ 

        Method for retrieving parameters for each toy problem.

        RETURNS: problem_config

        """

        if self.config["problem"] == "cart":
            return cartConfig
        elif self.config["problem"] == "gambler":
            return gamblerConfig
        elif self.config["problem"] == "hanoi":
            return hanoiConfig


    def get_visualizing_data(self, actor, ep_step_count, least_steps_list):
        """ 

        PARAMS: actor object, list of episodes and steps, list of steps
        RETURNS: x and y values for displaying learning

        """

        return self.problem.visualize(actor, ep_step_count, least_steps_list)


    def set_visualizing_data(self, list_of_states):
        """ 

        Method for setting the best game from the list of states

        PARAMS: list of states, from the learner
        
        """

        if self.config["problem"] == "cart":

            if self.best_game == None:
                self.best_game = list_of_states

            elif len(list_of_states) >= len(self.best_game):
                self.best_game = list_of_states

        elif self.config["problem"] == "hanoi":

            if self.best_game == None:
                self.best_game = list_of_states

            elif len(list_of_states) < len(self.best_game):
                self.best_game = list_of_states


    def render(self):
        """ 

        Method for visualizing more than the learning graph for problems
        that requires this. For example Hanoi, that needs the graphic visualization.

        """

        if self.config["problem"] == "cart":
            self.problem.get_graphic(self.best_game)

        elif self.config["problem"] == "hanoi":
            self.problem.get_graphic(self.best_game)