from StateManager import StateManager
from Actor import ANET
from MCTS.MonteCarloTreeSearch import MCTS

import numpy as np
import time

class RL_learner:

    def __init__(self, config):

        self.state_manager = StateManager(config)

        self.parameters = self.state_manager.get_parameters()

        self.actor = ANET(self.parameters['actor_config']['learning_rate'], 
                          self.parameters['actor_config']['hidden_layer_size'], 
                          self.parameters['actor_config']['activation_function'],
                          self.parameters['actor_config']['output_act'], 
                          self.parameters['actor_config']['optimizer'], 
                          self.parameters['actor_config']['loss_function'], 
                          self.parameters['actor_config']['epsilon'], 
                          self.parameters['actor_config']['epsilon_decay'],
                          self.state_manager)

        self.num_actual_games = config['num_actual_games']
        self.num_search_games = config['num_search_games']
        
        # self.starting_player = config['starting_player']

        self.minibatch_size = self.parameters['mcts_config']['minibatch_size']
        self.exploration_weight = self.parameters['mcts_config']['exploration_weight']
        self.epochs = self.parameters['mcts_config']['epochs']
        self.timout_max_time = self.parameters['mcts_config']['timout_max_time']

        self.save_interval = self.num_actual_games / 4 # Hvor ofte man lagrer nettverket
        
    def training(self):
        
        replay_buffer = []

        # Save the initial net
        # self.actor.save_net(0)
        
        for episode in range(self.num_actual_games):
            
            # Alternating which players' turn it is
            playing_player = episode % 2 + 1 # MULIG ENDRE
            
            self.state_manager.reset_game(playing_player)
            
            root_state = self.state_manager.get_state()
            
            monte_carlo = MCTS(self.exploration_weight, self.actor, self.state_manager)
            
            finished = self.state_manager.is_finished()

            while not finished:

                timeout_start_time = time.perf_counter()

                for search_game in range(self.num_search_games):

                    """ Mekke en Node class elns inni her. Typ hvordan thom gjør det. Denne skal
                    vel gjøre rollouts og sånn. Og backpropagating osv. """

                    monte_carlo.mcts() # KANSKJE GJØR OM NAVNET TIL DENNE, SIDEN DENNE DELEN ER LITT LIK NÅ

                    if time.perf_counter() - timeout_start_time > self.timout_max_time:
                        print("Game", search_game, "timeouted.")
                        break
            
                # Used for training the ANET
                distribution = monte_carlo.get_normalized_distribution()
                
                case_for_buffer = (root_state, distribution) # MENER DENNE ER GANSKE SMUD, MEN KANSKJE ENDRE LITT
                replay_buffer.append(case_for_buffer)
                
                action = None
                
                self.state_manager.do_move(action)
                
                root_state = self.state_manager.get_state()