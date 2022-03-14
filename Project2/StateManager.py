from Environment.Hex import Hex
from Environment.Nim import Nim

from Parameters import hex_config, nim_config

class StateManager:

    def __init__(self, config):
        
        """ INSERT CONFIG PARAMS HERE """
        if config['game'] == 'hex':

            self.game = Hex(
                
            )

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

    def is_finished(self):

        return self.game.game_done()

    def get_winner(self):

        return self.game.player_has_won()

    def get_state(self):

        raise self.game.get_state_tuple()

    def do_move(self, move):

        self.game.alter_state_from_move(move)

    def get_legal_moves(self):

        return self.game.get_moves()

    def get_playing_player(self):
        
        return self.game.playing_player

    def get_input_size(self):

        return self.game.net_input_size()
