import sys
sys.path.append("..") 

from Environment.Hex import Hex
from Environment.Nim import Nim

from Parameters import hex_config, nim_config

class StateManager:

    def __init__(self, config):
        
        """ INSERT CONFIG PARAMS HERE """
        if config['game'] == 'hex':
            self.game = Hex(hex_config['board_size'])
            

        elif config['game'] == 'nim':

            self.game = Nim(nim_config['num_stones'], 
                            nim_config['max_removal'])

        else:
            raise Exception('Game must be hex or nim.')

        self.config = config

    def get_parameters(self):
        
        if isinstance(self.game, Hex):
            return hex_config

        elif isinstance(self.game, Nim):
            return nim_config

    def reset_game(self, playing_player):

        self.game.reset(playing_player)
        

    def is_finished(self, state=None):
        # print('State stateManager: ' ,  state)
        return self.game.game_done(state)

    def get_winner(self):

        return self.game.player_has_won()

    def get_state(self):

        return self.game.get_current_state()

    def do_move(self, move):

        self.game.alter_state_from_move(move)

    def get_legal_moves(self, state=None):

        return self.game.get_moves(state)
    
    def get_all_moves(self):

        return self.game.get_all_moves()

    def get_playing_player(self):
        
        # return self.game.playing_player
        return self.game.get_playing_player()

    def get_input_size(self):

        return self.game.net_input_size()
    
    def get_output_size(self):
        return self.game.net_output_size()
    
    def check_if_legal_action(self, state, action):
        
        return self.game.is_legal_move(state, action)
    
    def get_kid_from_move(self, player, state, move):
        return self.game.generate_kid_from_move(player, state, move)
    
    def get_kids(self, state, player):
        
        legal_moves = self.get_legal_moves(state)
        states_arr = []
        state = state.copy()
        
        # print("-----------")
        # print("GET KIDS KJØRER GET KID FROM MOVE I EN LØKKE MED DISSE VAR:", state, legal_moves)
        
        for move in legal_moves:
            states_arr.append((self.get_kid_from_move(player, state, move)[0], move))
        #     print("NOE GALT HER?", (self.get_kid_from_move(player, state, move)[0], move))
        # print("-----------")
            
        if player == 1:
            player = 2
        else:
            player = 1
            
        return states_arr, player
    
    def get_normalized_distribution(self):
       
       return self.game.get_normalized_distribution() 
   
    def get_reward(self, state, player):
        # print('11111111111111111111111111111111111111')
        return self.game.get_reward(state, player)

        # return self.game.get_reward(state)
        
