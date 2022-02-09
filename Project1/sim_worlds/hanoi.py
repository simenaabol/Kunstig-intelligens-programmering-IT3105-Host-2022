from turtle import color
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np


class Hanoi():
    def __init__(self, pegs, discs) :   


        self.nPegs = pegs
        self.nDiscs = discs

        lPegs = []   # List that rep. all the pegs with the discs. Higer int = bigger discs 
        for i in range(pegs): # create a list with nested lists
            lPegs.append([])
            for n in range(discs):
                if i == 0:
                    lPegs[i].append(discs-n) # Place the discs in the first peg
                #else:
                #   lPegs[i].append(0) # fills nested lists with data
        self.lPegs = lPegs

    def get_state(self):
        return self.lPegs

    def get_state_key(self):
        # print(tuple(map(tuple, self.lPegs)))
        return tuple(map(tuple, self.lPegs))

    def get_legal_moves(self):

        pegWithDisc = self.peg_with_disc()
        # print('pegWithDisc:',  pegWithDisc)

        lMoves = []
        for peg in pegWithDisc:
            temp_moves = self.get_legal_move_from_peg(peg)
            if len(temp_moves) != 0:
                lMoves += temp_moves
            # lMoves+=(self.get_legal_move_from_peg(peg))
        # print('LMOVES',lMoves)
        return lMoves

    def get_legal_move_from_peg(self, pegWithDisc): #pegWithDisc is the peg which disc is from
        move = []
        lPegs = self.get_lPegs()


        #for i in range(len(pegWithDisc)+1): # i blir hvilken peg vi henter fra
        hDisc = lPegs[pegWithDisc][-1]
        # print('hDisc', hDisc)
        for j, peg in enumerate(lPegs): # J er hvilken peg vi er i
                
                if 0 == len(peg):
                    move.append([pegWithDisc, j])
                elif peg[-1] > hDisc:
                    move.append([pegWithDisc, j]) # legger til hvilken peg man kan flytt fra, og til
                else:
                    continue
                        
                
        
        return move

    def reset_game(self):

        pegs = self.nPegs
        discs = self.nDiscs
        lPegs = self.lPegs

        lPegs = []   # List that rep. all the pegs with the discs. Higer int = bigger discs 
        for i in range(pegs): # create a list with nested lists
            lPegs.append([])
            for n in range(discs):
                if i == 0:
                    lPegs[i].append(discs-n) # Place the discs in the first peg
                #else:
                #   lPegs[i].append(0) # fills nested lists with data
        self.lPegs = lPegs

    def peg_with_disc(self):
        lPegs = self.get_lPegs()
        pegs = []

        for i, peg in enumerate(lPegs):
            if 0 != len(peg):
                pegs.append(i)

        return pegs



    def find_highest_disc_in_peg(self):
        lPegs = self.get_lPegs()
        
        
 
        #Get the highest disc in thepeg [pegNumber]
        hDisc = 0
        for peg in lPegs:
            for disc in peg:
                if 0 != len(peg):

                    # print(peg)
                    hDisc = peg[-1]

                else:
                    break
        return hDisc
            
                              
    def take_action(self, move):
        # print(move)
        # print(self.lPegs)
        lPegs = self.get_lPegs()
        fromPeg = move[0]
        toPeg = move[1]
        # print(fromPeg, toPeg)
        lPegs[toPeg].append(lPegs[fromPeg][-1]) # Adds the disc to the new peg
        lPegs[fromPeg].pop()


    def game_done(self):
        lPegs = self.get_lPegs()
        discs = self.get_nDiscs()

        # print(self.lPegs)
        
        for i in range(len(lPegs)):
            if discs == len(lPegs[i]):   
                # if discs == lPegs[i][1]:   
                if len(lPegs[0]) != discs:
                    return [100, True]

        return [0, False]
            

    def get_nPegs(self):
        return self.nPegs

    def get_nDiscs(self):
        return self.nPegs

    def get_lPegs(self):
        return self.lPegs

    def get_aDiscs(self):
        return self.aDiscs
    
    def get_graphic(self):
        lPegs = self.get_lPegs()
        dWith = self.get_nDiscs()
        nPegs = self.get_nPegs()
        dWithG = dWith+3

        
        #define Matplotlib figure and axis
        fig, ax = plt.subplots()

        #add rectangle to plot
        for i, peg in enumerate(lPegs):
            ax.plot([(dWith*0.5)-0.5+i*(dWithG), (dWith*0.5)-0.5+i*(dWithG)], [0, dWith-0.5])
            
            for j,disc in enumerate(peg):
                if len(peg) != 0:
                    ax.add_patch(Rectangle((j*0.5+i*dWithG, j), disc, 1,  
                    edgecolor ="blue", linewidth=1, facecolor  ='yellow'))
              
                


        #create simple line plot.
        ax.plot([0, (dWith+2)*nPegs], [dWith, dWith], color = "white")

        return plt.show()






Game = Hanoi(3,3)#Pegs and discs
''' print('Sate of the game', Game.get_lPegs())
moves = Game.get_legal_moves()
print('Legal moves', moves)
Game.take_action([0,4])
print('Sate of the game', Game.get_lPegs())
moves = Game.get_legal_moves()
print('Legal moves', moves)
print(Game.game_done()) '''


# print(Game.get_lPegs())

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





