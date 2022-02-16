import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

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
        pegs_list = self.get_pegs_list()
        highest_disc = pegs_list[peg_with_disc][-1]

        # j signifies which peg we are examining
        for j, peg in enumerate(pegs_list):

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

        pegs = self.number_of_pegs
        discs = self.number_of_discs
        pegs_list = self.pegs_list

        pegs_list = []

        for i in range(pegs):
            pegs_list.append([])

            for n in range(discs):

                if i == 0:
                    pegs_list[i].append(discs-n)

        self.pegs_list = pegs_list
        self.highest_peg = 0


    def get_pegs_with_discs(self):
        """

        Method for retrieving all pegs that contain disc(s).

        RETURNS: list of pegs that has disc(s)

        """

        pegs_list = self.get_pegs_list()
        pegs = []

        for i, peg in enumerate(pegs_list):
            if 0 != len(peg):
                pegs.append(i)

        return pegs


    def find_highest_disc_in_peg(self):
        """

        Method for finding the highest disc for a peg.

        RETURNS: the highest disc

        """

        pegs_list = self.get_pegs_list()
        highest_disc = 0

        for peg in pegs_list:

            if 0 != len(peg):
                highest_disc = peg[-1]

            else:
                break

        return highest_disc
            
                              
    def take_action(self, action):
        """  

        Method that does the action the Sim World gives to the Hanoi game.

        PARAMS: action

        """
        # if len(self.current_action) == 0:
        #     self.last_action = action
        # else:
        self.current_action = action
 
        

        pegs_list = self.get_pegs_list()
        from_peg = action[0]
        to_peg = action[1]

        # Adds the disc to the new peg
        pegs_list[to_peg].append(pegs_list[from_peg][-1])

        # Removes the disc to the old peg
        pegs_list[from_peg].pop()


    def Reverse(self, tuple):
        new_tuple= ()
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
            current_action_reversed = self.Reverse(self.current_action)
        else:
            current_action_reversed = self.Reverse(self.current_action[0])


       
        # Return negative reward for placin the dics back where it come from
        rew = 0
        if self.last_action == current_action_reversed:
            # print(self.last_action, ' == ',  current_action_reversed )
            rew = -1
        self.last_action = self.current_action




        # Return a positive reward for builig a peg with a new height
        pegs_list = self.get_pegs_list()
        discs = self.get_number_of_discs()

        
        for i, peg in enumerate(pegs_list):
            if i == 0:
                continue
            else:
                if len(peg) > self.highest_peg:
                    rew = 1
                    self.highest_peg = len(peg)

    
        # Check if done
        for peg in pegs_list:
            
            if pegs_list[0] == []:   
                if len(peg) == discs:
                    rew = 200
                    return [rew, True]

        return [-rew, False]


    """ DENNE SKAL VEL FJERNES? """
    def get_number_of_pegs(self):
        """

        Helping method to retrieve number of pegs.

        RETURNS: number of pegs

        """

        return self.number_of_pegs


    """ DENNE SKAL VEL FJERNES? """
    def get_number_of_discs(self):
        """

        Helping method to retrieve number of discs.

        RETURNS: number of discs

        """

        return self.number_of_discs


    """ DENNE SKAL VEL FJERNES? """
    def get_pegs_list(self):
        """

        Helping method to retrieve the list of pegs.

        RETURNS: list of pegs and discs

        """

        return self.pegs_list


    def get_state_key(self):
        """

        Method for getting the state for which the sim world will send to the learner.

        RETURNS: a tuple of the state (the list of pegs discs)

        """

        return tuple(map(tuple, self.pegs_list))


    def get_graphic(self, best_game):
        """

        Method for visualizing the best game of a run.

        PARAMS: best game (game with the lowest amount of moves)

        """

        best_game.append(best_game[-1])
        disc_width = self.get_number_of_discs()
        number_of_pegs = self.get_number_of_pegs()
        disc_width_margin = disc_width + 3

        # Define Matplotlib figure and axis
        _, ax = plt.subplots()

        # Add rectangle to plot
        for j, peg_list in enumerate(best_game):

            for i, peg in enumerate(peg_list):
                ax.plot([(disc_width * 0.5) - 0.5 + i * (disc_width_margin), (disc_width * 0.5) - 0.5 + i * (disc_width_margin)], [0, disc_width - 0.5])
                
                for j, disc in enumerate(peg):

                    if len(peg) != 0:
                        ax.add_patch(Rectangle((j * 0.5 + i * disc_width_margin, j), disc, 1,  
                        edgecolor = "blue", linewidth = 1, facecolor = 'yellow'))
                
                    # Create simple line plot.
                    ax.plot([0, (disc_width + 2) * number_of_pegs], [disc_width, disc_width], color = "white")

            # Frame delay from parameters file
            plt.pause(config['frame_delay'])
            ax.clear()
         

    def visualize(self, _, ep_step_count, least_steps_list):
        """

        Method for visualizing the learning graph.

        PARAMS: list of episodes and steps, list of just steps
        RETURNS: list of episodes and steps, x label, y label, lowest step in the run

        """

        x_label = "Episodes"
        y_label = "Steps"

        return ep_step_count, x_label, y_label, min(least_steps_list) + 1