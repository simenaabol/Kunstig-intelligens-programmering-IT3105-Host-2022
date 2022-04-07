import tensorflow as tf
from Actor import ANET
import os
from StateManager import StateManager
from NeuralNetwork import custom_cross_entropy
import numpy as np
import math
import matplotlib as plt

class Topp:
    def __init__(self, config, topp_config):
        """Class for the Topp

        Args:
            config (dictionary): The main parameters
            topp_config (dictionary): The topp parameters
        """        
        
        self.state_manager = StateManager(config)
        
        """ MULIG DU MÅ ENDRE DENNE SIMEN """
        path_list = [anet_path for anet_path in os.scandir("./TrainedNets/{folder}".format(folder=config['network_folder_name']))]
        
        self.anets = self.get_anets(path_list)
        self.number_of_anets = len(self.anets)
        self.number_of_games = topp_config['number_of_games']
        self.epsilon = topp_config['topp_eps']
        self.winner1 = 0
        self.winner2 = 0
        self.champions = None
        
        
    def get_anets(self, path_list):
        """Method for retrieving the nets from the right folder

        Args:
            path_list (string): Path for the network folder

        Returns:
            array: All the a-nets in the folder
        """        
        
        anets = []

        for i, path in enumerate(path_list):
            
            model = tf.keras.models.load_model(path, custom_objects={"custom_cross_entropy": custom_cross_entropy})
            anet = ANET(model, None, None, None, None, None, self.epsilon, 1, self.state_manager)
            anets.append((int(path.name), anet))
           
        anets.sort(key=lambda x: x[0])
        
        return anets
            
    
    def play_one_game(self, agent1, agent2):
        """Method for playing one game in the tournament

        Args:
            agent1 (object): The first actor
            agent2 (object): The second actor

        Returns:
            int: The winner of the game
        """        
        
        agents = (self.anets[agent1][1], self.anets[agent2][1])
        
        gamestate = self.state_manager.get_state()
        self.state_manager.reset_game()
        current_player = 0
        
        while not self.state_manager.is_finished(gamestate):
            
            action = agents[current_player].get_action(False, gamestate, current_player + 1, False)
            self.state_manager.do_move(action)
            gamestate = self.state_manager.get_state()
            
            if current_player == 0:
                current_player = 1
            else:
                current_player = 0
                
        winner = self.state_manager.get_winner(gamestate)
        
        if winner == 1:
                self.winner1 +=1
        elif winner == 2:
                self.winner2 +=1
        
        return winner
    
    
    def bestVSbest(self):
        """Method for choosing what players that play against each other
        """        
        for game in range(self.number_of_games):
            self.play_one_game(2, 2)
        print('spiller 1:', self.winner1)
        print('spiller 2:', self.winner2)
                       
              
        
    def play_round_robin(self):
        """The round robin tournament. Each player plays againt each other N times.
        """        
        
        champions = np.zeros((self.number_of_anets, self.number_of_anets), int)
        
        
        for agent1 in range(self.number_of_anets):
            
            for agent2 in range(self.number_of_anets):
                if agent1 == agent2:
                    continue

                for game in range(math.floor(self.number_of_games / 2)):
                    outcome = self.play_one_game(agent1, agent2)

                    if outcome == 1:
                        champions[agent1][agent2] += 1
                    elif outcome == 2:
                        champions[agent2][agent1] += 1

        self.champions = champions        
        print(self.champions)
        print('spiller 1:', self.winner1)
        print('spiller 2:', self.winner2)
    
    
    """ LAG DENNE """
    
    # def visualize(self):