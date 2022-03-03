from StateManager import StateManager
from Actor import ANET

import numpy as np
import time

class RL_learner:

    def __init__(self, config):

        self.state_manager = StateManager(config)

        self.parameters = self.state_manager.get_parameters()

        self.actor = ANET(self.parameters['actor_config']['learning_rate'], 
                            self.parameters['actor_config']['hidden_layers'], 
                            self.parameters['actor_config']['activation_function'], 
                            self.parameters['actor_config']['output_act'], 
                            self.parameters['actor_config']['optimizer'], 
                            self.parameters['actor_config']['loss_function'], 
                            self.parameters['actor_config']['epsilon'], 
                            self.parameters['actor_config']['epsilon_decay'])

        self.num_actual_games = config['num_actual_games']
        self.num_search_games = config['num_search_games']

        self.minibatch_size = None # IDK tror denne brukes til trening elns
        self.save_interval = self.num_actual_games / 4 # Hvor ofte man lagrer nettverket

        self.replay_buffer = []


    def training(self):

        # Save the initial net
        self.actor.save_net()
        
        for episode in range(self.num_actual_games):

            # Alternating which players' turn it is
            playing_player = episode % 2 + 1 # Sykt smud linje men er kok

            print('Episode nr.', episode + 1)

            self.state_manager.reset_game()

            """ GJØR OM DENNE NÅR MCTS ER FERDIG """
            monte_carlo = None

            finished = self.state_manager.is_finished()

            while not finished:

                for search_game in range(self.num_search_games):

                    """ Mekke en Node class elns inni her. Typ hvordan thom gjør det. Denne skal
                    vel gjøre rollouts og sånn. Og backpropagating osv. """
                    monte_carlo.keeg_metode_som_bruker_tree_policy_og_rollout_backpropagate()

                    """ MULIGENS LEGGE TIL EN TIMEOUT FUNKSJON HER """

                # Used for training the ANET
                distribution = monte_carlo.get_distribution()

                # Numpy array representing the state
                state = self.state_manager.get_state()

                case_for_buffer = None # Thom: (np.concatenate(([player], state.flatten()), axis=None), distribution)
                self.replay_buffer.append(case_for_buffer)

                move_to_make = None  # Thom: np.unravel_index(np.argmax(distribution), simworld.get_grid().shape)

                self.state_manager.do_move(move_to_make)

                # Update the root
                monte_carlo.update_root(move_to_make)

            """ MULIGENS LAG EN PRINT FOR HVEM SOM VINNER """



            self.actor.update_epsilon()

            # Save the net according to the save interval
            if (episode + 1) % self.save_interval == 0:
                self.actor.save_net()