from StateManager import StateManager
from Actor import ANET
from MCTS.MonteCarloTreeSearch import MCTS
from LiteModel import LiteModel

import numpy as np
import time

class RL_learner:

    def __init__(self, config):
        """Reinforcement learner class for training the neural network actor

        Args:
            config (dictionary): General configuration with parameters etc.
        """        

        self.state_manager = StateManager(config)

        self.parameters = self.state_manager.get_parameters()

        self.actor = ANET(None,
                          self.parameters['actor_config']['learning_rate'], 
                          self.parameters['actor_config']['hidden_layer_size'], 
                          self.parameters['actor_config']['activation_function'],
                          self.parameters['actor_config']['output_act'], 
                          self.parameters['actor_config']['optimizer'], 
                          self.parameters['actor_config']['loss_function'], 
                          self.parameters['actor_config']['epsilon'], 
                          self.parameters['actor_config']['epsilon_decay'],
                          self.state_manager)
        
        self.config = config

        self.num_actual_games = config['num_actual_games']
        self.num_search_games = config['num_search_games']

        self.minibatch_size = self.parameters['mcts_config']['minibatch_size']
        self.exploration_weight = self.parameters['mcts_config']['exploration_weight']
        self.epochs = self.parameters['mcts_config']['epochs']
        self.timout_max_time = self.parameters['mcts_config']['timout_max_time']

        self.save_interval = self.num_actual_games / config['saving_interval'] # Hvor ofte man lagrer nettverket
        
        self.save_nets = config['save_nets']

    def training(self):
        """Method for training the ANET
        """        

        replay_buffer = []

        # Save the initial net
        if self.save_nets:
            self.actor.save_net(0)
        
        for actual_game in range(self.num_actual_games):

            # Alternating which players' turn it is
            """ TIDLIGERE BRUKT I RESET GAME """
            playing_player = actual_game % 2 + 1

            # if episode % 10 == 0:
            print("Actual game nr.", actual_game + 1)

            self.state_manager.reset_game()

            monte_carlo = MCTS(self.exploration_weight, self.actor, self.state_manager)
            
            if actual_game % self.config['lite_model_interval'] == 0:
                lite_model = LiteModel.from_keras_model(self.actor.get_model())

            finished = self.state_manager.is_finished()

            while not finished:
    
                timeout_start_time = time.perf_counter()
                
                count = 0

                for search_game in range(self.num_search_games):
                    
                    # if search_game % 100 == 0:
                    #     print("Search game nr.", search_game)

                    monte_carlo.mcts(lite_model) # KANSKJE GJØR OM NAVNET TIL DENNE, SIDEN DENNE DELEN ER LITT LIK NÅ
                    
                    count += 1

                    if time.perf_counter() - timeout_start_time > self.timout_max_time:
                        print("Search game", search_game, "timeouted.")
                        break
                    
                print(count)

                # Used for cases in the replay buffer -> training the ANET
                distribution = monte_carlo.get_normalized_distribution()
                player = self.state_manager.get_playing_player()
                state = np.array(self.state_manager.get_state())

                """ DANGER ZONE """
                # Creating a case for the replay buffer with PID, state, and the distribution 
                case_for_buffer = (np.concatenate(([player], state.flatten()), axis=None), distribution) # MENER DENNE ER GANSKE SMUD, MEN KANSKJE ENDRE LITT
                replay_buffer.append(case_for_buffer)

                # Get the index for the largest value in the distribution and do the move.
                act_ind = np.array(np.argmax(distribution))
                move_to_make = self.state_manager.get_all_moves()[act_ind]
                self.state_manager.do_move(move_to_make)
                
                # Updates the root after doing the actual move
                monte_carlo.update_root(move_to_make)
                
                # Check if the game is in a final state
                finished = self.state_manager.is_finished()

            # winner = self.state_manager.get_winner()
            # print("Game finished! Player", winner, "won.")

            probs_for_rbuf = []
            """ LOWKEY DANGER ZONE """
            """ SE OVER DENNE HER """
            for i in range(len(replay_buffer)):
                probs_for_rbuf.append(i ** self.exploration_weight + 1e-10) # USIKKER HVOR INNHOLDET I APPENDEN KOMMER FRA

            probs_for_rbuf = probs_for_rbuf / np.sum(probs_for_rbuf)

            """ DANGER ZONE """
            """ SE OVER DENNE OG """
            if self.minibatch_size > 0:
                indices_for_minibatch = np.random.choice(len(replay_buffer), 
                                                        size=self.minibatch_size if self.minibatch_size <= len(replay_buffer) else len(replay_buffer), 
                                                        p=probs_for_rbuf, 
                                                        replace=False)

            else:
                indices_for_minibatch = np.random.choice(len(replay_buffer), 
                                                        size = int(len(replay_buffer)) * self.minibatch_size,
                                                        p = probs_for_rbuf,
                                                        replace = False)
                

            """ DANGER ZONE """
            minibatch = np.array(replay_buffer, dtype=object)[indices_for_minibatch.astype(int)]

            # Get states and distributions 
            x_train, y_train = zip(*minibatch)

            # Train the network with the cases from the minibatch
            self.actor.fit_network(np.array(x_train), np.array(y_train), self.epochs)

            # Update epsilon at the end of an episode
            self.actor.update_epsilon()

            # Save the net according to the save interval
            if (actual_game + 1) % self.save_interval == 0 and self.save_nets:
                self.actor.save_net(actual_game + 1)