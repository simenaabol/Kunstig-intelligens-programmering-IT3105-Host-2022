import sys
sys.path.append("..") 

from Environment.Hex import Hex
from Environment.Nim import Nim

from Parameters import hex_config, nim_config

class StateManager:

    def __init__(self, config):
        """Class for the state manager

        Args:
            config (dictionary): The main parameters

        Raises:
            Exception: Wrong game is chosen
        """        
        
        # Initialize the right game
        if config['game'] == 'hex':
            self.game = Hex(hex_config['board_size'])
            self.gameconfig = hex_config

        elif config['game'] == 'nim':

            self.game = Nim(nim_config['num_stones'], 
                            nim_config['max_removal'])
            self.gameconfig = nim_config
        else:
            raise Exception('Game must be hex or nim.')

        self.config = config
        

    def get_parameters(self):
        """Method for getting the parameters from the right game

        Returns:
            dictionary: Parameters for game chosen
        """        
        
        if isinstance(self.game, Hex):
            return hex_config

        elif isinstance(self.game, Nim):
            return nim_config
        

    def reset_game(self):
        """Method for reseting the game
        """        

        self.game.reset()
           

    def is_finished(self, state=None):
        """Method for checking if the game is finished

        Args:
            state (numpy array, optional): The state of the game. Defaults to None.

        Returns:
            bool: Game is done or not
        """        
        
        return self.game.game_done(state)


    def get_winner(self, state):
        """Retrieves the winner of a state

        Args:
            state (numpy array): A game state

        Returns:
            int: The player that won
        """        

        return self.game.player_has_won(state)


    def get_state(self):
        """Retrieves the state from the game object

        Returns:
            numpy array: ^^
        """        

        return self.game.get_current_state()


    def do_move(self, move):
        """Alters the state of the game with an action

        Args:
            move (tuple): An action
        """        

        self.game.alter_state_from_move(move)


    def get_legal_moves(self, state=None):
        """Retrieves all legal moves 

        Args:
            state (numpy array, optional): A game state. Defaults to None.

        Returns:
            array: Legal moves
        """        

        return self.game.get_moves(state)
    
    
    def get_all_moves(self):
        """Retrieves all possible moves in the game

        Returns:
            array: All moves
        """        

        return self.game.get_all_moves()


    def get_playing_player(self):
        """Retrieves the playing player from the game object

        Returns:
            int: Playing player
        """        
        
        return self.game.get_playing_player()


    def get_input_size(self):
        """Retrieves the input size for the neural net

        Returns:
            int: Input size
        """        

        return self.game.net_input_size()
    
    
    def get_output_size(self):
        """Retrieves the output size for the neural net

        Returns:
            int: Output size
        """        
        
        return self.game.net_output_size()
    
    
    def check_if_legal_action(self, state, action):
        """Checks if an action is legal in a state

        Args:
            state (numpy array): The state in which the action will be done
            action (tuple): The action to be checked

        Returns:
            bool: Legal move or not
        """        
        
        return self.game.is_legal_move(state, action)
    
    
    def get_kid_from_move(self, player, state, move):
        """Method for retrieving a kid from an action

        Args:
            player (int): The player
            state (numpy array): A game state
            move (tuple): The action

        Returns:
            numpy array and int: A new state representing after the move is done, and the opposite player
        """        
        
        return self.game.generate_kid_from_move(player, state, move)
    
    
    def get_kids(self, state, player):
        """Method for retrieving all kids from a state

        Args:
            state (numpy array): A game state
            player (int): The player

        Returns:
            array and int: An array of all kid-states, and the opposite player
        """        
        
        legal_moves = self.get_legal_moves(state)
        states_arr = []
        state = state.copy()
        
        for move in legal_moves:
            states_arr.append((self.get_kid_from_move(player, state, move)[0], move))
            
        if player == 1:
            player = 2
        else:
            player = 1
            
        return states_arr, player
   
   
    def get_reward(self, state, player):
        """Retrieves the reward from a state and player

        Args:
            state (numpy array): A game state
            player (int): A player

        Returns:
            int: The reward as an integer
        """        
        
        return self.game.get_reward(state, player)
    
    def vis_entire_game(self, array_of_states, number_of_vis):
        # print('array_of_states', array_of_states)
        self.game.get_graphic(array_of_states, number_of_vis)
