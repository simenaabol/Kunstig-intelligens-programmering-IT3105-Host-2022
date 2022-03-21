import sys
sys.path.append("..") 
 
from MCTS.Node import Node
import numpy as np

import random


class MCTS:
    def __init__(self, exploration_weight, actor, state_manager):
        """

        Class for Monte Carlo Search Tree

        PARAMS: exploration_weight, actor, state_manager

        RETURN: nothing

        """
        self.root = Node(
            state = state_manager.get_state(),
            parent = None,
            player = state_manager.get_playing_player()
            )

        self.exp_weight = exploration_weight
        self.actor = actor # obj
        self.state_manager = state_manager # obj

# Main-kok
    def get_normalized_distribution(self):
        """

        Method fetching the distribution

        PARAMS: nothing

        RETURNS: the normalized distribution 

        """

        
        """
        Gets the distribution of visit counts of the children of the root
        :return: The normalized distribution
        """
        # Mix med niclas
        board_shape = self.state_manager.get_state().shape
        distribution = np.zeros(board_shape)
        for action in self.root.kid: #Itererer alle barna til roten? Ikke alle?
                distribution.append(float(self.root.kid[action].count) / float(self.root.count))
        return distribution.flatten()

        # Dette er fra main. Kan evt testes
        # board_shape = self.simworld.get_grid().shape
        # distribution = np.zeros(board_shape)
        # for action in self.root.kid: #Itererer alle barna til roten? Ikke alle?
        #     kid = self.root.kid[action]
        #     distribution[action] = kid.count
        # distribution = distribution.flatten()
        # return distribution / np.sum(distribution)    

        

    def mcts(self):
        """

        Method for running the mcts algorithm.

        PARAMS: nothing 

        RETURNS: nothing

        """

        if self.state_manager.is_finished(self.root.get_state()): #Sjekk opp metodNavn til done
            return # Kunne returnert noe her for å skille seg fra kok. 
        
        # Bør legge inn en raise her hvis det ikke eksisterer en node


    # 1. Tree Search - Traversing the tree from the root to a leaf node by using the tree policy
        leaf = self.search() # returns current_node
        
        # print("LEAF", leaf)

        # Check if the leaf is at the end
        if self.state_manager.is_finished(leaf.get_state()):
            rew = self.state_manager.get_reward(leaf.get_state())
            self.backpropagation(leaf, rew)
            return

        
    # 2. Node Expansion - Generating some or all child states of a parent state, 
    # and then connecting the tree node housing the parent state (a.k.a. parent node) 
    # to the nodes housing the child states (a.k.a. child nodes).

        # Find ALL the leaf for the input node
        kids = self.new_leaves(leaf)


    # 3. Leaf Evaluation - Estimating the value of a leaf node in the tree by doing
    # a rollout simulation using the default policy from the leaf node’s state to a final state

        # Chooses one of the new kids found in new_leaves
        kid = np.random.choice(kids)

        # Leaf evaluation // a rollout
        leaf, rew = self.leaf_evaluation(kid)
        
        print("ETTER ROLLOUT")



    # 4. Backpropagation - Passing the evaluation of a final state back up the tree, 
    # updating relevant data (see course lecture notes) at all nodes and edges 
    # on the path from the final state to the tree root.

        # Kommenatren under er kok
        # If only nodes in MCT should be updated change leaf to successor
        self.backpropagation(kid, rew)
   

    def update_root(self, action):
        """

        Method for updating the root

        PARAMS: action

        RETURNS: nothing

        """
        _temp_root = self.root.get_kid(action)
        if not _temp_root: # kok - usikker hva som skjer her
            self.root = Node(
                state = self.state_manager.get_state(),
                parent = None, 
                player = self.state_manager.get_playing_player()
            )
        self.root = _temp_root

    def search(self):
        """

        Method for traversing the tree from the root to a leaf node by using the actor.

        PARAMS: nothing

        RETURNS: a leaf node

        """


        current_node = self.root

        #  Er vell bare å bruke player her?
        player = current_node.get_player()   
        flag = 0   
        if player == 1:
            flag = 1
        elif player == 2:
            flag = -1
        else:
            raise TypeError("Sorry, the player int is not compatible")

        max = -flag * float('inf')
        current_best = None
        kids = current_node.get_kids()

        for action in kids:
            # hvorfor a?
            a = current_node.get_q_value(action) + flag * current_node.get_u_value(action, self.exp_weight)
            
            if (a < max and flag == -1) or (a > max and flag == 1):
                max = a
                current_best = action

            flag *= -1
            current_node = current_node.get_kid_with_action(current_best)
            
        return current_node


    
    def new_leaves(self, leaf): # Node expansion
        """

        Method - Generating all(atm) child states of a parent state, 
              and then connecting the tree node housing the parent state (a.k.a. parent node) 
              to the nodes housing the kid states (a.k.a. kid nodes)

        PARAMS: leaf-node

        RETURNS: a set of new kids from the input parent 'leaf'

        """
        # merk at denne finne alle nye leaves. 

        state = leaf.get_state()
        player = leaf.get_player()

        state_action_list, player = self.state_manager.get_kids(state, player)
        kids = []

        for state, action in state_action_list:
            kid = leaf.get_kid_with_action(action, rollout = True)
            leaf.remove_kid(action, rollout = True)

            if not kid: # Sjekk om man kan bruke noe annet her
                kid = Node(state, leaf, player)
            leaf.add_kid(kid, action)
            kids.append(kid)
        return kids


    def leaf_evaluation(self, from_node):  # rollout
        """

        Method for traversing the tree from the root to a leaf node by using the actor.

        PARAMS: from_node

        RETURNS: a leaf node

        """
        
        leaf = from_node.get_state()
        player = from_node.get_player()
        done = self.state_manager.is_finished(leaf) #Sjekk opp metodNavn
        parent = from_node 

        while done == False:
            # Tomy
            action = self.actor.get_action()
            
            
            # action = self.pick_move_ann(self.state_manager.get_state(), legal_actions, all_actions)
            """ TROR NOE RART MED LINJA UNDER? """
            leaf, player = self.state_manager.get_kid_from_move(player, leaf, action)
            next_leaf = parent.get_kid_with_action(action, rollout = True)

            if not next_leaf:
                next_leaf = Node(leaf, parent, player)
                parent.add_kid(next_leaf, action, rollout = True)
            parent = next_leaf
            done = self.state_manager.is_finished(leaf) #Sjekk opp metodNavn
        
        final_leaf = parent.get_state()  # Kan smelle disse sammen
        rew = self.state_manager.get_reward(final_leaf) # Kan smelle disse sammen
        # Disse to over bør egt ikke lagres som egne variabler, da de ikke brukes    
        return parent, rew

    # def pick_move_ann(state,legal_actions,all_actions  ):


    def backpropagation(self, leaf, rew):
        """

        Method - Passing the evaluation of a final state back up the tree,
              updating relevant data at all nodes and edges on the path from 
              the final state to the tree root.

        PARAMS: leaf-node , reward


        RETURNS: a set of new kids from the input parent 'leaf'

        """
    
        current_node = leaf

        while self.root != current_node:
            current_node.update_evaluate(rew)
            current_node.update_count()

            # Update current_node to it's parent for the next iteration
            current_node = current_node.get_parent()
        
        self.root.update_evaluate(rew)
        self.root.update_count()
















       




      
        

            


                
            

