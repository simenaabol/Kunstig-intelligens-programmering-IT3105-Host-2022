from StateManager import StateManager
from Actor import ANET
from ReplayBuffer import RBUF

class RL_learner():

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

        self.RBUF = RBUF() # INVESTIGATE WHAT THIS SHIT DOES

        self.num_actual_games = config['num_actual_games']
        self.num_search_games = config['num_search_games']

        self.minibatch_size = None # IDK tror denne brukes til trening elns
        self.save_interval = self.num_actual_games / 4 # Hvor ofte man lagrer nettverket

        self.starting_player = 1 # Evt gjør om dette til et parameter


    def training(self):

        # Save the initial net
        self.actor.save_net()
        
        for episode in range(self.num_actual_games):

            print('Episode nr.', episode + 1)

            self.state_manager.reset_game()

            """ GJØR OM DENNE NÅR MCTS ER FERDIG """
            mct_root = None

            finished = self.state_manager.is_finished()

            while not finished:




                for search_game in range(self.num_search_games):
                    pass


    def change_starting_player():
        raise NotImplementedError
