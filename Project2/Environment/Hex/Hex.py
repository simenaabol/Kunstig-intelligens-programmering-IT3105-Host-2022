# player 1 (red) or player 2 (black).
# Player 1 will always try to build a path that spans all rows, while player 2 will always try to span the columns¨

# On the diamond, this means that Player 1 seeks a path between the northeast and southwest sides, while player 2 wants a path
# between the northwest and southeast sides.
# -> Dette til si at vi må rotere matrisen 45 grader med klokken

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import copy


class Hex:
    def __init__(self, boardsize):
        self.boardsize = boardsize

        self.board = np.zeros((boardsize, boardsize))
        self.player = 1
        self.board_history = []
    
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


    def get_state_tuple(self):
        return tuple(self.board)

    
    def playing_player(self):
        return self.player
        
    def get_graphic(self):
        g = nx.Graph()
        

        g.add_node(1)
        g.add_node(2)

        g.add_edge(1,2)

        nx.draw(g)
        plt.pause(100)     


    def visualize_state(self, action=None):
        """
        Method for visualizing the game state.
        :param action: Action to be performed.
        :return: None
        """
        graph = nx.Graph()
        state = self.board
        board_size = self.boardsize
        # graph.clear() # Remove all nodes and edged from the graph
        # plt.clf() # Clears the plt



        position = []
        total_height = 1 + 2 * board_size
        total_width = total_height
        colors=['lightgrey', 'red', 'black']
        color_map = []
        node_with = []

        # Add nodes to graph (+position, color and size)
        c = 0
        for i in range(board_size):
            h = total_height - i
            w = np.ceil(total_width / 2) - i
            for j in range(board_size):
                graph.add_node(j) # Add up a list with all the nodes
                position.append((w, h)) # Add the position of the node
                node_with.append(500)
                color_map.append(colors[round(self.board[i, j])])

                h -= 1
                w += 1
                c += 1

        # Add edges to graph
        neighbours = {(-1, 0), (-1, 1), (0, 1), (1, 0), (1, -1), (0, -1)}
        c = 0
        for i in range(board_size):
            for j in range(board_size):
                for dy, dx in neighbours:
                    if 0 <= i + dy < board_size and 0 <= j + dx < board_size \
                            and c != board_size * (i + dy) + (j + dx):
                        graph.add_edge(c, board_size * (i + dy) + (j + dx))
                c += 1
        print(position)
        # graph.set_edgecolor('red') 

        nx.draw(graph, position, node_color=color_map, node_size=node_with, with_labels=False,
                font_weight='bold', ) # node_shape='^'
        plt.pause(0)
        # plt.draw() #With this it only plots states 2 times, compared to 3 without


    
    


obj = Hex(3)
moves = obj.get_moves()
obj.alter_state_from_move((2,2))
# obj.visualize_state()
obj.alter_state_from_move((2,1))
# obj.visualize_state()
obj.alter_state_from_move((1,1))
obj.alter_state_from_move((0,2))
obj.alter_state_from_move((0,0))
# Seier til 1 (red) -> enere langs radene
print(obj.board)
# obj.get_graphic()
obj.visualize_state()