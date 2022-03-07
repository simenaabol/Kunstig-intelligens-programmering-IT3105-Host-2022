from collections import defaultdict
import numpy as np

class Node:
    
    def __init__(self, state, parent, player):

        self.state = state
        self.player = player
        self.parent = parent
        self.kids = defaultdict(lambda: None) # kok
        self.kids_rollout = defaultdict(lambda: None) # kok

        self.evaluate = 0
        self.count = 0


    def update_count(self):
        self.count +=1

    def update_evaluate(self, rew):
        self.evaluate += rew


    def get_player(self):
        return self.player

    def get_state(self):
        return self.state


    def get_kids(self):
        return self.kids

    def add_kid(self, kid, action, rollout = False): #kok siste del
        
        if rollout == True:
            self.kids_rollout[action] = kid
        else:
            self.kids[action] = kid
            


    def get_kid_with_action(self, action, rollout= False): # kok siste del
        
        if rollout == True:
            return self.kids_rollout[action]
        else:
            return self.kids[action]


    def remove_kid(self, action, rollout = False): # kok siste del
        
        if rollout == True:
            self.kids_rollout[action] = None
        else:
            self.kids[action] = None

    
    def get_action_count(self, action):

        if self.kids[action]:
            return self.kids[action].count
        else:
            return 0

    
    def get_kids_count(self):

        return len(self.kids)

    
    def get_parent(self):

        return self.parent


    def get_q_value(self, action):

        if self.get_action_count(action) != 0:
            # kok, endre på oppsettet?
            return ( self.get_kids(action).evaluate )  /  ( self.get_action_count(action) )
        else: 
            return 0

    
    def get_u_value(self, action, exploration_weight):

        # rein kok på oppsettet - ich
        
        return (  np.sqrt( np.log( self.count ) ) * exploration_weight  )  / ( 1 + self.get_action_count(action)   )


    

        
        