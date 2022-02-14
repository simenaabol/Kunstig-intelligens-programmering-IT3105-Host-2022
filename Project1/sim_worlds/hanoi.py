from tkinter import Y
from turtle import color
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np


class Hanoi():
    def __init__(self, pegs, discs) :   

        self.number_of_pegs = pegs
        self.number_of_discs = discs

        pegs_list = []   # List that rep. all the pegs with the discs. Higer int = bigger discs 
        for i in range(pegs): # create a list with nested lists
            pegs_list.append([])
            for n in range(discs):
                if i == 0:
                    pegs_list[i].append(discs-n) # Place the discs in the first peg
                #else:
                #   pegs_list[i].append(0) # fills nested lists with data
        self.pegs_list = pegs_list

    def get_state(self):
        return self.pegs_list

    def get_state_key(self):
        # print(tuple(map(tuple, self.pegs_list)))
        return tuple(map(tuple, self.pegs_list))

    def get_legal_moves(self):

        peg_with_disc = self.peg_with_disc()
        # print('peg_with_disc:',  peg_with_disc)

        moves_list = []
        for peg in peg_with_disc:
            temp_moves = self.get_legal_move_from_peg(peg)
            if len(temp_moves) != 0:
                moves_list += temp_moves
            # moves_list+=(self.get_legal_move_from_peg(peg))
        # print('LMOVES',moves_list)
        return moves_list

    def get_legal_move_from_peg(self, peg_with_disc): #peg_with_disc is the peg which disc is from
        move = []
        pegs_list = self.get_pegs_list()

        #for i in range(len(peg_with_disc)+1): # i blir hvilken peg vi henter fra
        highest_disc = pegs_list[peg_with_disc][-1]
        # print('highest_disc', highest_disc)
        for j, peg in enumerate(pegs_list): # J er hvilken peg vi er i
                
                if 0 == len(peg):
                    move.append([peg_with_disc, j])
                elif peg[-1] > highest_disc:
                    move.append([peg_with_disc, j]) # legger til hvilken peg man kan flytt fra, og til
                else:
                    continue
                        
        return move

    def reset_game(self):

        pegs = self.number_of_pegs
        discs = self.number_of_discs
        pegs_list = self.pegs_list

        pegs_list = []   # List that rep. all the pegs with the discs. Higer int = bigger discs 
        for i in range(pegs): # create a list with nested lists
            pegs_list.append([])
            for n in range(discs):
                if i == 0:
                    pegs_list[i].append(discs-n) # Place the discs in the first peg
                #else:
                #   pegs_list[i].append(0) # fills nested lists with data
        self.pegs_list = pegs_list

    def peg_with_disc(self):
        pegs_list = self.get_pegs_list()
        pegs = []

        for i, peg in enumerate(pegs_list):
            if 0 != len(peg):
                pegs.append(i)

        return pegs



    def find_highest_disc_in_peg(self):
        pegs_list = self.get_pegs_list()
        
        
 
        #Get the highest disc in thepeg [pegNumber]
        highest_disc = 0
        for peg in pegs_list:
            for disc in peg:
                if 0 != len(peg):

                    # print(peg)
                    highest_disc = peg[-1]

                else:
                    break
        return highest_disc
            
                              
    def take_action(self, move):
        pegs_list = self.get_pegs_list()
        from_peg = move[0]
        to_peg = move[1]
        pegs_list[to_peg].append(pegs_list[from_peg][-1]) # Adds the disc to the new peg
        pegs_list[from_peg].pop()


    def game_done(self):
        pegs_list = self.get_pegs_list()
        discs = self.get_number_of_discs()

        for peg in pegs_list:
            
            if pegs_list[0] == []:   
                if len(peg) == discs:
                    return [100, True]

        return [-0.1, False]


    def get_number_of_pegs(self):
        return self.number_of_pegs

    def get_number_of_discs(self):
        return self.number_of_discs

    def get_pegs_list(self):
        return self.pegs_list

    
    def get_graphic(self):
        pegs_list = self.get_pegs_list()
        dWith = self.get_number_of_discs()
        number_of_pegs = self.get_number_of_pegs()
        dWithG = dWith+3

        
        #define Matplotlib figure and axis
        fig, ax = plt.subplots()

        #add rectangle to plot
        for i, peg in enumerate(pegs_list):
            ax.plot([(dWith*0.5)-0.5+i*(dWithG), (dWith*0.5)-0.5+i*(dWithG)], [0, dWith-0.5])
            
            for j,disc in enumerate(peg):
                if len(peg) != 0:
                    ax.add_patch(Rectangle((j*0.5+i*dWithG, j), disc, 1,  
                    edgecolor ="blue", linewidth=1, facecolor  ='yellow'))
              

        #create simple line plot.
        ax.plot([0, (dWith+2)*number_of_pegs], [dWith, dWith], color = "white")

        return plt.show()


    def visualize(self, _, ep_step_count, least_steps_list):

        x_label = "Episodes"
        y_label = "Steps"

        return ep_step_count, x_label, y_label, min(least_steps_list)













Game = Hanoi(3,3)#Pegs and discs
''' print('Sate of the game', Game.get_pegs_list())
moves = Game.get_legal_moves()
print('Legal moves', moves)
Game.take_action([0,4])
print('Sate of the game', Game.get_pegs_list())
moves = Game.get_legal_moves()
print('Legal moves', moves)
print(Game.game_done()) '''


# print(Game.get_pegs_list())

# print(Game.get_legal_moves())
# Game.get_graphic()

# Game.take_action([0,1])
# Game.get_graphic()


Game.take_action([0,2])
Game.take_action([0,1])
#print(Game.get_legal_moves())

# Game.get_graphic()

# print(Game.get_legal_moves())
# print(Game.game_done())
# print(Game.get_state())



''' Game.get_graphic()
Game.take_action([0,1])
Game.get_graphic()
Game.take_action([0,2])
Game.get_graphic()
Game.take_action([0,4])
Game.get_graphic()
 '''





