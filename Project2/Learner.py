from StateManager import StateManager
from Actor import ANET
from MCTS.MonteCarloTreeSearch import MCTS

import numpy as np
import time

class RL_learner:

    def __init__(self, config):

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

        self.num_actual_games = config['num_actual_games']
        self.num_search_games = config['num_search_games']

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

            # if episode % 10 == 0:
            print("Episode game nr.", episode+1)

            self.state_manager.reset_game(playing_player)

            monte_carlo = MCTS(self.exploration_weight, self.actor, self.state_manager)

            finished = self.state_manager.is_finished()

            while not finished:
                
                # print("DONE?", self.state_manager.is_finished())
    
                timeout_start_time = time.perf_counter()

                for search_game in range(self.num_search_games):
                    
                    # if search_game % 100 == 0:
                    # print("Search game nr.", search_game)

                    """ Mekke en Node class elns inni her. Typ hvordan thom gjør det. Denne skal
                    vel gjøre rollouts og sånn. Og backpropagating osv. """

                    monte_carlo.mcts() # KANSKJE GJØR OM NAVNET TIL DENNE, SIDEN DENNE DELEN ER LITT LIK NÅ

                    # print('HALLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLO')
                    if time.perf_counter() - timeout_start_time > self.timout_max_time:
                        print("Game", search_game, "timeouted.")
                        break

                # Used for training the ANET
                """ SJEKK OM DENNE ER BRA ELLER IKKE. DEN SER LITT SNODIG UT """
                distribution = monte_carlo.get_normalized_distribution()
                print('DIS til spillet - visited count',distribution)

                player = self.state_manager.get_playing_player()
                # Numpy array representing the state
                state = np.array(self.state_manager.get_state()) # Litt usikker på denne

                """ DANGER ZONE """
                '''Skal vell ikke ha med player her?? - hmm, Ser thommy har det'''
                case_for_buffer = (np.concatenate(([player], state.flatten()), axis=None), distribution) # MENER DENNE ER GANSKE SMUD, MEN KANSKJE ENDRE LITT
                replay_buffer.append(case_for_buffer)
                # print(case_for_buffer)

                act_ind = np.array(np.argmax(distribution))

                move_to_make = self.state_manager.get_all_moves()[act_ind]
                
                # print("MOVE", move_to_make)

                self.state_manager.do_move(move_to_make)

                monte_carlo.update_root(move_to_make)
                
                finished = self.state_manager.is_finished()
                
                print("State", state)
                print("Move", move_to_make)
                print("Finish", finished)

            winner = self.state_manager.get_winner()
            # print("Game finished! Player", winner, "won.")

            probs_for_rbuf = []
            """ LOWKEY DANGER ZONE """
            """ SE OVER DENNE HER """
            for i in range(len(replay_buffer)):
                probs_for_rbuf.append(i ** self.exploration_weight + 1e-10) # USIKKER HVOR INNHOLDET I APPENDEN KOMMER FRA

            # print("PROBS", probs_for_rbuf)
            probs_for_rbuf = probs_for_rbuf / np.sum(probs_for_rbuf)
            

            """ DANGER ZONE """
            """ SE OVER DENNE OG """
            if self.minibatch_size > 0:
                # print("FØRSTE IF")
                indices_for_minibatch = np.random.choice(len(replay_buffer), 
                                                        size=self.minibatch_size if self.minibatch_size <= len(replay_buffer) else len(replay_buffer), 
                                                        p=probs_for_rbuf, 
                                                        replace=False)

            else:
                # print("ANDRE IF")
                indices_for_minibatch = np.random.choice(len(replay_buffer), 
                                                        size = int(len(replay_buffer)) * self.minibatch_size,
                                                        p = probs_for_rbuf,
                                                        replace = False)
                
            # print("INDICES", indices_for_minibatch)

            """ DANGER ZONE """
            # print("REPLAY", replay_buffer)
            minibatch = np.array(replay_buffer)[indices_for_minibatch.astype(int)]
            
            # print("MINIB", minibatch)

            x_train, y_train = zip(*minibatch)
            
            # print("XTRAIN", x_train)
            # print("YTRAIN", y_train)
            
            # print(self.epochs)

            self.actor.fit_network(np.array(x_train), np.array(y_train), self.epochs)

            self.actor.update_epsilon()

            # Save the net according to the save interval
            # if (episode + 1) % self.save_interval == 0:
            #     self.actor.save_net(episode + 1)