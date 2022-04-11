import sys
sys.path.append("..") 
 
from MCTS.Node import Node
import numpy as np


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
        self.actor = actor
        self.state_manager = state_manager
  
    def get_normalized_distribution(self):
        """

        Method fetching the distribution

        PARAMS: nothing

        RETURNS: the normalized distribution 

        """

        distribution = []
        
        for action in self.state_manager.get_all_moves():
            
            if action in self.root.kids:
                kid = self.root.get_kid_with_action(action)
                distribution.append(float(kid.count) / float(self.root.count))
            else:
                distribution.append(0.0)
                
        return distribution / np.sum(distribution)

    def mcts(self, lite_model):
        """

        Method for running the mcts algorithm.

        PARAMS: nothing 

        RETURNS: nothing

        """

        if self.state_manager.is_finished(self.root.get_state()):
            return

        # 1. Tree Search - Traversing the tree from the root to a leaf node by using the tree policy
    
        leaf = self.search()

        # Check if the leaf is at the end
        if self.state_manager.is_finished(leaf.get_state()):
            rew = self.state_manager.get_reward(leaf.get_state(),leaf.get_player() )
            self.backpropagation(leaf, rew)
            return
        
        # 2. Node Expansion - Generating some or all child states of a parent state, 
        # and then connecting the tree node housing the parent state (a.k.a. parent node) 
        # to the nodes housing the child states (a.k.a. child nodes).
        
        kids = self.new_leaves(leaf)

        # 3. Leaf Evaluation - Estimating the value of a leaf node in the tree by doing
        # a rollout simulation using the default policy from the leaf node’s state to a final state

        # Chooses one of the new kids found in new_leaves
        kid = np.random.choice(kids)
        
        leaf, rew = self.leaf_evaluation(kid, lite_model)

        # 4. Backpropagation - Passing the evaluation of a final state back up the tree, 
        # updating relevant data (see course lecture notes) at all nodes and edges 
        # on the path from the final state to the tree root.
    
        self.backpropagation(kid, rew)
   

    def update_root(self, action):
        """

        Method for updating the root

        PARAMS: action

        RETURNS: nothing

        """
        
        _temp_root = self.root.get_kid_with_action(action)
        
        if not _temp_root:
            self.root = Node(
                state = self.state_manager.get_state(),
                parent = None, 
                player = self.state_manager.get_playing_player()
            )
            
        self.root = _temp_root
        self.root.parent = None

    def search(self):
        """

        Method for traversing the tree from the root to a leaf node by using the actor.

        PARAMS: nothing

        RETURNS: a leaf node

        """
        """
        current_node = self.root
        
        while current_node.get_kids_count() > 0:
            
            player = current_node.player
            policy_function = max if player == 1 else min
            
            action = policy_function(current_node.kids.keys(), key=lambda key: current_node.kids[key].UCT(player, self.exp_weight))

            current_node = current_node.kids[action]

        return current_node
        """
        
        current_node = self.root
        player = current_node.get_player()
        flag = 0   
        
        if player == 1:
            flag = 1
        elif player == 2:
            flag = -1
        else:
            raise TypeError("Sorry, the player int is not compatible[2]")

        while current_node.get_kids_count() > 0:
    
            max = -flag * float('inf')
            current_best = None
            kids = current_node.get_kids()

            for action in kids:
                
                if  current_node.get_action_count(action) == 0:
                    a = -max
                else:
                    if flag == 1:
                        a = current_node.get_q_value(action) + current_node.get_u_value(action, self.exp_weight)
                    else:
                       a = current_node.get_q_value(action) - current_node.get_u_value(action, self.exp_weight)
                
                if (a < max and flag == -1) or (a > max and flag == 1):
                    max = a
                    current_best = action

            current_node = current_node.get_kid_with_action(current_best)
            flag *= -1
            
        return current_node
    
    def new_leaves(self, leaf):
        """
        Method - Generating all(atm) child states of a parent state, 
              and then connecting the tree node housing the parent state (a.k.a. parent node) 
              to the nodes housing the kid states (a.k.a. kid nodes)

        PARAMS: leaf-node

        RETURNS: a set of new kids from the input parent 'leaf'

        """

        state = leaf.get_state()
        player = leaf.get_player()

        state_action_list, player = self.state_manager.get_kids(state, player)
        kids = []

        for state, action in state_action_list:
            kid = leaf.get_kid_with_action(action, rollout = True)
            leaf.remove_kid(action, rollout = True)

            if not kid:
                kid = Node(state, leaf, player)
                
            leaf.add_kid(kid, action)
            kids.append(kid)
            
        return kids


    def leaf_evaluation(self, from_node, lite_model):
        """
        Method for traversing the tree from the root to a leaf node by using the actor.

        PARAMS: from_node

        RETURNS: a leaf node

        """
        
        leaf = from_node.get_state()
        player = from_node.get_player()
        rew_player = from_node.get_player()
        done = self.state_manager.is_finished(leaf)
        parent = from_node 


        while done == False:
            
            action = self.actor.get_action(lite_model, leaf, player)
            
            leaf, player = self.state_manager.get_kid_from_move(player, leaf, action)
            next_leaf = parent.get_kid_with_action(action, rollout = True)

            if not next_leaf:
                
                next_leaf = Node(leaf, parent, player)
                parent.add_kid(next_leaf, action, rollout = True)
                
            parent = next_leaf
            done = self.state_manager.is_finished(leaf)
            
        rew = self.state_manager.get_reward(parent.get_state(), rew_player)
        
        return parent, rew


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
















       




      
        

            


                
            
