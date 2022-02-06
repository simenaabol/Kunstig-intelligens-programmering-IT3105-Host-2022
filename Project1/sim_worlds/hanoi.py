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
        return "HanoiState"

    def get_legal_moves(self):

        pegWithDisc = self.peg_with_disc()
        print('Peg som har discs', pegWithDisc)

        lMoves = self.get_legal_move_from_peg(pegWithDisc)
        print(lMoves)


        return lMoves

    def get_legal_move_from_peg(self, pegWithDisc): #pegNumber is the peg which disc is from
        move= []
        lPegs = self.get_lPegs()
        intPeg = int(pegWithDisc[0])

        for i in range(len(pegWithDisc)): # i blir hvilken peg vi henter fra
            print('hallo', lPegs[intPeg])
            hDisc = lPegs[intPeg][-1]
            print('Henter overste disk fra peg', hDisc)
            for j, peg in enumerate(lPegs): # J er hvilken peg vi er i
                if 0 == len(peg):
                    move.append([pegWithDisc, j])
                elif peg[-1] < hDisc:
                    move.append([pegWithDisc, j]) # legger til hvilken peg man kan flytt fra, og til
                else:
                    continue
                        
                
        
        return move

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

                    print(peg)
                    hDisc = peg[-1]

                else:
                    break
        return hDisc
            
                              


    def game_over(self):
        raise NotImplementedError()


    def get_nPegs(self):
        return self.nPegs

    def get_nDiscs(self):
        return self.nPegs

    def get_lPegs(self):
        return self.lPegs

    def get_aDiscs(self):
        return self.aDiscs





Game = Hanoi(5,4)#Pegs and discs
print(Game.get_lPegs())
print(Game.get_legal_moves())




