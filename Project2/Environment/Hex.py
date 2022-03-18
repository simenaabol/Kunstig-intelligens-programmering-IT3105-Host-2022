# player 1 (red) or player 2 (black).
# Player 1 will always try to build a path that spans all rows, while player 2 will always try to span the columns¨

# On the diamond, this means that Player 1 seeks a path between the northeast and southwest sides, while player 2 wants a path
# between the northwest and southeast sides.
# -> Dette til si at vi må rotere matrisen 45 grader med klokken


import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import copy

from collections import deque



class Hex:
    def __init__(self, boardsize):
        self.boardsize = boardsize

        self.board = np.zeros((boardsize, boardsize))
        self.player = 1
        self.board_history = []
        self.neighbours = ((-1, 0), (-1, 1), (0, 1), (1, 0), (1, -1), (0, -1))

        self.node_size = 500
        self.colors = ['lightgrey', 'red', 'black']

        self.enough_pegs = False


    def reset(self, player):
        self.board = np.zeros((self.boardsize, self.boardsize))
        self.player = 1



    def get_moves(self):
        legal_moves = []
        for i in range(self.boardsize):
            for j in range(self.boardsize):
                if self.board[i, j] == 0.0:
                    legal_moves.append((i,j))
        return legal_moves
        # raise TypeError("Sorry, the player int is not compatible")


    def alter_state_from_move(self, action):


 


        self.board_history.append(copy.deepcopy(self.board))

        if self.board[action] != 0.0:
            raise TypeError("Sorry, this is a illegal action")
        else:
            self.board[action] = self.player
            
            if self.player == 1:
                self.player = 2
            else:
                self.player = 1

    
    def get_state(self):
        return self.board


    def game_done(self):
        pass


    def player_has_won(self):
        pass


    def game_done(self):
        # Check if player 1 has won
        player1 = self.check_winner(1)

        # If player one has not won, check player 2
        if player1[0] == False:
            return  self.check_winner(2)
        else:
            #Return the victory of player 1
            return player1


    def check_winner(self, player):


         # Checks if there are enough pegs on the board for a potential win
        if self.enough_pegs == False:
            if np.count_nonzero(self.board == self.player) < self.boardsize:
                print('Not enough pegs')
                return 'Ingen vinner'
            else:
                self.enough_pegs = True
                

        if self.enough_pegs == True:
            print('Enough pegs to winn, start DFS')

            edge = []
            visited = []     
            for i in range(len(self.board)):
                if player == 1: # 
                    # Find start state(s) for player 1
                    if self.board[0, i] == 1:
                        edge.append((0, i))
                elif player == 2:
                    # Find start state(s) for player 2
                    if self.board[i, 0] == 2:
                        edge.append((i, 0))
            
            while len(edge) > 0:
                node = edge.pop()
                visited.append(node)

                
                if player == 1 and node[0] == self.boardsize - 1:
                    return True, 1
                elif player == 2 and node[1] == self.boardsize -1:
                    return True, 2
                
                for i in range(len(self.neighbours)):
                    # x er 1, y er 0
                    if 0 <= node[0] + self.neighbours[i][0] < self.boardsize and 0 <= node[1] + self.neighbours[i][1] < self.boardsize \
                        and (node[0] + self.neighbours[i][0], node[1] + self.neighbours[i][1]) not in (visited + edge) \
                        and self.board[(node[0] + self.neighbours[i][0], node[1] + self.neighbours[i][1])] == player:
                            edge.append((node[0] + self.neighbours[i][0], node[1] + self.neighbours[i][1]))
            return False, 0


    def get_state_tuple(self):
        return tuple(self.board)

    
    def playing_player(self):
        return self.player
        

    def get_graphic(self):
        """
        Method for visualizing the game state.
        :param action: Action to be performed.
        :return: None
        """
        graph = nx.Graph()
        # graph.clear() # Remove all nodes and edged from the graph
        # plt.clf() # Clears the plt

        position = []
        node_color = []
        node_width = []
        
        for i in range(self.boardsize):
            height = self.boardsize - i
            width = np.ceil(self.boardsize / 2) - i
            for j in range(self.boardsize):
                graph.add_node(j) # Add up a list with all the nodes
                position.append((width, height)) # Add the position of the node
                node_width.append(self.node_size)
                node_color.append(self.colors[round(self.board[i, j])])  

                height -= 1
                width += 1
                
                # Add the edges to the graph
                # for dy, dx in self.neighbours:
                #     if 0 <= i + dy < board_size and 0 <= j + dx < board_size \
                #             and c != board_size * (i + dy) + (j + dx):
                #         graph.add_edge(c, board_size * (i + dy) + (j + dx))
                # c += 1

        # Add the edges to the graph
        c = 0
        for i in range(self.boardsize):
            for j in range(self.boardsize):
                for x in range(len(self.neighbours)):
                    if 0 <= i + self.neighbours[x][0] < self.boardsize and 0 <= j + self.neighbours[x][1] < self.boardsize \
                            and c != self.boardsize * (i + self.neighbours[x][0]) + (j + self.neighbours[x][1]):
                        graph.add_edge(c, self.boardsize * (i + self.neighbours[x][0]) + (j + self.neighbours[x][1]))
                c += 1


        nx.draw(graph, position, node_color=node_color, node_size=node_width, with_labels=False,
                font_weight='bold', ) # node_shape='^', mulig det eksisterer en smultring-form
        # graph.set_edgecolor('red') # Dette er ikke til kant, men som en border-color 
        plt.pause(0)
       

obj = Hex(4)
moves = obj.get_moves()

# Seier til 1 (red) 3*3
# '''
obj.alter_state_from_move((2,2))
obj.alter_state_from_move((2,0))
obj.alter_state_from_move((1,1))
obj.alter_state_from_move((0,2))
obj.alter_state_from_move((0,0))
obj.alter_state_from_move((1,2))
obj.alter_state_from_move((1,0))
obj.alter_state_from_move((0,1))
obj.alter_state_from_move((2,1))
# '''
obj.alter_state_from_move((0,3))
obj.alter_state_from_move((2,3))
obj.alter_state_from_move((3,0))
obj.alter_state_from_move((3,3))


# 
'''
obj.alter_state_from_move((2,1))
obj.alter_state_from_move((0,1))
obj.alter_state_from_move((1,1))
obj.alter_state_from_move((0,2))
obj.alter_state_from_move((0,0))
obj.alter_state_from_move((1,2))
'''




'''
# Fyll en hel 3*3
obj.alter_state_from_move((0,0))
obj.alter_state_from_move((1,0))
obj.alter_state_from_move((0,1))
obj.alter_state_from_move((1,1))
obj.alter_state_from_move((0,2))
obj.alter_state_from_move((1,2))

obj.alter_state_from_move((2,0))
obj.alter_state_from_move((2,1))
obj.alter_state_from_move((2,2))
'''

print(obj.board)
# print(obj.gameDone())
# print(obj.gameDone())
# obj.gameDone()
# obj.gameDone()
status = obj.game_done()
# status = obj.check_winner(1)
print('Status seier: ', status)




obj.get_graphic()

