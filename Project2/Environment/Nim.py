from Parameters import nim_config
import numpy as np

class Nim:
    def __init__(self, num_stones, max_removal):
        

        # Variables from config
        self.num_stones = num_stones
        self.max_removal = max_removal
        
        # The current player
        self.playing_player = 1

        # The state in this game
        self.remaining_stones = np.array([num_stones])

    def get_moves(self, state=None):
        
        if state == None:
            state = self.remaining_stones
        
        legal_moves = []

        for i in range(1, self.max_removal + 1):
            if i <= state[0]:
                legal_moves.append(i)

        return legal_moves
    
    def get_all_moves(self):
        
        all_moves = []

        for i in range(1, self.max_removal + 1):
            all_moves.append(i)

        return all_moves

    def reset(self):
        self.num_stones = nim_config['num_stones']
        self.max_removal = nim_config['max_removal']
        
        if self.playing_player == 1:
            self.playing_player = 2
        else:
            self.playing_player = 1

        self.remaining_stones = np.array([self.num_stones])

    def game_done(self, state=None):
        
        if state == None:
            state = self.remaining_stones

        if state == 0:
            return True

        return False

    def player_has_won(self):   

        if self.game_done():
            if self.playing_player == 1:
                return 2
            else:
                return 1
        else:
            raise ValueError("No winner, game broken xD")


    def get_current_state(self):
        
        return self.remaining_stones


    def alter_state_from_move(self, move):

        if move not in self.get_moves():
            raise('Not a legal move')
        else:
            self.remaining_stones -= move

        if self.playing_player == 1:
            self.playing_player = 2
        else:
            self.playing_player = 1


    def net_input_size(self):   

        return len(self.remaining_stones) + 1
    
    def net_output_size(self):
        return len(self.get_all_moves())
    
    def is_legal_move(self, state, move):
        
        moves = self.get_moves(state)
        
        if move in moves:
            return True
        return False
    
    def generate_kid_from_move(self, player, state, move):
        
        if not self.is_legal_move(state, move):
            raise ValueError("IS ILLEGAL", state, move)
        
        
        new_kid = state.copy()
        new_kid -= move
        
        if player == 1:
            player = 2
        else:
            player = 1
            
        return new_kid, player
        
    def get_playing_player(self):
        return self.playing_player        
        
    
    def get_reward(self, player, _):
        if player == 1:
            return 2
        else:
            return 1