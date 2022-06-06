import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import copy
from parameters import config

class Hanoi():
    def __init__(self, pegs, discs):
        """  

        Class representing the Towers of Hanoi problem.

        PARAMS: number of pegs, number of discs

        """

        self.number_of_pegs = pegs
        self.number_of_discs = discs

        # List that represents all the pegs with the discs. Higher int = bigger discs
        # For example, if there are 5 discs in the game, then disc with int: 5 is the biggest.
        pegs_list = []

        # Create a list with nested lists to represent the game
        for i in range(pegs):
            pegs_list.append([])
            for n in range(discs):
                # Place the discs in the first peg
                if i == 0:
                    pegs_list[i].append(discs-n)

        self.pegs_list = pegs_list

        self.last_action = [(0,0)]
        self.current_action = [(0,0)]    
        
        self.highest_peg = 0

        self.first_game = []
        self.this_game = []
        self.best_game = []

        self.reset = 0
    

    def get_legal_moves(self):
        """  

        Method for retrieving all the legal moves for a state.

        RETURNS: list of all legal moves

        """

        peg_with_disc = self.get_pegs_with_discs()
        moves_list = []

        for peg in peg_with_disc:
            temp_moves = self.get_legal_move_from_peg(peg)

            if len(temp_moves) != 0:
                moves_list += temp_moves

        return moves_list


    def get_legal_move_from_peg(self, peg_with_disc):
        """

        Helping method for retrieving all legal moves.

        PARAMS: peg_with_disc, meaning the peg where the disc is from

        """

        move = []
        highest_disc = self.pegs_list[peg_with_disc][-1]

        # j signifies which peg we are examining
        for j, peg in enumerate(self.pegs_list):

            # Appending the peg a move can be taken from and to
            if 0 == len(peg):
                move.append([peg_with_disc, j])

            elif peg[-1] > highest_disc:
                move.append([peg_with_disc, j])

            else:
                continue
                        
        return move


    def reset_game(self):
        """

        Method for reseting the game to its initial state. Much like the init-method.

        """

        init_pegs_list = []

        for i in range(self.number_of_pegs):
            init_pegs_list.append([])

            for n in range(self.number_of_discs):

                if i == 0:
                    init_pegs_list[i].append(self.number_of_discs-n)

        self.pegs_list = init_pegs_list
        self.highest_peg = 0

        self.this_game = []
        self.reset += 1

                             
    def take_action(self, action):
        """  

        Method that does the action the Sim World gives to the Hanoi game.

        PARAMS: action

        """

        self.current_action = action

        self.this_game.append(copy.deepcopy(self.pegs_list))

        if self.reset == 1:
            self.first_game.append(copy.deepcopy(self.pegs_list))

        from_peg = action[0]
        to_peg = action[1]

        self.pegs_list[to_peg].append(self.pegs_list[from_peg][-1])

        self.pegs_list[from_peg].pop()
        

    def get_pegs_with_discs(self):
        """

        Method for retrieving all pegs that contain disc(s).

        RETURNS: list of pegs that has disc(s)

        """

        pegs = []

        for i, peg in enumerate(self.pegs_list):
            if 0 != len(peg):
                pegs.append(i)

        return pegs


    def find_highest_disc_in_peg(self):
        """

        Method for finding the highest disc for a peg.

        RETURNS: the highest disc

        """

        highest_disc = 0

        for peg in self.pegs_list:

            if 0 != len(peg):
                highest_disc = peg[-1]

            else:
                break

        return highest_disc
            
 
        
    def reverse(self, tuple):
        """

        Method that reverse a tuple 

        PARAMS: tuple
        RETURNS: tuple

        """
        
        new_tuple = ()

        for i in reversed(tuple):
            new_tuple = new_tuple + (i,)

        return new_tuple


    def game_done(self):
        """

        Method that returns if the game is done or not, in addition to the reward
        for the action.

        RETURNS: list of reward and bool

        """

        # Reverse the action
        is_tuple = type(self.current_action) is tuple

        if is_tuple:
            current_action_reversed = self.reverse(self.current_action)
        else:
            current_action_reversed = self.reverse(self.current_action[0])

        # Default reward for a move
        rew = -1

        # Return negative reward for placing the dics back where it come from
        if self.last_action == current_action_reversed:
            rew = -2

        self.last_action = self.current_action

        # Return a positive reward for builig a peg with a new height  
        for i, peg in enumerate(self.pegs_list):
            if i == 0:
                continue

            else:
                if len(peg) > self.highest_peg:
                    rew = 1
                    self.highest_peg = len(peg)
 
        # Check if done
        for peg in self.pegs_list:
            if self.pegs_list[0] == []:                
                if len(peg) == self.number_of_discs:

                    rew = 100
                    self.reset +=1

                    if self.this_game != []:
                        self.best_game = (self.this_game)
                        
                        self.best_game.append(self.pegs_list)

                    # Reset this_game
                    self.this_game = []    

                    return [rew, True]

        return [rew, False]


    def get_state_key(self):
        """

        Method for getting the state for which the sim world will send to the learner.

        RETURNS: a tuple of the state (the list of pegs discs)

        """

        return tuple(map(tuple, self.pegs_list))


    def get_graphic(self):
        """

        Method for visualizing the first and the best game of a run.


        """

        disc_width = self.number_of_discs
        disc_width_margin = disc_width + 3

        # Define Matplotlib figure and axis
        _, ax = plt.subplots()
        
        for j, peg_list in enumerate(self.best_game):
            plt.title("Best game")
            for i, peg in enumerate(peg_list):
                ax.plot([(disc_width * 0.5) - 0.5 + i * (disc_width_margin), (disc_width * 0.5) - 0.5 + i * (disc_width_margin)], [0, disc_width - 0.5]) 
                for j, disc in enumerate(peg):
                    if len(peg) != 0:
                        ax.add_patch(Rectangle((j * 0.5 + i * disc_width_margin, j), disc, 1,  
                        edgecolor = "blue", linewidth = 1, facecolor = 'yellow'))
                
                    # Create simple line plot.
                    ax.plot([0, (disc_width + 2) * self.number_of_pegs], [disc_width, disc_width], color = "white")

            # Frame delay from parameters file
            plt.pause(config['frame_delay'])
            ax.clear()
        plt.close()

        # Define Matplotlib figure and axis
        _, ax = plt.subplots()

        for j, peg_list in enumerate(self.first_game):
            plt.title("First game")
            for i, peg in enumerate(peg_list):
                ax.plot([(disc_width * 0.5) - 0.5 + i * (disc_width_margin), (disc_width * 0.5) - 0.5 + i * (disc_width_margin)], [0, disc_width - 0.5])
                for j, disc in enumerate(peg):
                    if len(peg) != 0:
                        ax.add_patch(Rectangle((j * 0.5 + i * disc_width_margin, j), disc, 1,  
                        edgecolor = "blue", linewidth = 1, facecolor = 'yellow'))
                
                    # Create simple line plot.
                    ax.plot([0, (disc_width + 2) * self.number_of_pegs], [disc_width, disc_width], color = "white")

            # Frame delay from parameters file
            plt.pause(config['frame_delay'])
            ax.clear()  
        plt.close()
            


    def visualize(self, _, ep_step_count, least_steps_list):
        """

        Method for visualizing the learning graph.

        PARAMS: list of episodes and steps, list of just steps
        RETURNS: list of episodes and steps, x label, y label, lowest step in the run

        """

        x_label = "Episodes"
        y_label = "Steps"

        title = "Hanoi learning graph"

        return ep_step_count, x_label, y_label, min(least_steps_list) + 1, title