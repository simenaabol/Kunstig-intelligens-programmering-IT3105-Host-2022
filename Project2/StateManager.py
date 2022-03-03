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

            self.game = Nim(

            )

        else:
            raise Exception('Game must be hex or nim.')

        self.config = config

    def get_parameters(self):
        
        if isinstance(self.game, Hex):
            return hex_config

        elif isinstance(self.game, Nim):
            return nim_config

    def reset_game(self):
        raise NotImplementedError

    def is_finished(self):
        raise NotImplementedError

    def get_state(self):
        raise NotImplementedError

    def do_move(self, move):
        raise NotImplementedError
