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
        """Class for the Hex game

        Args:
            boardsize (int): How large one side of the board should be
        """        
        
        self.boardsize = boardsize
        self.board = np.zeros((boardsize, boardsize), int)
        self.player = 1
        self.board_history = []
        self.neighbours = ((-1, 0), (-1, 1), (0, 1), (1, 0), (1, -1), (0, -1))

        self.node_size = 500
        self.colors = ['lightgrey', 'red', 'black']

        self.enough_pegs = False

    def reset(self):
        self.board = np.zeros((self.boardsize, self.boardsize))
        self.player = 1
    
    def get_moves_flatten(self, state):
        # Made for 7*7 board
        arr = state.pop(0)
        arr = np.array(state)
        arr = arr.reshape(7,7)
        return self.get_moves(arr)
                
        

    def get_moves(self, state=None):
        
        # if state.any() == None:
        #     state = self.board
        
        # print(state)
            
        legal_moves = []
        for i in range(self.boardsize):
            for j in range(self.boardsize):
                if state[i, j] == 0:
                    legal_moves.append((i,j))
        return legal_moves
        
    def get_all_moves(self):
        all_moves = []
        for i in range(self.boardsize):
            for j in range(self.boardsize):
                    all_moves.append((i,j))
        return all_moves

    def alter_state_from_move(self, action):

        self.board_history.append(copy.deepcopy(self.board))

        if self.board[action] != 0:
            raise TypeError("Sorry, this is a illegal action")
        else:
            self.board[action] = self.player
            
            if self.player == 1:
                self.player = 2
            else:
                self.player = 1

    def get_current_state(self):
        return self.board
    
    def generate_kid_from_move(self, player, state, move):
        
        if not self.is_legal_move(state, move):
            raise ValueError("IS ILLEGAL", state, move)
        
        new_kid = state.copy()
        new_kid[move] = player
        
        if player == 1:
            player = 2
        else:
            player = 1
            
        return new_kid, player

    def is_legal_move(self, state, move):
        
        moves = self.get_moves(state)
        
        if move in moves:
            return True
        return False

    def player_has_won(self, state):
        
        player1 = self.check_winner(1, state)
        if player1[0]:
            return 1
        else:
            return 2

    def get_reward(self, state, player):
        
        if player == 1:
            if self.check_winner(player, state)[0]  == True:
                return 1
            else:
                return 0
        
        if player == 2:
            if self.check_winner(player, state)[0]  == True:
                return -1
            else:
                return 0

    def game_done(self, state=None):
        
        try:
            if state == None:
                state = self.board
                return self.game_done(state)
        except:   
            
            new_state = []
            for arrayCount, element in enumerate(state):
                new_state.append([])
                for number in element:
                    new_state[arrayCount].append(int(number))
            
            state = np.array(new_state)
            
            # Check if player 1 has won
            player1 = self.check_winner(1, state)
            player2 = self.check_winner(2, state)
            
            # Game done
            if player1[0] or player2[0]:
                return  True
            else:
                # Game not done
                return False
   
    def check_winner(self, player, state):

         # Checks if there are enough pegs on the board for a potential win
        if self.enough_pegs == False:
            if np.count_nonzero(state == self.player) < self.boardsize:
                return False, 0
            else:
                self.enough_pegs = True
                

        if self.enough_pegs == True:
            # print('Enough pegs to winn, start DFS')

            edge = []
            visited = []
            
            for i in range(len(state)):
                if player == 1:
                    
                    # Find start state(s) for player 1
                    if round(state[0, i], 0) == 1:
                        edge.append((0, round(i)))
                        
                elif player == 2:
                    # Find start state(s) for player 2
                    if round(state[i, 0]) == 2:
                        edge.append((round(i), 0))
  
            while len(edge) > 0:
                node = edge.pop()
                
                visited.append(node)
              
                if player == 1 and node[0] == self.boardsize - 1:
                    return [True, 1]
                elif player == 2 and node[1] == self.boardsize -1:
                    return [True, 2]
                
                for i in range(len(self.neighbours)):
                    if 0 <= node[0] + self.neighbours[i][0] < self.boardsize and 0 <= node[1] + self.neighbours[i][1] < self.boardsize \
                        and (node[0] + self.neighbours[i][0], node[1] + self.neighbours[i][1]) not in (visited + edge) \
                        and state[(node[0] + self.neighbours[i][0], node[1] + self.neighbours[i][1])] == player:
                            edge.append((node[0] + self.neighbours[i][0], node[1] + self.neighbours[i][1]))
            return [False, 0]

    def get_state_tuple(self):
        return tuple(self.board)

    def net_input_size(self):
        return self.boardsize*self.boardsize+1
    
    def net_output_size(self):  
        return self.boardsize*self.boardsize
    
    def get_playing_player(self):
        return self.player
        

    def get_graphic(self, array_of_states,number_of_vis ):
        """
        Method for visualizing the game state.
        :param action: Action to be performed.
        :return: None
        """
        graph = nx.Graph()
        graph.clear() # Remove all nodes and edged from the graph
        plt.clf() # Clears the plt
        
        print('array_of_states in hex', array_of_states)

        for one_board in array_of_states:
            position = []
            node_color = []
            node_width = []
            
            # self.board = np.array(copy.deepcopy(one_board))
            # print('oneBB', one_board)
            
            for i in range(self.boardsize):
                height = self.boardsize - i*0.5
                width = np.ceil(self.boardsize / 2) -i
                for j in range(self.boardsize):
                    graph.add_node(j) # Add up a list with all the nodes
                    position.append((width, height)) # Add the position of the node
                    node_width.append(self.node_size)
                    node_color.append(self.colors[round(one_board[i, j])])  

                    height -= 0.5
                    width += 1
                    
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
            plt.pause(0.7)
        
  
        plt.close()

    def board_flip(self, state):
        #  State is the board with player first

        #  remove the first int, the player
        # print('State1', state)

        temp_state = []

        for int in state:
            if int == 1:
                temp_state.append(2)
            elif int == 0:
                temp_state.append(0)
            else:
                temp_state.append(1)
        return temp_state
        

