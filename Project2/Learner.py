from StateManager import StateManager

import matplotlib.pyplot as plt

class RL_learner():

    def __init__(self, config):

        self.state_manager = StateManager(config)

        self.num_actual_games = config['num_actual_games']
        self.num_search_games = config['num_search_games']




        # 1. Save interval for ANET parameters
        # 2. Clear RBUF
        # 3. Randomly initialize parameters (weights and biases) of ANET




    def training(self):
        
        for episode in range(self.num_actual_games):

            for search in range(self.num_search_games):
                pass
